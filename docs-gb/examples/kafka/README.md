# Serving models through Kafka

Out of the box, MLServer provides support to receive inference requests from Kafka.
The Kafka server can run side-by-side with the REST and gRPC ones, and adds a new interface to interact with your model.
The inference responses coming back from your model, will also get written back to their own output topic.

In this example, we will showcase the integration with Kafka by serving a [Scikit-Learn](../sklearn/README) model thorugh Kafka.

## Run Kafka

We are going to start by running a simple local docker deployment of kafka that we can test against. This will be a minimal cluster that will consist of a single zookeeper node and a single broker.

You need to have Java installed in order for it to work correctly.


```python
!wget https://apache.mirrors.nublue.co.uk/kafka/2.8.0/kafka_2.12-2.8.0.tgz
!tar -zxvf kafka_2.12-2.8.0.tgz
!./kafka_2.12-2.8.0/bin/kafka-storage.sh format -t OXn8RTSlQdmxwjhKnSB_6A -c ./kafka_2.12-2.8.0/config/kraft/server.properties
```

### Run the no-zookeeper kafka broker

Now you can just run it with the following command outside the terminal:
```
!./kafka_2.12-2.8.0/bin/kafka-server-start.sh ./kafka_2.12-2.8.0/config/kraft/server.properties
```

### Create Topics

Now we can create the input and output topics required


```python
!./kafka_2.12-2.8.0/bin/kafka-topics.sh --create --topic mlserver-input --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
!./kafka_2.12-2.8.0/bin/kafka-topics.sh --create --topic mlserver-output --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
```

## Training

The first step will be to train a simple `scikit-learn` model.
For that, we will use the [MNIST example from the `scikit-learn` documentation](https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html) which trains an SVM model.


```python
# Original source code and more details can be found in:
# https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split

# The digits dataset
digits = datasets.load_digits()

# To apply a classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.001)

# Split data into train and test subsets
X_train, X_test, y_train, y_test = train_test_split(
    data, digits.target, test_size=0.5, shuffle=False)

# We learn the digits on the first half of the digits
classifier.fit(X_train, y_train)
```

### Saving our trained model

To save our trained model, we will serialise it using `joblib`.
While this is not a perfect approach, it's currently the recommended method to persist models to disk in the [`scikit-learn` documentation](https://scikit-learn.org/stable/modules/model_persistence.html).

Our model will be persisted as a file named `mnist-svm.joblib`


```python
import joblib

model_file_name = "mnist-svm.joblib"
joblib.dump(classifier, model_file_name)
```

## Serving

Now that we have trained and saved our model, the next step will be to serve it using `mlserver`. 
For that, we will need to create 2 configuration files: 

- `settings.json`: holds the configuration of our server (e.g. ports, log level, etc.).
- `model-settings.json`: holds the configuration of our model (e.g. input type, runtime to use, etc.).

Note that, the `settings.json` file will contain our Kafka configuration, including the address of the Kafka broker and the input / output topics that will be used for inference.

### `settings.json`


```python
%%writefile settings.json
{
    "debug": "true",
    "kafka_enabled": "true"
}
```

### `model-settings.json`


```python
%%writefile model-settings.json
{
    "name": "mnist-svm",
    "implementation": "mlserver_sklearn.SKLearnModel",
    "parameters": {
        "uri": "./mnist-svm.joblib",
        "version": "v0.1.0"
    }
}
```

### Start serving our model

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

### Send test inference request

We now have our model being served by `mlserver`.
To make sure that everything is working as expected, let's send a request from our test set.

For that, we can use the Python types that `mlserver` provides out of box, or we can build our request manually.


```python
import requests

x_0 = X_test[0:1]
inference_request = {
    "inputs": [
        {
          "name": "predict",
          "shape": x_0.shape,
          "datatype": "FP32",
          "data": x_0.tolist()
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/mnist-svm/versions/v0.1.0/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```

### Send inference request through Kafka

Now that we have verified that our server is accepting REST requests, we will try to send a new inference request through Kafka.
For this, we just need to send a request to the `mlserver-input` topic (which is the default input topic):


```python
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")

headers = {
    "mlserver-model": b"mnist-svm",
    "mlserver-version": b"v0.1.0",
}

producer.send(
    "mlserver-input",
    json.dumps(inference_request).encode("utf-8"),
    headers=list(headers.items()))
```

Once the message has gone into the queue, the Kafka server running within MLServer should receive this message and run inference.
The prediction output should then get posted into an output queue, which will be named `mlserver-output` by default.


```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "mlserver-output",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest")

for msg in consumer:
    print(f"key: {msg.key}")
    print(f"value: {msg.value}\n")
    break
```

As we should now be able to see above, the results of our inference request should now be visible in the output Kafka queue.


```python

```

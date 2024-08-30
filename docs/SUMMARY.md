* [MLServer](README.md)
* [Getting Started](getting-started.md)
* [User Guide](user-guide/README.md)
* [examples]()
│   ├── alibi-detect
│   │   ├── alibi-detector-artifacts
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── settings.json
│   ├── alibi-explain
│   │   ├── data
│   │   │   └── mnist_anchor_image
│   │   │       ├── explainer.dill
│   │   │       ├── meta.dill
│   │   │       └── segmentation_fn.dill
│   │   ├── model-settings.json
│   │   └── settings.json
│   ├── cassava
│   │   ├── app.py
│   │   ├── deployment.yaml
│   │   ├── helpers.py
│   │   ├── img
│   │   │   ├── cassava_examples.png
│   │   │   ├── slides.pdf
│   │   │   ├── step_1.png
│   │   │   ├── step_2.png
│   │   │   ├── step_3.png
│   │   │   ├── step_4.png
│   │   │   ├── step_5.png
│   │   │   └── video_play.png
│   │   ├── model
│   │   │   ├── model-settings.json
│   │   │   ├── requirements.txt
│   │   │   ├── saved_model.pb
│   │   │   ├── serve-model.py
│   │   │   ├── settings.json
│   │   │   └── variables
│   │   │       ├── variables.data-00000-of-00001
│   │   │       └── variables.index
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── test.py
│   ├── catboost
│   │   ├── model.cbm
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── settings.json
│   ├── conda
│   │   ├── environment.yml
│   │   ├── Makefile
│   │   ├── model.joblib
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   └── README.md
│   ├── content-type
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── runtime.py
│   ├── custom
│   │   ├── model-settings.json
│   │   ├── models.py
│   │   ├── numpyro-divorce.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── seldondeployment.yaml
│   │   └── settings.json
│   ├── custom-json
│   │   ├── jsonmodels.py
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── settings.json
│   ├── huggingface
│   │   ├── README.ipynb
│   │   └── README.md
│   ├── index.md
│   ├── kafka
│   │   ├── inference-request.json
│   │   ├── mnist-svm.joblib
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── settings.json
│   ├── lightgbm
│   │   ├── iris-lightgbm.bst
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── settings.json
│   ├── Makefile
│   ├── mlflow
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── src
│   │       └── train.py
│   ├── mllib
│   │   ├── data
│   │   │   ├── part-00000-3b569ac9-e283-4220-ba6c-31088ed23cb8-c000.snappy.parquet
│   │   │   └── _SUCCESS
│   │   ├── metadata
│   │   │   ├── part-00000
│   │   │   └── _SUCCESS
│   │   └── model-settings.json
│   ├── mms
│   │   ├── agaricus.txt.test
│   │   ├── agaricus.txt.train
│   │   ├── Makefile
│   │   ├── models
│   │   │   ├── mnist-svm
│   │   │   │   ├── model.joblib
│   │   │   │   └── model-settings.json
│   │   │   └── mushroom-xgboost
│   │   │       ├── model.json
│   │   │       └── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── settings.json
│   ├── model-repository
│   │   ├── models
│   │   │   ├── mnist-svm
│   │   │   │   ├── model.joblib
│   │   │   │   └── model-settings.json
│   │   │   └── mushroom-xgboost
│   │   │       ├── model.json
│   │   │       └── model-settings.json
│   │   ├── README.ipynb
│   │   └── README.md
│   ├── sklearn
│   │   ├── inference-request.json
│   │   ├── mnist-svm.joblib
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   └── settings.json
│   ├── streaming
│   │   ├── generate-request.json
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   ├── README.md
│   │   ├── settings.json
│   │   └── text_model.py
│   ├── tempo
│   │   ├── models
│   │   │   ├── inference-pipeline
│   │   │   │   └── model.pickle
│   │   │   ├── sklearn-iris
│   │   │   │   ├── metadata.yaml
│   │   │   │   └── model.joblib
│   │   │   └── xgboost-iris
│   │   │       ├── metadata.yaml
│   │   │       └── model.bst
│   │   ├── model-settings.json
│   │   ├── README.ipynb
│   │   └── README.md
│   └── xgboost
│       ├── agaricus.txt.test
│       ├── agaricus.txt.train
│       ├── model-settings.json
│       ├── mushroom-xgboost.json
│       ├── README.ipynb
│       ├── README.md
│       └── settings.json
├── favicon.ico
├── getting-started.md
├── reference
│   ├── api
│   │   ├── codecs.md
│   │   ├── index.md
│   │   ├── metrics.md
│   │   ├── model.md
│   │   └── types.md
│   ├── cli.md
│   ├── index.md
│   ├── model-settings.md
│   └── settings.md
├── references.bib
├── runtimes
│   ├── alibi-detect.md
│   ├── alibi-explain.md
│   ├── catboost.md
│   ├── custom.md
│   ├── huggingface.md
│   ├── index.md
│   ├── lightgbm.md
│   ├── mlflow.md
│   ├── mllib.md
│   ├── sklearn.md
│   └── xgboost.md
└── user-guide
    ├── adaptive-batching.md
    ├── content-type.md
    ├── custom.md
    ├── deployment
    │   ├── index.md
    │   ├── kserve.md
    │   └── seldon-core.md
    ├── index.md
    ├── metrics.md
    ├── openapi.md
    ├── parallel-inference.md
    └── streaming.md
* [](changelog.md)
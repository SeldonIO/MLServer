# MLServer CLI

The MLServer package includes a mlserver CLI designed to help with common tasks in a model’s lifecycle. You can see a high-level outline at any time via:

```bash
mlserver --help
```

## root

Command-line interface to manage MLServer models.

```bash
root [OPTIONS] COMMAND [ARGS]...
```

### Options

- `--version` (Default: `False`)
  Show the version and exit.

## build

Build a Docker image for a custom MLServer runtime.

```bash
root build [OPTIONS] FOLDER
```

### Options

- `-t`, `--tag` `<text>`

- `--no-cache` (Default: `False`)

### Arguments

- `FOLDER`
  Required argument

## dockerfile

Generate a Dockerfile

```bash
root dockerfile [OPTIONS] FOLDER
```

### Options

- `-i`, `--include-dockerignore` (Default: `False`)

### Arguments

- `FOLDER`
  Required argument

## infer

Deprecated: This experimental feature will be removed in future work.
    Execute batch inference requests against V2 inference server.

> Deprecated: This experimental feature will be removed in future work.

```bash
root infer [OPTIONS]
```

### Options

- `--url`, `-u` `<text>` (Default: `localhost:8080`; Env: `MLSERVER_INFER_URL`)
  URL of the MLServer to send inference requests to. Should not contain http or https.

- `--model-name`, `-m` `<text>` (Required; Env: `MLSERVER_INFER_MODEL_NAME`)
  Name of the model to send inference requests to.

- `--input-data-path`, `-i` `<path>` (Required; Env: `MLSERVER_INFER_INPUT_DATA_PATH`)
  Local path to the input file containing inference requests to be processed.

- `--output-data-path`, `-o` `<path>` (Required; Env: `MLSERVER_INFER_OUTPUT_DATA_PATH`)
  Local path to the output file for the inference responses to be  written to.

- `--workers`, `-w` `<integer>` (Default: `10`; Env: `MLSERVER_INFER_WORKERS`)

- `--retries`, `-r` `<integer>` (Default: `3`; Env: `MLSERVER_INFER_RETRIES`)

- `--batch-size`, `-s` `<integer>` (Default: `1`; Env: `MLSERVER_INFER_BATCH_SIZE`)
  Send inference requests grouped together as micro-batches.

- `--binary-data`, `-b` (Default: `False`; Env: `MLSERVER_INFER_BINARY_DATA`)
  Send inference requests as binary data (not fully supported).

- `--verbose`, `-v` (Default: `False`; Env: `MLSERVER_INFER_VERBOSE`)
  Verbose mode.

- `--extra-verbose`, `-vv` (Default: `False`; Env: `MLSERVER_INFER_EXTRA_VERBOSE`)
  Extra verbose mode (shows detailed requests and responses).

- `--transport`, `-t` `<choice>` (Options: `rest` | `grpc`; Default: `rest`; Env: `MLSERVER_INFER_TRANSPORT`)
  Transport type to use to send inference requests. Can be 'rest' or 'grpc' (not yet supported).

- `--request-headers`, `-H` `<text>` (Env: `MLSERVER_INFER_REQUEST_HEADERS`)
  Headers to be set on each inference request send to the server. Multiple options are allowed as: -H 'Header1: Val1' -H 'Header2: Val2'. When setting up as environmental provide as 'Header1:Val1 Header2:Val2'.

- `--timeout` `<integer>` (Default: `60`; Env: `MLSERVER_INFER_CONNECTION_TIMEOUT`)
  Connection timeout to be passed to tritonclient.

- `--batch-interval` `<float>` (Default: `0`; Env: `MLSERVER_INFER_BATCH_INTERVAL`)
  Minimum time interval (in seconds) between requests made by each worker.

- `--batch-jitter` `<float>` (Default: `0`; Env: `MLSERVER_INFER_BATCH_JITTER`)
  Maximum random jitter (in seconds) added to batch interval between requests.

- `--use-ssl` (Default: `False`; Env: `MLSERVER_INFER_USE_SSL`)
  Use SSL in communications with inference server.

- `--insecure` (Default: `False`; Env: `MLSERVER_INFER_INSECURE`)
  Disable SSL verification in communications. Use with caution.

## init

Generate a base project template

```bash
root init [OPTIONS]
```

### Options

- `-t`, `--template` `<text>` (Default: `https://github.com/EthicalML/sml-security/`)

## start

Start serving a machine learning model with MLServer.

```bash
root start [OPTIONS] FOLDER
```

### Arguments

- `FOLDER`
  Required argument

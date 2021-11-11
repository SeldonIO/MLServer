# MLServer Settings

MLServer can be configured through a `settings.json` file on the root folder
from where MLServer is started.
Note that these are server-wide settings (e.g. gRPC or HTTP port) which are
separate from the [invidual model settings](./model-settings).
Alternatively, this configuration can also be passed through **environment
variables** prefixed with `MLSERVER_` (e.g. `MLSERVER_GRPC_PORT`).

## Settings

```{eval-rst}

.. autopydantic_settings:: mlserver.settings.Settings
```

<a id="settings"></a>

# Settings

<a id="mlserver.settings.ModelSettings"></a>

### *pydantic settings* mlserver.settings.ModelSettings

* **Fields:**
  - [`cache_enabled (bool)`](#mlserver.settings.ModelSettings.cache_enabled)
  - [`implementation_ (str)`](#mlserver.settings.ModelSettings.implementation_)
  - [`inputs (List[mlserver.types.dataplane.MetadataTensor])`](#mlserver.settings.ModelSettings.inputs)
  - [`max_batch_size (int)`](#mlserver.settings.ModelSettings.max_batch_size)
  - [`max_batch_time (float)`](#mlserver.settings.ModelSettings.max_batch_time)
  - [`name (str)`](#mlserver.settings.ModelSettings.name)
  - [`outputs (List[mlserver.types.dataplane.MetadataTensor])`](#mlserver.settings.ModelSettings.outputs)
  - [`parallel_workers (int | None)`](#mlserver.settings.ModelSettings.parallel_workers)
  - [`parameters (mlserver.settings.ModelParameters | None)`](#mlserver.settings.ModelSettings.parameters)
  - [`platform (str)`](#mlserver.settings.ModelSettings.platform)
  - [`versions (List[str])`](#mlserver.settings.ModelSettings.versions)
  - [`warm_workers (bool)`](#mlserver.settings.ModelSettings.warm_workers)

<a id="mlserver.settings.ModelSettings.cache_enabled"></a>

#### *field* cache_enabled *: bool* *= False*

Enable caching for a specific model. This parameter can be used to disable
cache for a specific model, if the server level caching is enabled. If the
server level caching is disabled, this parameter value will have no effect.

<a id="mlserver.settings.ModelSettings.implementation_"></a>

#### *field* implementation_ *: str* *[Required]*

<a id="mlserver.settings.ModelSettings.inputs"></a>

#### *field* inputs *: List[[MetadataTensor](types.md#mlserver.types.MetadataTensor)]* *= []*

Metadata about the inputs accepted by the model.

<a id="mlserver.settings.ModelSettings.max_batch_size"></a>

#### *field* max_batch_size *: int* *= 0*

When adaptive batching is enabled, maximum number of requests to group
together in a single batch.

<a id="mlserver.settings.ModelSettings.max_batch_time"></a>

#### *field* max_batch_time *: float* *= 0.0*

When adaptive batching is enabled, maximum amount of time (in seconds)
to wait for enough requests to build a full batch.

<a id="mlserver.settings.ModelSettings.name"></a>

#### *field* name *: str* *= ''*

Name of the model.

<a id="mlserver.settings.ModelSettings.outputs"></a>

#### *field* outputs *: List[[MetadataTensor](types.md#mlserver.types.MetadataTensor)]* *= []*

Metadata about the outputs returned by the model.

<a id="mlserver.settings.ModelSettings.parameters"></a>

#### *field* parameters *: [ModelParameters](#mlserver.settings.ModelParameters) | None* *= None*

Extra parameters for each instance of this model.

<a id="mlserver.settings.ModelSettings.platform"></a>

#### *field* platform *: str* *= ''*

Framework used to train and serialise the model (e.g. sklearn).

<a id="mlserver.settings.ModelSettings.versions"></a>

#### *field* versions *: List[str]* *= []*

Versions of dependencies used to train the model (e.g.
sklearn/0.20.1).

<a id="mlserver.settings.ModelSettings.model_validate"></a>

#### *classmethod* model_validate(obj)

Validate a pydantic model instance.

* **Parameters:**
  * **obj** (*Any*) – The object to validate.
  * **strict** – Whether to enforce types strictly.
  * **from_attributes** – Whether to extract data from object attributes.
  * **context** – Additional context to pass to the validator.
* **Raises:**
  **ValidationError** – If the object could not be validated.
* **Returns:**
  The validated model instance.
* **Return type:**
  [*ModelSettings*](#mlserver.settings.ModelSettings)

<a id="mlserver.settings.ModelSettings.parse_file"></a>

#### *classmethod* parse_file(path)

* **Parameters:**
  **path** (*str*)
* **Return type:**
  [*ModelSettings*](#mlserver.settings.ModelSettings)

<a id="mlserver.settings.ModelSettings.__init__"></a>

#### \_\_init_\_(\*args, \*\*kwargs)

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

<a id="mlserver.settings.ModelSettings.model_post_init"></a>

#### model_post_init(context,)

This function is meant to behave like a BaseModel method to initialise private attributes.

It takes context as an argument since that’s what pydantic-core passes when calling it.

* **Parameters:**
  * **self** (*BaseModel*) – The BaseModel instance.
  * **context** (*Any*) – The context.
* **Return type:**
  None

<a id="mlserver.settings.ModelSettings.implementation"></a>

#### *property* implementation *: Type[MLModel]*

<a id="mlserver.settings.ModelSettings.parallel_workers"></a>

#### parallel_workers *: int | None*

Data descriptor used to emit a runtime deprecation warning before accessing a deprecated field.

<a id="mlserver.settings.ModelSettings.msg"></a>

#### msg

The deprecation message to be emitted.

<a id="mlserver.settings.ModelSettings.wrapped_property"></a>

#### wrapped_property

The property instance if the deprecated field is a computed field, or None.

<a id="mlserver.settings.ModelSettings.field_name"></a>

#### field_name

The name of the field being deprecated.

<a id="mlserver.settings.ModelSettings.version"></a>

#### *property* version *: str | None*

<a id="mlserver.settings.ModelSettings.warm_workers"></a>

#### warm_workers *: bool*

Data descriptor used to emit a runtime deprecation warning before accessing a deprecated field.

<a id="id0"></a>

#### msg

The deprecation message to be emitted.

<a id="id1"></a>

#### wrapped_property

The property instance if the deprecated field is a computed field, or None.

<a id="id2"></a>

#### field_name

The name of the field being deprecated.

<a id="extra-model-parameters"></a>

# Extra Model Parameters

<a id="mlserver.settings.ModelParameters"></a>

### *pydantic settings* mlserver.settings.ModelParameters

Parameters that apply only to a particular instance of a model.
This can include things like model weights, or arbitrary `extra`
parameters particular to the underlying inference runtime.
The main difference with respect to `ModelSettings` is that parameters
can change on each instance (e.g. each version) of the model.

* **Fields:**
  - [`autogenerate_inference_pool_gid (bool)`](#mlserver.settings.ModelParameters.autogenerate_inference_pool_gid)
  - [`content_type (str | None)`](#mlserver.settings.ModelParameters.content_type)
  - [`environment_path (str | None)`](#mlserver.settings.ModelParameters.environment_path)
  - [`environment_tarball (str | None)`](#mlserver.settings.ModelParameters.environment_tarball)
  - [`extra (dict | None)`](#mlserver.settings.ModelParameters.extra)
  - [`format (str | None)`](#mlserver.settings.ModelParameters.format)
  - [`inference_pool_gid (str | None)`](#mlserver.settings.ModelParameters.inference_pool_gid)
  - [`uri (str | None)`](#mlserver.settings.ModelParameters.uri)
  - [`version (str | None)`](#mlserver.settings.ModelParameters.version)
* **Validators:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid) » `all fields`

<a id="mlserver.settings.ModelParameters.autogenerate_inference_pool_gid"></a>

#### *field* autogenerate_inference_pool_gid *: bool* *= False*

Flag to autogenerate the inference pool group id for this model.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.content_type"></a>

#### *field* content_type *: str | None* *= None*

Default content type to use for requests and responses.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.environment_path"></a>

#### *field* environment_path *: str | None* *= None*

Path to a directory that contains the python environment to be used
to load this model.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.environment_tarball"></a>

#### *field* environment_tarball *: str | None* *= None*

Path to the environment tarball which should be used to load this
model.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.extra"></a>

#### *field* extra *: dict | None* *= {}*

Arbitrary settings, dependent on the inference runtime
implementation.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.format"></a>

#### *field* format *: str | None* *= None*

Format of the model (only available on certain runtimes).

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.inference_pool_gid"></a>

#### *field* inference_pool_gid *: str | None* *= None*

Inference pool group id to be used to serve this model.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.uri"></a>

#### *field* uri *: str | None* *= None*

URI where the model artifacts can be found.
This path must be either absolute or relative to where MLServer is running.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.version"></a>

#### *field* version *: str | None* *= None*

Version of the model.

* **Validated by:**
  - [`set_inference_pool_gid`](#mlserver.settings.ModelParameters.set_inference_pool_gid)

<a id="mlserver.settings.ModelParameters.set_inference_pool_gid"></a>

#### *validator* set_inference_pool_gid  *»*  *all fields*

* **Return type:**
  *Self*

# MLServer Settings

## Module `mlserver.settings`

### Class `AliasChoices`

```python
class AliasChoices
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/alias#aliaspath-and-aliaschoices

A data class used by `validation_alias` as a convenience to create aliases.

Attributes:
    choices: A list containing a string or `AliasPath`.


### Class `Any`

```python
class Any
```

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.


### Class `BaseSettings`

```python
class BaseSettings
```

Base class for settings, allowing values to be overridden by environment variables.

This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

Args:
    _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
        Defaults to `None`.
    _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
        Defaults to `False`.
    _env_prefix: Prefix for all environment variables. Defaults to `None`.
    _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
        means that the value from `model_config['env_file']` should be used. You can also pass
        `None` to indicate that environment variables should not be loaded from an env file.
    _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
    _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
    _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
    _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
        into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
    _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
    _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
        Otherwse, defaults to sys.argv[0].
    _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
        If set to `True`, defaults to sys.argv[1:].
    _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
    _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
        `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
        _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
    _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
    _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
    _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
    _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
        Defaults to `False`.
    _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
        Defaults to `True`.
    _cli_prefix: The root parser command line arguments prefix. Defaults to "".
    _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
    _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
        (e.g. --flag, --no-flag). Defaults to `False`.
    _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
    _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.

**JSON Schema:**

```json
{
  "additionalProperties": false,
  "properties": {},
  "title": "BaseSettings",
  "type": "object"
}
```


### Class `CORSSettings`

```python
class CORSSettings
```

Base class for settings, allowing values to be overridden by environment variables.

This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

Args:
    _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
        Defaults to `None`.
    _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
        Defaults to `False`.
    _env_prefix: Prefix for all environment variables. Defaults to `None`.
    _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
        means that the value from `model_config['env_file']` should be used. You can also pass
        `None` to indicate that environment variables should not be loaded from an env file.
    _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
    _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
    _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
    _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
        into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
    _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
    _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
        Otherwse, defaults to sys.argv[0].
    _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
        If set to `True`, defaults to sys.argv[1:].
    _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
    _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
        `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
        _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
    _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
    _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
    _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
    _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
        Defaults to `False`.
    _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
        Defaults to `True`.
    _cli_prefix: The root parser command line arguments prefix. Defaults to "".
    _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
    _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
        (e.g. --flag, --no-flag). Defaults to `False`.
    _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
    _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.

**JSON Schema:**

```json
{
  "properties": {
    "allow_origins": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": [],
      "title": "Allow Origins"
    },
    "allow_origin_regex": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Allow Origin Regex"
    },
    "allow_credentials": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "default": false,
      "title": "Allow Credentials"
    },
    "allow_methods": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": [
        "GET"
      ],
      "title": "Allow Methods"
    },
    "allow_headers": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": [],
      "title": "Allow Headers"
    },
    "expose_headers": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": [],
      "title": "Expose Headers"
    },
    "max_age": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": 600,
      "title": "Max Age"
    }
  },
  "title": "CORSSettings",
  "type": "object"
}
```


### Function `Field`

```python
Field(default: 'Any' = PydanticUndefined, *, default_factory: 'typing.Callable[[], Any] | None' = PydanticUndefined, alias: 'str | None' = PydanticUndefined, alias_priority: 'int | None' = PydanticUndefined, validation_alias: 'str | AliasPath | AliasChoices | None' = PydanticUndefined, serialization_alias: 'str | None' = PydanticUndefined, title: 'str | None' = PydanticUndefined, field_title_generator: 'typing_extensions.Callable[[str, FieldInfo], str] | None' = PydanticUndefined, description: 'str | None' = PydanticUndefined, examples: 'list[Any] | None' = PydanticUndefined, exclude: 'bool | None' = PydanticUndefined, discriminator: 'str | types.Discriminator | None' = PydanticUndefined, deprecated: 'Deprecated | str | bool | None' = PydanticUndefined, json_schema_extra: 'JsonDict | typing.Callable[[JsonDict], None] | None' = PydanticUndefined, frozen: 'bool | None' = PydanticUndefined, validate_default: 'bool | None' = PydanticUndefined, repr: 'bool' = PydanticUndefined, init: 'bool | None' = PydanticUndefined, init_var: 'bool | None' = PydanticUndefined, kw_only: 'bool | None' = PydanticUndefined, pattern: 'str | typing.Pattern[str] | None' = PydanticUndefined, strict: 'bool | None' = PydanticUndefined, coerce_numbers_to_str: 'bool | None' = PydanticUndefined, gt: 'annotated_types.SupportsGt | None' = PydanticUndefined, ge: 'annotated_types.SupportsGe | None' = PydanticUndefined, lt: 'annotated_types.SupportsLt | None' = PydanticUndefined, le: 'annotated_types.SupportsLe | None' = PydanticUndefined, multiple_of: 'float | None' = PydanticUndefined, allow_inf_nan: 'bool | None' = PydanticUndefined, max_digits: 'int | None' = PydanticUndefined, decimal_places: 'int | None' = PydanticUndefined, min_length: 'int | None' = PydanticUndefined, max_length: 'int | None' = PydanticUndefined, union_mode: "Literal['smart', 'left_to_right']" = PydanticUndefined, fail_fast: 'bool | None' = PydanticUndefined, **extra: 'Unpack[_EmptyKwargs]') -> 'Any'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/fields

Create a field for objects that can be configured.

Used to provide extra information about a field, either for the model schema or complex validation. Some arguments
apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.

Note:
    - Any `_Unset` objects will be replaced by the corresponding value defined in the `_DefaultValues` dictionary. If a key for the `_Unset` object is not found in the `_DefaultValues` dictionary, it will default to `None`

Args:
    default: Default value if the field is not set.
    default_factory: A callable to generate the default value, such as :func:`~datetime.utcnow`.
    alias: The name to use for the attribute when validating or serializing by alias.
        This is often used for things like converting between snake and camel case.
    alias_priority: Priority of the alias. This affects whether an alias generator is used.
    validation_alias: Like `alias`, but only affects validation, not serialization.
    serialization_alias: Like `alias`, but only affects serialization, not validation.
    title: Human-readable title.
    field_title_generator: A callable that takes a field name and returns title for it.
    description: Human-readable description.
    examples: Example values for this field.
    exclude: Whether to exclude the field from the model serialization.
    discriminator: Field name or Discriminator for discriminating the type in a tagged union.
    deprecated: A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport,
        or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.
    json_schema_extra: A dict or callable to provide extra JSON schema properties.
    frozen: Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.
    validate_default: If `True`, apply validation to the default value every time you create an instance.
        Otherwise, for performance reasons, the default value of the field is trusted and not validated.
    repr: A boolean indicating whether to include the field in the `__repr__` output.
    init: Whether the field should be included in the constructor of the dataclass.
        (Only applies to dataclasses.)
    init_var: Whether the field should _only_ be included in the constructor of the dataclass.
        (Only applies to dataclasses.)
    kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass.
        (Only applies to dataclasses.)
    coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
    strict: If `True`, strict validation is applied to the field.
        See [Strict Mode](../concepts/strict_mode.md) for details.
    gt: Greater than. If set, value must be greater than this. Only applicable to numbers.
    ge: Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.
    lt: Less than. If set, value must be less than this. Only applicable to numbers.
    le: Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.
    multiple_of: Value must be a multiple of this. Only applicable to numbers.
    min_length: Minimum length for iterables.
    max_length: Maximum length for iterables.
    pattern: Pattern for strings (a regular expression).
    allow_inf_nan: Allow `inf`, `-inf`, `nan`. Only applicable to numbers.
    max_digits: Maximum number of allow digits for strings.
    decimal_places: Maximum number of decimal places allowed for numbers.
    union_mode: The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`.
        See [Union Mode](../concepts/unions.md#union-modes) for details.
    fail_fast: If `True`, validation will stop on the first error. If `False`, all validation errors will be collected.
        This option can be applied only to iterable types (list, tuple, set, and frozenset).
    extra: (Deprecated) Extra fields that will be included in the JSON schema.

        !!! warning Deprecated
            The `extra` kwargs is deprecated. Use `json_schema_extra` instead.

Returns:
    A new [`FieldInfo`][pydantic.fields.FieldInfo]. The return annotation is `Any` so `Field` can be used on
        type-annotated fields without causing a type error.


### Class `ImportString`

```python
class ImportString
```

A type that can be used to import a type from a string.

`ImportString` expects a string and loads the Python object importable at that dotted path.
Attributes of modules may be separated from the module by `:` or `.`, e.g. if `'math:cos'` was provided,
the resulting field value would be the function`cos`. If a `.` is used and both an attribute and submodule
are present at the same path, the module will be preferred.

On model instantiation, pointers will be evaluated and imported. There is
some nuance to this behavior, demonstrated in the examples below.

**Good behavior:**
```py
import math

from pydantic import BaseModel, Field, ImportString, ValidationError

class ImportThings(BaseModel):
    obj: ImportString

# A string value will cause an automatic import
my_cos = ImportThings(obj='math.cos')

# You can use the imported function as you would expect
cos_of_0 = my_cos.obj(0)
assert cos_of_0 == 1

# A string whose value cannot be imported will raise an error
try:
    ImportThings(obj='foo.bar')
except ValidationError as e:
    print(e)
    '''
    1 validation error for ImportThings
    obj
      Invalid python path: No module named 'foo.bar' [type=import_error, input_value='foo.bar', input_type=str]
    '''

# Actual python objects can be assigned as well
my_cos = ImportThings(obj=math.cos)
my_cos_2 = ImportThings(obj='math.cos')
my_cos_3 = ImportThings(obj='math:cos')
assert my_cos == my_cos_2 == my_cos_3

# You can set default field value either as Python object:
class ImportThingsDefaultPyObj(BaseModel):
    obj: ImportString = math.cos

# or as a string value (but only if used with `validate_default=True`)
class ImportThingsDefaultString(BaseModel):
    obj: ImportString = Field(default='math.cos', validate_default=True)

my_cos_default1 = ImportThingsDefaultPyObj()
my_cos_default2 = ImportThingsDefaultString()
assert my_cos_default1.obj == my_cos_default2.obj == math.cos

# note: this will not work!
class ImportThingsMissingValidateDefault(BaseModel):
    obj: ImportString = 'math.cos'

my_cos_default3 = ImportThingsMissingValidateDefault()
assert my_cos_default3.obj == 'math.cos'  # just string, not evaluated
```

Serializing an `ImportString` type to json is also possible.

```py lint="skip"
from pydantic import BaseModel, ImportString

class ImportThings(BaseModel):
    obj: ImportString

# Create an instance
m = ImportThings(obj='math.cos')
print(m)
#> obj=<built-in function cos>
print(m.model_dump_json())
#> {"obj":"math.cos"}
```


### Class `MetadataTensor`

```python
class MetadataTensor
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "datatype": {
      "$ref": "#/$defs/Datatype"
    },
    "shape": {
      "items": {
        "type": "integer"
      },
      "title": "Shape",
      "type": "array"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "name",
    "datatype",
    "shape"
  ],
  "title": "MetadataTensor",
  "type": "object"
}
```


### Class `ModelParameters`

```python
class ModelParameters
```

Parameters that apply only to a particular instance of a model.
This can include things like model weights, or arbitrary ``extra``
parameters particular to the underlying inference runtime.
The main difference with respect to ``ModelSettings`` is that parameters
can change on each instance (e.g. each version) of the model.

**JSON Schema:**

```json
{
  "additionalProperties": true,
  "description": "Parameters that apply only to a particular instance of a model.\nThis can include things like model weights, or arbitrary ``extra``\nparameters particular to the underlying inference runtime.\nThe main difference with respect to ``ModelSettings`` is that parameters\ncan change on each instance (e.g. each version) of the model.",
  "properties": {
    "uri": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Uri"
    },
    "version": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Version"
    },
    "environment_path": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Environment Path"
    },
    "environment_tarball": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Environment Tarball"
    },
    "inference_pool_gid": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Inference Pool Gid"
    },
    "autogenerate_inference_pool_gid": {
      "default": false,
      "title": "Autogenerate Inference Pool Gid",
      "type": "boolean"
    },
    "format": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Format"
    },
    "content_type": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Content Type"
    },
    "extra": {
      "anyOf": [
        {
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": {},
      "title": "Extra"
    }
  },
  "title": "ModelParameters",
  "type": "object"
}
```


### Class `ModelSettings`

```python
class ModelSettings
```

Base class for settings, allowing values to be overridden by environment variables.

This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

Args:
    _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
        Defaults to `None`.
    _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
        Defaults to `False`.
    _env_prefix: Prefix for all environment variables. Defaults to `None`.
    _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
        means that the value from `model_config['env_file']` should be used. You can also pass
        `None` to indicate that environment variables should not be loaded from an env file.
    _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
    _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
    _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
    _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
        into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
    _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
    _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
        Otherwse, defaults to sys.argv[0].
    _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
        If set to `True`, defaults to sys.argv[1:].
    _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
    _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
        `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
        _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
    _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
    _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
    _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
    _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
        Defaults to `False`.
    _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
        Defaults to `True`.
    _cli_prefix: The root parser command line arguments prefix. Defaults to "".
    _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
    _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
        (e.g. --flag, --no-flag). Defaults to `False`.
    _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
    _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "MetadataTensor": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "datatype": {
          "$ref": "#/$defs/Datatype"
        },
        "shape": {
          "items": {
            "type": "integer"
          },
          "title": "Shape",
          "type": "array"
        },
        "parameters": {
          "anyOf": [
            {
              "$ref": "#/$defs/Parameters"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "name",
        "datatype",
        "shape"
      ],
      "title": "MetadataTensor",
      "type": "object"
    },
    "ModelParameters": {
      "additionalProperties": true,
      "description": "Parameters that apply only to a particular instance of a model.\nThis can include things like model weights, or arbitrary ``extra``\nparameters particular to the underlying inference runtime.\nThe main difference with respect to ``ModelSettings`` is that parameters\ncan change on each instance (e.g. each version) of the model.",
      "properties": {
        "uri": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Uri"
        },
        "version": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Version"
        },
        "environment_path": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Environment Path"
        },
        "environment_tarball": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Environment Tarball"
        },
        "inference_pool_gid": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Inference Pool Gid"
        },
        "autogenerate_inference_pool_gid": {
          "default": false,
          "title": "Autogenerate Inference Pool Gid",
          "type": "boolean"
        },
        "format": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Format"
        },
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "extra": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": {},
          "title": "Extra"
        }
      },
      "title": "ModelParameters",
      "type": "object"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    }
  },
  "properties": {
    "implementation": {
      "title": "Implementation",
      "type": "string"
    },
    "name": {
      "default": "",
      "title": "Name",
      "type": "string"
    },
    "platform": {
      "default": "",
      "title": "Platform",
      "type": "string"
    },
    "versions": {
      "default": [],
      "items": {
        "type": "string"
      },
      "title": "Versions",
      "type": "array"
    },
    "inputs": {
      "default": [],
      "items": {
        "$ref": "#/$defs/MetadataTensor"
      },
      "title": "Inputs",
      "type": "array"
    },
    "outputs": {
      "default": [],
      "items": {
        "$ref": "#/$defs/MetadataTensor"
      },
      "title": "Outputs",
      "type": "array"
    },
    "parallel_workers": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "deprecated": true,
      "description": "Use the `parallel_workers` field the server wide settings instead.",
      "title": "Parallel Workers"
    },
    "warm_workers": {
      "default": false,
      "deprecated": true,
      "description": "Inference workers will now always be `warmed up` at start time.",
      "title": "Warm Workers",
      "type": "boolean"
    },
    "max_batch_size": {
      "default": 0,
      "title": "Max Batch Size",
      "type": "integer"
    },
    "max_batch_time": {
      "default": 0.0,
      "title": "Max Batch Time",
      "type": "number"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/ModelParameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "cache_enabled": {
      "default": false,
      "title": "Cache Enabled",
      "type": "boolean"
    }
  },
  "required": [
    "implementation"
  ],
  "title": "ModelSettings",
  "type": "object"
}
```


### Class `Settings`

```python
class Settings
```

Base class for settings, allowing values to be overridden by environment variables.

This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

Args:
    _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
        Defaults to `None`.
    _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
        Defaults to `False`.
    _env_prefix: Prefix for all environment variables. Defaults to `None`.
    _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
        means that the value from `model_config['env_file']` should be used. You can also pass
        `None` to indicate that environment variables should not be loaded from an env file.
    _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
    _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
    _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
    _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
        into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
    _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
    _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
        Otherwse, defaults to sys.argv[0].
    _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
        If set to `True`, defaults to sys.argv[1:].
    _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
    _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
        `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
        _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
    _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
    _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
    _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
    _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
        Defaults to `False`.
    _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
        Defaults to `True`.
    _cli_prefix: The root parser command line arguments prefix. Defaults to "".
    _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
    _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
        (e.g. --flag, --no-flag). Defaults to `False`.
    _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
    _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.

**JSON Schema:**

```json
{
  "$defs": {
    "CORSSettings": {
      "properties": {
        "allow_origins": {
          "anyOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "default": [],
          "title": "Allow Origins"
        },
        "allow_origin_regex": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Allow Origin Regex"
        },
        "allow_credentials": {
          "anyOf": [
            {
              "type": "boolean"
            },
            {
              "type": "null"
            }
          ],
          "default": false,
          "title": "Allow Credentials"
        },
        "allow_methods": {
          "anyOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "default": [
            "GET"
          ],
          "title": "Allow Methods"
        },
        "allow_headers": {
          "anyOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "default": [],
          "title": "Allow Headers"
        },
        "expose_headers": {
          "anyOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "default": [],
          "title": "Expose Headers"
        },
        "max_age": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": 600,
          "title": "Max Age"
        }
      },
      "title": "CORSSettings",
      "type": "object"
    }
  },
  "properties": {
    "debug": {
      "default": true,
      "title": "Debug",
      "type": "boolean"
    },
    "parallel_workers": {
      "default": 1,
      "title": "Parallel Workers",
      "type": "integer"
    },
    "parallel_workers_timeout": {
      "default": 5,
      "title": "Parallel Workers Timeout",
      "type": "integer"
    },
    "environments_dir": {
      "default": "/Users/paul.bridi/Projects/MLServer/.envs",
      "title": "Environments Dir",
      "type": "string"
    },
    "model_repository_implementation": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Model Repository Implementation"
    },
    "model_repository_root": {
      "default": ".",
      "title": "Model Repository Root",
      "type": "string"
    },
    "model_repository_implementation_args": {
      "default": {},
      "title": "Model Repository Implementation Args",
      "type": "object"
    },
    "load_models_at_startup": {
      "default": true,
      "title": "Load Models At Startup",
      "type": "boolean"
    },
    "server_name": {
      "default": "mlserver",
      "title": "Server Name",
      "type": "string"
    },
    "server_version": {
      "default": "1.7.0.dev0",
      "title": "Server Version",
      "type": "string"
    },
    "extensions": {
      "default": [],
      "items": {
        "type": "string"
      },
      "title": "Extensions",
      "type": "array"
    },
    "host": {
      "default": "0.0.0.0",
      "title": "Host",
      "type": "string"
    },
    "http_port": {
      "default": 8080,
      "title": "Http Port",
      "type": "integer"
    },
    "root_path": {
      "default": "",
      "title": "Root Path",
      "type": "string"
    },
    "grpc_port": {
      "default": 8081,
      "title": "Grpc Port",
      "type": "integer"
    },
    "grpc_max_message_length": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Grpc Max Message Length"
    },
    "cors_settings": {
      "anyOf": [
        {
          "$ref": "#/$defs/CORSSettings"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "metrics_endpoint": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "/metrics",
      "title": "Metrics Endpoint"
    },
    "metrics_port": {
      "default": 8082,
      "title": "Metrics Port",
      "type": "integer"
    },
    "metrics_rest_server_prefix": {
      "default": "rest_server",
      "title": "Metrics Rest Server Prefix",
      "type": "string"
    },
    "metrics_dir": {
      "default": "/Users/paul.bridi/Projects/MLServer/.metrics",
      "title": "Metrics Dir",
      "type": "string"
    },
    "use_structured_logging": {
      "default": false,
      "title": "Use Structured Logging",
      "type": "boolean"
    },
    "logging_settings": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Logging Settings"
    },
    "kafka_enabled": {
      "default": false,
      "title": "Kafka Enabled",
      "type": "boolean"
    },
    "kafka_servers": {
      "default": "localhost:9092",
      "title": "Kafka Servers",
      "type": "string"
    },
    "kafka_topic_input": {
      "default": "mlserver-input",
      "title": "Kafka Topic Input",
      "type": "string"
    },
    "kafka_topic_output": {
      "default": "mlserver-output",
      "title": "Kafka Topic Output",
      "type": "string"
    },
    "tracing_server": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Tracing Server"
    },
    "cache_enabled": {
      "default": false,
      "title": "Cache Enabled",
      "type": "boolean"
    },
    "cache_size": {
      "default": 100,
      "title": "Cache Size",
      "type": "integer"
    },
    "gzip_enabled": {
      "default": true,
      "title": "Gzip Enabled",
      "type": "boolean"
    }
  },
  "title": "Settings",
  "type": "object"
}
```


### Class `SettingsConfigDict`

```python
class SettingsConfigDict
```

dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)


### Function `contextmanager`

```python
contextmanager(func)
```

@contextmanager decorator.

Typical usage:

    @contextmanager
    def some_generator(<arguments>):
        <setup>
        try:
            yield <value>
        finally:
            <cleanup>

This makes this:

    with some_generator(<arguments>) as <variable>:
        <body>

equivalent to this:

    <setup>
    try:
        <variable> = <value>
        <body>
    finally:
        <cleanup>


### Function `import_string`

```python
import_string(value: 'Any') -> 'Any'
```




### Function `model_validator`

```python
model_validator(*, mode: "Literal['wrap', 'before', 'after']") -> 'Any'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/validators/#model-validators

Decorate model methods for validation purposes.

Example usage:
```py
from typing_extensions import Self

from pydantic import BaseModel, ValidationError, model_validator

class Square(BaseModel):
    width: float
    height: float

    @model_validator(mode='after')
    def verify_square(self) -> Self:
        if self.width != self.height:
            raise ValueError('width and height do not match')
        return self

s = Square(width=1, height=1)
print(repr(s))
#> Square(width=1.0, height=1.0)

try:
    Square(width=1, height=2)
except ValidationError as e:
    print(e)
    '''
    1 validation error for Square
      Value error, width and height do not match [type=value_error, input_value={'width': 1, 'height': 2}, input_type=dict]
    '''
```

For more in depth examples, see [Model Validators](../concepts/validators.md#model-validators).

Args:
    mode: A required string literal that specifies the validation mode.
        It can be one of the following: 'wrap', 'before', or 'after'.

Returns:
    A decorator that can be used to decorate a function to be used as a model validator.


### Function `no_type_check`

```python
no_type_check(arg)
```

Decorator to indicate that annotations are not type hints.

The argument must be a class or function; if it is a class, it
applies recursively to all methods and classes defined in that class
(but not to methods defined in its superclasses or subclasses).

This mutates the function(s) or class(es) in place.


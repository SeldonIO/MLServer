# mlserver.types.InferenceErrorResponse

### *pydantic model* mlserver.types.InferenceErrorResponse

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "InferenceErrorResponse",
   "type": "object",
   "properties": {
      "error": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Error"
      }
   }
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

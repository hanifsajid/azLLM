Models Nomenclature
===================

Model identifiers follow a structured format to ensure clarity and flexibility when working across different providers and configurations.

Format
-------

```python
client:model::version
```

- **`client`** → The model provider (e.g., `openai`, `deepseek`, `grok`, `gemini`, `anthropic`, `ollama`, `fireworks`)
- **`model`** → The exact model name as defined by the provider
- **`version`** → A user-defined label to distinguish between configurations (e.g., `v1`, `default`, `projectX`)

> `model` and `version` are **only required** when `azLLM` is instantiated with **custom configurations**.

Colon Rules
-------------

- Use a **single colon (`:`)** to separate `client` and `model`
- Use **double colons (`::`)** to separate `model` and `version`

Examples
--------

- `openai:gpt-4.1-2025-04-14::default`
- `deepseek:deepseek-chat::v2`
- `fireworks:accounts/fireworks/models/llama4-scout-instruct-basic::project1`

Notes
-----

- For **default configurations**, simply provide the `client` name (e.g., `openai`). A default model and version will be applied automatically.
- For **custom configurations**, always use the full `client:model::version` format.
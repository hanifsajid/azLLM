Configurations Management
=========================

The `azLLMConfigs` class enables you to **view, customize, and manage** model configurations used by `azLLM`.

You can work in two modes:

- **Default mode**: Uses built-in configurations per client.
- **Custom mode**: Lets you define your own configurations.

> **NOTE:** Once `azLLM` is initialized with custom configurations, it will no longer use default ones in that session.

Accessing Default Configurations
--------------------------------

Default configurations are pre-defined for each supported client (e.g., OpenAI, DeepSeek, Grok, Fireworks).

```python
from azllm import azLLMConfigs

configmanager = azLLMConfigs()

configmanager.get_default_configs('all')     # Get configs for all clients
configmanager.get_default_configs('grok')    # Get configs for a specific client
```

Working with Custom Configurations
------------------------------------

To define your own model configurations, initialize `azLLMConfigs` with `custom=True`.
This will create a local configuration file at:

```shell
custom_configs/config.yaml
```

You can:
- Edit the config file manually, or
- Programmatically update it using `update_custom_configs()`.

Why use custom configurations?
------------------------------

Custom configs give you control over:
- Response style (via `system_message`)
- Creativity (`temperature`)
- Output length (`max_tokens`)
- Repetition control (`frequency_penalty`, `presence_penalty`)

Example: Creating & Updating Custom Configurations
---------------------------------------------------

```python
configmanager = azLLMConfigs(custom=True)

example_conf = {
    'openai': {
        'gpt-4o-mini': {
            'version': 'v1',
            'parameters': {
                'system_message': 'You are an advanced AI assistant',
                'temperature': 0.6,
                'max_tokens': 1500,
                'frequency_penalty': 0.5,
                'presence_penalty': 0.1
            }
        }
    },
    'deepseek': {
        'deepseek-chat': {
            'version': 'v2',
            'parameters': {
                'system_message': 'You are an advanced AI assistant.',
                'temperature': 0.7,
                'max_tokens': 1024,
                'frequency_penalty': 0,
                'presence_penalty': 0
            }
        }
    }
}

for client, models in example_conf.items():
    configmanager.update_custom_configs(client, models)
```

Accessing Custom Configurations
-------------------------------

After switching to custom mode, access your configurations using:

```python
configmanager.custom_configs
```

Notes
-----

- If a model's config is missing in custom mode, it may raise an error. Be sure to define all necessary parameters.


Introduction
=============

## azllm

`azllm` is a Python package designed to interface with various large language models (LLMs) from different AI providers. It offers a unified interface for interacting with models from providers like **OpenAI**, **DeepSeek**, **Grok**, **Gemini**, **Meta's Llama**, **Anthropic**, **Ollama**, and others. The package allows for customizable configurations, batch generation, parallel generation, error handling, and the ability to parse structured responses from different models.

## Features

- **Unified Client Interface**: A single interface for interacting with various language models.
- **Customizable Parameters**: Easily configure parameters like `temperature`, `max_tokens`, and more for each model.
- **Batch Generation**: Generate responses for multiple prompts in a single function call.
- **Parallel Generation**: Generate text in parallel using different clients and models for the same prompt.
- **Parse Responses**: Handle different model responses with parsing support for those models that support it.
- **Error Handling**: Graceful error handling with informative messages in case of failures.
- **Lazy Client Initialization**: Clients are initialized only when needed to optimize performance.
- **Environment Configuration**: API keys and other secrets are managed via `.env` files.

## Supported Clients

- <a href="https://platform.openai.com/docs/overview" target="_blank">OpenAI</a>
- <a href="https://api-docs.deepseek.com" target="_blank">DeepSeek</a>
- <a href="https://x.ai" target="_blank">Grok</a>
- <a href="https://www.anthropic.com/claude" target="_blank">Anthropic</a>
- <a href="https://fireworks.ai" target="_blank">Fireworks</a> for Meta's LLaMA and others.
- <a href="https://ai.google.dev/gemini-api/docs" target="_blank">Google's Gemini</a>
- <a href="https://ollama.com" target="_blank">Ollama</a>

**NOTE:**   If you would like to request support for additional LLMs, please open a new issue on our <a href= "https://github.com/hanifsajid/azllm/issues" target="_blank">GitHub page</a>.
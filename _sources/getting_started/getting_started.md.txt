Set Up
======

## Installation

You can install the `azllm` package via pip:

```bash
pip install azllm
```

## Prerequisites

- Python 3.11+
- `.env` file to store your API keys
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    DEEPSEEK_API_KEY=your_deepseek_api_key
    XAI_API_KEY=your_xai_api_key
    GEMINI_API_KEY=your_gemini_api_key
    ANTHROPIC_API_KEY=your_anthropic_api_key
    FIREWORKS_API_KEY=your_fireworks_api_key
    ```
- [Ollama](https://ollama.com) must be installed and running locally to use Ollama models.
- The package expects the Ollama server to be available at `http://localhost:11434/v1` (default)


Dynamic Parameters: `kwargs`
===========================

The `kwargs` parameter lets you dynamically update any model configuration at runtime. It works whether you are using default or custom settings, and it overrides existing settings or adds new ones.

It supports both parsed (structured output) and unparsed modes.

Format Guide by Method:
-----------------------

```python
from azllm import azLLM
manager = azLLM()  # Instantiated with default parameters 
```

**`generate_text`**:  

- Accepts a **single dictionary**
- Don't forget to use `parse` when using `response_format` in kwargs

Exmaple: 

```python
from pydantic import BaseModel, Field

class FinalAnswer(BaseModel):
    capital: str = Field(..., description="Capital name only")

prompt = "What is the capital of France?"
generated = manager.generate_text(
    'openai',
    prompt,
    kwargs={
        'response_format': FinalAnswer,
        'temperature': 1,
        'system_message': 'You are an advanced AI assistant.'
    },
    parse=True
)

print(generated)
```

  
**`batch_generate`**:  
- Accepts a **list of dictionaries**, one per prompt.  
  > Tip: If a prompt doesn’t require custom kwargs, include an **empty dictionary** in its place.

Example:

```Python
batch_prompts = [
    'What is the capital of France?',
    'Tell me a joke.'
    ]

results = manager.batch_generate('openai', batch_prompts, 
                                    kwargs = [{'max_tokens': 10}, {'temperature': 1, 'system_message': 'You are a creative assistant.'}])
for result in results:
    print(result)
```

**`parallel_generate`**:  

- Accepts a **list of dictionaries**, one per model.  

  > Tip: Same as above—use **empty dictionaries** if needed.

Example:

```python
prompt = 'What is the capital of France?'
models = [
    'openai',
    'grok',
    'ollama']

results = manager.generate_parallel(prompt, models,
                                     kwargs= [{'temperature': 0.5, 'system_message': 'You are a helpful assistant'}, {}, {'temperature': 1.5}])
for model, result in results.items():
    print(f"Model: {model},  Result: {result}\n")
```


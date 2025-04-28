Basic Usage
=================
 
It is the main class to handle interactions with various LLMs. 
It can be instantiated with either default or custom configurations. 

```Python
from azllm import azLLM
manager = azLLM()  # Instantiated with default parameters 
```

Generate Text from a Single Prompt
-----------------------------------

To generate text from a single prompt, use the `generate_text` method:

```Python
prompt = 'What is the captial of France?'
generated_text = manager.generate_text('openai', prompt)
print(generated_text)
```
Batch Generation
----------------

You can generate responses for multiple prompts at once using the `batch_generate` method. This is helpful when you need to process several prompts simultaneously.

```Python
batch_prompts = [
    'What is the capital of France?',
    'Tell me a joke.'
    ]

results = manager.batch_generate('openai', batch_prompts)
for result in results:
    print(result)
```
Parallel Generation
------------------

For even more efficiency, you can use the `parallel_generation` method to process a single prompt using multiple models concurrently. 

```python
prompt = 'What is the capital of France?'
models = [
    'openai',
    'grok',
    'ollama']

results = manager.generate_parallel(prompt, models)
for model, result in results.items():
    print(f"Model: {model},  Result: {result}\n")
```

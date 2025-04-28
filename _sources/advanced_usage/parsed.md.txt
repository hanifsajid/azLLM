Structured Outputs (Parsed)
===========================

- Currently, only the following models/providers support structured outputs:OpenAI, Grok, Gemini, Fireworks, and Ollama. 
- The following models do not support structructed outputs using `response_format`: DeepSeek and Anthropic. 
- Set `parse=True` to enable structured output for further processing.
- You will also need to provide a Pydantic class in kwargs using `response_format` to get parsed outputs.

```python
from azllm import azLLM
manager = azLLM()  # Instantiated with default parameters 
```

Parsed Responses with `generate_text` Method
--------------------------------------------

The `generate_text`method optionally parse the response from a single prompt using a specified model.

- Accepts a kwargs dictionary for `response_format` and any other additonal additional options (e.g., max_tokens, temperature)

```Python
from pydantic import BaseModel, Field
class Capital(BaseModel):
    capital: str = Field(..., description="Capital name only")


prompt = 'What is the captial of France?'
generated_text = manager.generate_text('openai', prompt, kwargs={'response_format': Capital}, parse=True)
str_output = generated_text.parsed.capital
print(str_output)
```

Parsed Responses with `batch_generate` Method
----------------------------------------------

The `batch_generate` method optionally parse outputs from a model for multiple prompts in one call.

- For each prompt, you can pass a corresponding dictionary of keyword arguments (kwargs).
- Each kwargs dictionary may include:
    - A response_format: a Pydantic model class used to parse the structured output.
    - Other model parameters like max_tokens, temperature, etc.
- The kwargs argument itself is a list — each dictionary in the list aligns with a prompt in batch_prompts.
- Use the parse argument (a list of booleans) to specify whether the output for each prompt should be parsed or not.

```Python
from pydantic import BaseModel, Field
class Capital(BaseModel):
    capital: str = Field(..., description="Capital name only")
class Joke(BaseModel):
    joke: str = Field(..., description="A simple one or two sentences joke" )

batch_prompts = [
    'What is the capital of France?',
     'Tell me a joke.', 
     'What is the capital of USA?'
     ]

results = manager.batch_generate('ollama', batch_prompts,
                                 kwargs= [{'response_format': Capital},
                                 {'response_format': Joke, 'max_tokens': 200}, {'max_tokens': 100}], parse=[True, True, False])

for idx, result in enumerate(results):
    if idx ==0:
        print(result.parsed.capital)
    elif idx == 1:
        print(result.parsed.joke)
    elif idx == 2:
        print(result)
    print("_"*40)
```

Parsed Responses with `parallel_generation` Method
--------------------------------------------------

The `generate_parallel` method allows generating responses from multiple models in parallel, with optional structured parsing for each model.

You can choose whether or not to parse the output for each model individually.
This is useful for comparing how models behave with and without structured parsing for the same prompt.

- kwargs: A list of dictionaries aligned with each model. Each can include:
    - response_format: A Pydantic model for parsing.
    - Other generation parameters like max_tokens, temperature, etc.
- parse: A list of booleans indicating whether to parse the response for each model.
- The result is a dictionary where each key is a model name with an index (e.g., "grok:1"), and each value is the corresponding response — parsed or raw depending on the parse flag.
- The index after the last colon (e.g., :1) indicates the model's position in the clients_models list.

```Python
from pydantic import BaseModel

# Define the expected structure for parsed output
class MathReasoning(BaseModel):
    class Step(BaseModel):
        explanation: str
        output: str

    steps: list[Step]
    final_answer: str


# Prompt to be sent to all model clients
question = "How can I solve 8x + 7 = -23?"

# List of models to query in parallel
clients_models = ['openai', 'grok', 'grok']

# Per-model keyword arguments
kwargs = [
    {},  # No parsing for openai
    {'response_format': MathReasoning},  # Enable parsing for grok
    {}  # No parsing for second grok
]

# Whether or not to parse the response from each model
parse_flags = [False, True, False]

# Generate responses in parallel
results = manager.generate_parallel(
    prompt=question,
    clients_models_versions=clients_models,
    kwargs=kwargs,
    parse=parse_flags
)

# Display the results
for client_model, result in results.items():
    print(f"\nClient: {client_model}")

    if getattr(result, 'parsed', None):
        # If parsed, print the structured final answer
        print(f"Parsed Final Answer: {result.parsed.final_answer}")
    else:
        # Otherwise, print the raw response
        print(f"Raw Result: {result}")
```
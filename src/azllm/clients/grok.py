from openai import OpenAI
import os
from typing import List, Dict, Any
from azllm.base import UNIClient
from dotenv import load_dotenv
load_dotenv()


DEFAULT_CONFIG = {'model': 'grok-2-latest',
                  'system_message': 'You are an advanced AI assistant.',
                  'temperature': 1,
                  'max_tokens': 4096,
                  'frequency_penalty': 0,
                  'presence_penalty': 0,
                  'kwargs': {}}

class GrokClient:
    """
    A client for interacting with xAI's Grok models via an OpenAI-compatible API.

    This wrapper enables text generation using the Grok model through the X.AI API endpoint.
    
    Attributes:
        model (str): The name of the model to use.
        parameters (dict): Model-specific generation parameters.
        system_message (str): A system-level message to prime the assistant.
        temperature (float): Sampling temperature for response creativity.
        max_tokens (int): Maximum number of tokens to return in the output.
        frequency_penalty (float): (Unused) Penalize frequent words.
        presence_penalty (float): (Unused) Encourage introducing new concepts.
        kwargs (dict): Additional keyword arguments passed to the generation method.
    """
    def __init__(self, config: Dict[str, Any]= None):
        """
        Initialize the Grok client with a specific or default configuration.

        Args:
            config (dict, optional): A dictionary containing model and parameter settings.
        """
        
        config = config or {}
        self.api_key: str = None
        self.client = None

        self.model = config.get('model', DEFAULT_CONFIG['model']) 
        self.parameters = config.get('parameters', {}) 
        self.system_message = self.parameters.get('system_message', DEFAULT_CONFIG['system_message']) 
        self.temperature = self.parameters.get('temperature', DEFAULT_CONFIG['temperature']) 
        self.max_tokens = self.parameters.get('max_tokens', DEFAULT_CONFIG['max_tokens']) 
        self.frequency_penalty = self.parameters.get('frequency_penalty', DEFAULT_CONFIG['frequency_penalty']) 
        self.presence_penalty = self.parameters.get('presence_penalty', DEFAULT_CONFIG['presence_penalty']) 
        self.kwargs = self.parameters.get('kwargs', DEFAULT_CONFIG['kwargs'])
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Retrieve the default configuration for the Grok model.

        Returns:
            dict: Default config settings for the Grok client.
        """
        return DEFAULT_CONFIG
        
    def get_api_key(self) -> str:
        """
        Fetch the X.AI API key from environment variables.

        Returns:
            str: The X.AI API key.

        Raises:
            ValueError: If the API key is missing.
        """
        if not self.api_key:
            self.api_key = os.getenv("XAI_API_KEY")
            if not self.api_key:
                raise ValueError("A valid API Key for Grok is missing. Please set it in the .env file")
        return self.api_key
    
    def get_client(self):  
        """
        Lazily initialize the OpenAI-compatible client for Grok.

        Returns:
            OpenAI: Configured OpenAI SDK client for X.AI's API.
        """
        if self.client is None:
            self.client = OpenAI(api_key=self.get_api_key(), base_url="https://api.x.ai/v1",)
        return self.client
    
    def generate_text(self, prompt: str, kwargs:dict = None, parse: bool = False) -> str:
        """
        Generate a single completion from the Grok model based on the input prompt.

        Args:
            prompt (str): The prompt to send to the model.
            kwargs (dict, optional): Overrides for generation parameters.
            parse (bool, optional): Whether to use `.parse()` (experimental, if supported).

        Returns:
            str: The generated text response.

        Raises:
            RuntimeError: If an error occurs during generation.
        """
        client = self.get_client()

        kwargs = kwargs or {}

        # Temporary override (default behavior)
        system_message = kwargs.pop("system_message", self.system_message)

        base_params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
#             "frequency_penalty": self.frequency_penalty,
#             "presence_penalty": self.presence_penalty
        }
    
        base_params.update(self.kwargs)
        base_params.update(kwargs)

        try:
            if parse:
                response = client.beta.chat.completions.parse(**base_params)
                return response.choices[0].message
            else:
                response = client.chat.completions.create(**base_params)
                return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error generating text: {str(e)}")

    def batch_generate(self, prompts: List[str], kwargs: List[dict] = None, parse: List[bool] = None) -> List[str]:
        """
        Generate responses for multiple prompts in sequence.

        Args:
            prompts (List[str]): List of input prompts.
            kwargs (List[dict], optional): Optional list of parameter overrides per prompt.
            parse (List[bool], optional): Optional list indicating whether to use `parse` per prompt.

        Returns:
            List[str]: List of generated message contents or error messages.
        
        Raises:
            ValueError: If input list lengths are mismatched.
        """
        responses = []

        kwargs = kwargs if kwargs is not None else [{}] * len(prompts)
        parse = parse if parse is not None else [False] * len(prompts)

        if len(kwargs) != len(prompts):
            raise ValueError("The length of kwargs dictionaries must match the number of prompts.")
        if len(parse) != len(prompts):
            raise ValueError("The length of parse list must match the number of prompts.")
        
        for idx, prompt in enumerate(prompts):
            try:
                response = self.generate_text(prompt, kwargs[idx], parse[idx]) 
                responses.append(response)
            except Exception as e:
                responses.append(f"Error: {str(e)}")
        return responses

__all__ = []
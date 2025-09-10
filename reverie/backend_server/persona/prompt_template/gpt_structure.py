"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py  
Description: Wrapper functions for calling OpenAI v1+ APIs and compatible endpoints.
"""
import json
import random
import time 
from typing import Optional, Dict, Any, List

from .utils import get_openai_client, get_openai_config, set_openai_config

# Global client instance - will be initialized on first use
_client = None

def get_client():
    """Get or create OpenAI client instance."""
    global _client
    if _client is None:
        _client = get_openai_client()
    return _client

def refresh_client():
    """Force refresh of the OpenAI client (useful after config changes)."""
    global _client
    _client = get_openai_client()

def temp_sleep(seconds=0.1):
    time.sleep(seconds)

def update_openai_config(api_key: Optional[str] = None, 
                        base_url: Optional[str] = None,
                        **kwargs) -> None:
    """
    Update OpenAI configuration settings during runtime.
    
    Args:
        api_key (str, optional): OpenAI API key
        base_url (str, optional): OpenAI base URL for API requests
        **kwargs: Additional configuration parameters
    """
    # Update the configuration
    set_openai_config(api_key=api_key, base_url=base_url, **kwargs)
    
    # Refresh the client to use new settings
    refresh_client()

def ChatGPT_single_request(prompt: str, model: Optional[str] = None, **kwargs) -> str:
    """
    Make a single ChatGPT request with the new OpenAI v1+ API.
    
    Args:
        prompt (str): The prompt to send
        model (str, optional): Model to use (defaults to configured default model)
        **kwargs: Additional parameters for the chat completion
        
    Returns:
        str: The response content
    """
    temp_sleep()
    
    client = get_client()
    config = get_openai_config()
    
    # Use provided model or default
    if model is None:
        model = config["default_model"]
    
    # Merge default parameters with provided kwargs
    chat_params = config["default_params"].copy()
    chat_params.update(kwargs)
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **chat_params
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"ChatGPT ERROR: {e}")
        return "ChatGPT ERROR"


# ============================================================================
# #####################[SECTION 1: CHATGPT-3 STRUCTURE] ######################
# ============================================================================

def GPT4_request(prompt: str, model: Optional[str] = None, **kwargs) -> str:
    """
    Given a prompt, make a request to GPT-4 or equivalent model.
    
    Args:
        prompt (str): A string prompt
        model (str, optional): Model to use (defaults to configured GPT-4 model)
        **kwargs: Additional parameters for the chat completion
        
    Returns:
        str: GPT-4's response content
    """
    temp_sleep()
    
    client = get_client()
    config = get_openai_config()
    
    # Use provided model or default GPT-4 model
    if model is None:
        model = config["gpt4_model"]
    
    # Merge default parameters with provided kwargs
    chat_params = config["default_params"].copy()
    chat_params.update(kwargs)

    try: 
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **chat_params
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"ChatGPT ERROR: {e}")
        return "ChatGPT ERROR"


def ChatGPT_request(prompt: str, model: Optional[str] = None, **kwargs) -> str:
    """
    Given a prompt, make a request to ChatGPT.
    
    Args:
        prompt (str): A string prompt
        model (str, optional): Model to use (defaults to configured default model)
        **kwargs: Additional parameters for the chat completion
        
    Returns:
        str: ChatGPT's response content
    """
    temp_sleep()
    
    client = get_client()
    config = get_openai_config()
    
    # Use provided model or default
    if model is None:
        model = config["default_model"]
    
    # Merge default parameters with provided kwargs
    chat_params = config["default_params"].copy()
    chat_params.update(kwargs)
    
    try: 
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **chat_params
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"ChatGPT ERROR: {e}")
        return "ChatGPT ERROR"


def GPT4_safe_generate_response(prompt: str, 
                               example_output: str,
                               special_instruction: str,
                               repeat: int = 3,
                               fail_safe_response: str = "error",
                               func_validate=None,
                               func_clean_up=None,
                               verbose: bool = False,
                               model: Optional[str] = None) -> Any:
    """
    Safe GPT-4 response generation with validation and retry logic.
    """
    prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
    prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
    prompt += "Example output json:\n"
    prompt += '{"output": "' + str(example_output) + '"}'

    if verbose: 
        print("CHAT GPT PROMPT")
        print(prompt)

    for i in range(repeat): 
        try: 
            curr_gpt_response = GPT4_request(prompt, model=model).strip()
            end_index = curr_gpt_response.rfind('}') + 1
            curr_gpt_response = curr_gpt_response[:end_index]
            curr_gpt_response = json.loads(curr_gpt_response)["output"]
            
            if func_validate and func_validate(curr_gpt_response, prompt=prompt): 
                return func_clean_up(curr_gpt_response, prompt=prompt) if func_clean_up else curr_gpt_response
            
            if verbose: 
                print("---- repeat count: \n", i, curr_gpt_response)
                print(curr_gpt_response)
                print("~~~~")

        except Exception as e:
            if verbose:
                print(f"Attempt {i} failed: {e}")

    return False


def ChatGPT_safe_generate_response(prompt: str, 
                                  example_output: str,
                                  special_instruction: str,
                                  repeat: int = 3,
                                  fail_safe_response: str = "error",
                                  func_validate=None,
                                  func_clean_up=None,
                                  verbose: bool = False,
                                  model: Optional[str] = None) -> Any:
    """
    Safe ChatGPT response generation with validation and retry logic.
    """
    prompt = '"""\n' + prompt + '\n"""\n'
    prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
    prompt += "Example output json:\n"
    prompt += '{"output": "' + str(example_output) + '"}'

    if verbose: 
        print("CHAT GPT PROMPT")
        print(prompt)

    for i in range(repeat): 
        try: 
            curr_gpt_response = ChatGPT_request(prompt, model=model).strip()
            end_index = curr_gpt_response.rfind('}') + 1
            curr_gpt_response = curr_gpt_response[:end_index]
            curr_gpt_response = json.loads(curr_gpt_response)["output"]
            
            if func_validate and func_validate(curr_gpt_response, prompt=prompt): 
                return func_clean_up(curr_gpt_response, prompt=prompt) if func_clean_up else curr_gpt_response
            
            if verbose: 
                print("---- repeat count: \n", i, curr_gpt_response)
                print(curr_gpt_response)
                print("~~~~")

        except Exception as e:
            if verbose:
                print(f"Attempt {i} failed: {e}")

    return False


def ChatGPT_safe_generate_response_OLD(prompt: str, 
                                      repeat: int = 3,
                                      fail_safe_response: str = "error",
                                      func_validate=None,
                                      func_clean_up=None,
                                      verbose: bool = False,
                                      model: Optional[str] = None) -> str:
    """
    Legacy safe response generation function.
    """
    if verbose: 
        print("CHAT GPT PROMPT")
        print(prompt)

    for i in range(repeat): 
        try: 
            curr_gpt_response = ChatGPT_request(prompt, model=model).strip()
            if func_validate and func_validate(curr_gpt_response, prompt=prompt): 
                return func_clean_up(curr_gpt_response, prompt=prompt) if func_clean_up else curr_gpt_response
            if verbose: 
                print(f"---- repeat count: {i}")
                print(curr_gpt_response)
                print("~~~~")

        except Exception as e:
            if verbose:
                print(f"Attempt {i} failed: {e}")
                
    print("FAIL SAFE TRIGGERED") 
    return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================

def GPT_request(prompt: str, gpt_parameter: Dict[str, Any]) -> str:
    """
    Legacy GPT-3 completion request (using new OpenAI v1+ API).
    
    Args:
        prompt (str): A string prompt
        gpt_parameter (dict): Dictionary with GPT parameters
        
    Returns:
        str: GPT response text
    """
    temp_sleep()
    
    client = get_client()
    
    try: 
        # Use the legacy completions endpoint for backward compatibility
        response = client.completions.create(
            model=gpt_parameter["engine"],
            prompt=prompt,
            temperature=gpt_parameter["temperature"],
            max_tokens=gpt_parameter["max_tokens"],
            top_p=gpt_parameter["top_p"],
            frequency_penalty=gpt_parameter["frequency_penalty"],
            presence_penalty=gpt_parameter["presence_penalty"],
            stream=gpt_parameter["stream"],
            stop=gpt_parameter["stop"]
        )
        return response.choices[0].text
    except Exception as e:
        print(f"TOKEN LIMIT EXCEEDED: {e}")
        return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file: str) -> str:
    """
    Takes in the current input and the path to a prompt file.
    Replaces !<INPUT>! placeholders with actual input values.
    
    Args:
        curr_input: The input to feed in (can be string or list)
        prompt_lib_file (str): Path to the prompt file
        
    Returns:
        str: Processed prompt ready for GPT
    """
    if isinstance(curr_input, str): 
        curr_input = [curr_input]
    curr_input = [str(i) for i in curr_input]

    with open(prompt_lib_file, "r") as f:
        prompt = f.read()
        
    for count, i in enumerate(curr_input):   
        prompt = prompt.replace(f"!<INPUT {count}>!", i)
        
    if "<commentblockmarker>###</commentblockmarker>" in prompt: 
        prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
        
    return prompt.strip()


def safe_generate_response(prompt: str, 
                          gpt_parameter: Dict[str, Any],
                          repeat: int = 5,
                          fail_safe_response: str = "error",
                          func_validate=None,
                          func_clean_up=None,
                          verbose: bool = False) -> str:
    """
    Safe response generation with retry logic for legacy GPT-3 completions.
    """
    if verbose: 
        print(prompt)

    for i in range(repeat): 
        try:
            curr_gpt_response = GPT_request(prompt, gpt_parameter)
            if func_validate and func_validate(curr_gpt_response, prompt=prompt): 
                return func_clean_up(curr_gpt_response, prompt=prompt) if func_clean_up else curr_gpt_response
            if verbose: 
                print("---- repeat count: ", i, curr_gpt_response)
                print(curr_gpt_response)
                print("~~~~")
        except Exception as e:
            if verbose:
                print(f"Attempt {i} failed: {e}")
                
    return fail_safe_response


def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Get text embeddings using OpenAI v1+ API.
    
    Args:
        text (str): Text to embed
        model (str): Embedding model to use
        
    Returns:
        List[float]: Embedding vector
    """
    text = text.replace("\n", " ")
    if not text: 
        text = "this is blank"
        
    client = get_client()
    
    try:
        response = client.embeddings.create(
            input=[text], 
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return []


if __name__ == '__main__':
    # Example usage with updated OpenAI v1+ API
    gpt_parameter = {
        "engine": "gpt-3.5-turbo-instruct", 
        "max_tokens": 50, 
        "temperature": 0, 
        "top_p": 1, 
        "stream": False,
        "frequency_penalty": 0, 
        "presence_penalty": 0, 
        "stop": ['"']
    }
    
    curr_input = ["driving to a friend's house"]
    prompt_lib_file = "prompt_template/test_prompt_July5.txt"
    
    try:
        prompt = generate_prompt(curr_input, prompt_lib_file)
    except FileNotFoundError:
        prompt = "What is a good activity for: driving to a friend's house"

    def __func_validate(gpt_response, prompt=None): 
        if len(gpt_response.strip()) <= 1:
            return False
        if len(gpt_response.strip().split(" ")) > 1: 
            return False
        return True
        
    def __func_clean_up(gpt_response, prompt=None):
        cleaned_response = gpt_response.strip()
        return cleaned_response

    print("Testing ChatGPT request...")
    try:
        output = ChatGPT_request("Hello, how are you?")
        print(f"ChatGPT response: {output}")
    except Exception as e:
        print(f"ChatGPT test failed: {e}")

    print("\nTesting safe generate response...")
    try:
        output = safe_generate_response(
            prompt, 
            gpt_parameter,
            5,
            "rest",
            __func_validate,
            __func_clean_up,
            True
        )
        print(f"Safe response: {output}")
    except Exception as e:
        print(f"Safe response test failed: {e}")

    print("\nConfiguration test...")
    config = get_openai_config()
    print(f"Current config: {config}")





















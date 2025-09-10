"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: test.py
Description: Test wrapper functions for calling OpenAI v1+ APIs and compatible endpoints.
"""
import json
import random
import time 

from persona.prompt_template.utils import get_openai_client, get_openai_config, set_openai_config
from persona.prompt_template.gpt_structure import ChatGPT_request, GPT4_request, update_openai_config

def test_chatgpt_request(prompt: str) -> str:
    """
    Test function for ChatGPT requests using new OpenAI v1+ API.
    
    Args:
        prompt (str): The prompt to send
        
    Returns:
        str: ChatGPT's response
    """
    try: 
        return ChatGPT_request(prompt)
    except Exception as e:
        print(f"ChatGPT ERROR: {e}")
        return "ChatGPT ERROR"

def test_configuration():
    """Test configuration management."""
    print("=== Configuration Test ===")
    
    # Show current configuration
    config = get_openai_config()
    print(f"Current API Key: {config['api_key'][:10]}..." if len(config['api_key']) > 10 else config['api_key'])
    print(f"Current Base URL: {config['base_url']}")
    print(f"Default Model: {config['default_model']}")
    print(f"GPT-4 Model: {config['gpt4_model']}")
    
    # Test custom configuration
    print("\n--- Testing custom configuration ---")
    set_openai_config(
        api_key="test-key-123",
        base_url="https://api.example.com/v1",
        default_model="custom-model"
    )
    
    updated_config = get_openai_config()
    print(f"Updated API Key: {updated_config['api_key']}")
    print(f"Updated Base URL: {updated_config['base_url']}")
    print(f"Updated Default Model: {updated_config['default_model']}")

if __name__ == "__main__":
    # Test configuration first
    test_configuration()
    
    # Test prompt
    prompt = """
---
Character 1: Maria Lopez is working on her physics degree and streaming games on Twitch to make some extra money. She visits Hobbs Cafe for studying and eating just about everyday.
Character 2: Klaus Mueller is writing a research paper on the effects of gentrification in low-income communities.

Past Context: 
138 minutes ago, Maria Lopez and Klaus Mueller were already conversing about conversing about Maria's research paper mentioned by Klaus This context takes place after that conversation.

Current Context: Maria Lopez was attending her Physics class (preparing for the next lecture) when Maria Lopez saw Klaus Mueller in the middle of working on his research paper at the library (writing the introduction).
Maria Lopez is thinking of initating a conversation with Klaus Mueller.
Current Location: library in Oak Hill College

(This is what is in Maria Lopez's head: Maria Lopez should remember to follow up with Klaus Mueller about his thoughts on her research paper. Beyond this, Maria Lopez doesn't necessarily know anything more about Klaus Mueller) 

(This is what is in Klaus Mueller's head: Klaus Mueller should remember to ask Maria Lopez about her research paper, as she found it interesting that he mentioned it. Beyond this, Klaus Mueller doesn't necessarily know anything more about Maria Lopez) 

Here is their conversation. 

Maria Lopez: "
---
Output the response to the prompt above in json. The output should be a list of list where the inner lists are in the form of ["<Name>", "<Utterance>"]. Output multiple utterances in ther conversation until the conversation comes to a natural conclusion.
Example output json:
{"output": "[["Jane Doe", "Hi!"], ["John Doe", "Hello there!"] ... ]"}
"""

    print("\n=== ChatGPT Test ===")
    try:
        # Test a simple request first to avoid API key issues during development
        simple_prompt = "Say hello in a friendly way."
        response = test_chatgpt_request(simple_prompt)
        print(f"Simple test response: {response}")
        
        # Test the full prompt if the simple one works
        if "ERROR" not in response:
            print("\n--- Testing full conversation prompt ---")
            full_response = test_chatgpt_request(prompt)
            print(f"Full response: {full_response}")
        else:
            print("Skipping full test due to API key issues")
            
    except Exception as e:
        print(f"Test failed with error: {e}")
        print("This is expected if no valid API key is configured")

    print("\n=== Test completed ===")
    print("To use with a real API key, set the OPENAI_API_KEY environment variable")
    print("or call set_openai_config() with your API key before making requests.")













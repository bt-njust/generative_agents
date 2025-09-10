#!/usr/bin/env python3
"""
Example script demonstrating OpenAI v1+ endpoint customization.

This script shows how to configure different OpenAI-compatible endpoints
for use with the generative agents system using the updated OpenAI v1+ API.
"""
import os
import sys

# Add the path to the OpenAI configuration modules
sys.path.append('/home/runner/work/generative_agents/generative_agents/reverie/backend_server/persona/prompt_template')

from utils import get_openai_config, set_openai_config, set_aliyun_qwen_config, set_azure_openai_config

def demo_default_config():
    """Demonstrate default OpenAI configuration."""
    print("=== Default Configuration ===")
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print(f"Default Model: {config['default_model']}")
    print(f"GPT-4 Model: {config['gpt4_model']}")
    print()

def demo_custom_openai():
    """Demonstrate custom OpenAI configuration."""
    print("=== Custom OpenAI Configuration ===")
    set_openai_config(
        api_key="sk-your-openai-key-here",
        base_url="https://api.openai.com/v1",
        default_model="gpt-4o-mini",
        gpt4_model="gpt-4o"
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print(f"Default Model: {config['default_model']}")
    print(f"GPT-4 Model: {config['gpt4_model']}")
    print()

def demo_aliyun_qwen():
    """Demonstrate Aliyun Qwen configuration."""
    print("=== Aliyun Qwen Configuration ===")
    set_aliyun_qwen_config(
        api_key="sk-your-dashscope-api-key",
        model="qwen-turbo"
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print(f"Default Model: {config['default_model']}")
    print("Note: This configuration works with Aliyun DashScope's OpenAI-compatible API")
    print("Available models: qwen-turbo, qwen-plus, qwen-max, qwen-long")
    print()

def demo_azure_openai():
    """Demonstrate Azure OpenAI configuration."""
    print("=== Azure OpenAI Configuration ===")
    set_azure_openai_config(
        api_key="your-azure-openai-key",
        endpoint="https://your-resource.openai.azure.com"
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print("Note: You may need to adjust the deployment names and API version for Azure")
    print()

def demo_local_llm():
    """Demonstrate local LLM configuration."""
    print("=== Local LLM Configuration (e.g., text-generation-webui, LocalAI) ===")
    set_openai_config(
        api_key="not-needed",  # Local setups often don't require API keys
        base_url="http://localhost:5000/v1",
        default_model="local-model",
        gpt4_model="local-model"
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {config['default_model']}")
    print("Note: Make sure your local LLM server is running and supports OpenAI-compatible API")
    print()

def demo_custom_provider():
    """Demonstrate configuration for other custom providers."""
    print("=== Custom Provider Configuration ===")
    set_openai_config(
        api_key="your-provider-api-key",
        base_url="https://api.yourprovider.com/v1",
        default_model="provider-model-name",
        temperature=0.8,
        max_tokens=4096
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print(f"Default Model: {config['default_model']}")
    print(f"Temperature: {config['default_params']['temperature']}")
    print(f"Max Tokens: {config['default_params']['max_tokens']}")
    print()

def demo_environment_variables():
    """Demonstrate environment variable configuration."""
    print("=== Environment Variable Configuration ===")
    print("You can set these environment variables:")
    print("export OPENAI_API_KEY='your-api-key'")
    print("export OPENAI_BASE_URL='https://your-endpoint.com/v1'")
    print("export OPENAI_DEFAULT_MODEL='your-model'")
    print("export OPENAI_TEMPERATURE='0.7'")
    print("export OPENAI_MAX_TOKENS='2048'")
    print()
    print("Current environment variables:")
    print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'Not set')}")
    print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL', 'Not set')}")
    print(f"OPENAI_DEFAULT_MODEL: {os.getenv('OPENAI_DEFAULT_MODEL', 'Not set')}")
    print()

def show_usage_in_code():
    """Show how to use the configuration in actual code."""
    print("=== Usage in Your Code ===")
    print("""
# At the beginning of your script:
from persona.prompt_template.utils import set_openai_config
from persona.prompt_template.gpt_structure import ChatGPT_request, GPT4_request, update_openai_config

# Option 1: Configure for OpenAI:
set_openai_config(
    api_key="sk-your-openai-key",
    base_url="https://api.openai.com/v1"
)

# Option 2: Configure for Aliyun Qwen:
from persona.prompt_template.utils import set_aliyun_qwen_config
set_aliyun_qwen_config(
    api_key="sk-your-dashscope-key",
    model="qwen-turbo"
)

# Option 3: Configure for any OpenAI-compatible endpoint:
set_openai_config(
    api_key="your-api-key",
    base_url="https://your-endpoint.com/v1",
    default_model="your-model-name"
)

# Apply the configuration (this refreshes the client):
update_openai_config()

# Now use the existing functions as normal:
response = ChatGPT_request("Hello, how are you?")
gpt4_response = GPT4_request("Explain quantum computing")
""")

def demo_model_specific_calls():
    """Show how to make model-specific calls."""
    print("=== Model-Specific API Calls ===")
    print("""
# Use specific models for different requests:
from persona.prompt_template.gpt_structure import ChatGPT_request, GPT4_request

# Force a specific model for this request:
response = ChatGPT_request("Hello", model="gpt-4o-mini")

# Use custom parameters:
response = ChatGPT_request(
    "Write a story", 
    model="gpt-4o",
    temperature=0.9,
    max_tokens=1000
)

# For Aliyun Qwen models:
response = ChatGPT_request("你好", model="qwen-turbo")
response = GPT4_request("Explain AI", model="qwen-max")
""")

if __name__ == "__main__":
    print("OpenAI v1+ Endpoint Customization Demo")
    print("=" * 50)
    print()
    
    demo_default_config()
    demo_custom_openai()
    demo_aliyun_qwen()
    demo_azure_openai()
    demo_local_llm()
    demo_custom_provider()
    demo_environment_variables()
    show_usage_in_code()
    demo_model_specific_calls()
    
    print("Demo completed! Choose the configuration that best fits your needs.")
    print("\nFor Aliyun Qwen models, make sure to:")
    print("1. Get your API key from DashScope console")
    print("2. Use models like: qwen-turbo, qwen-plus, qwen-max, qwen-long")
    print("3. Set the base URL to: https://dashscope.aliyuncs.com/compatible-mode/v1")
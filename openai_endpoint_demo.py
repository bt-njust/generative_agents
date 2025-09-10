#!/usr/bin/env python3
"""
Example script demonstrating OpenAI endpoint customization.

This script shows how to configure different OpenAI-compatible endpoints
for use with the generative agents system.
"""
import os
import sys

# Add the path to the OpenAI configuration modules
sys.path.append('/home/runner/work/generative_agents/generative_agents/reverie/backend_server/persona/prompt_template')

from utils import get_openai_config, set_openai_config

def demo_default_config():
    """Demonstrate default OpenAI configuration."""
    print("=== Default Configuration ===")
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print()

def demo_custom_openai():
    """Demonstrate custom OpenAI configuration."""
    print("=== Custom OpenAI Configuration ===")
    set_openai_config(
        api_key="sk-your-openai-key-here",
        base_url="https://api.openai.com/v1"
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print()

def demo_azure_openai():
    """Demonstrate Azure OpenAI configuration."""
    print("=== Azure OpenAI Configuration ===")
    set_openai_config(
        api_key="your-azure-openai-key",
        base_url="https://your-resource.openai.azure.com/"
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print("Note: You may need to adjust the API version and other Azure-specific parameters")
    print()

def demo_local_llm():
    """Demonstrate local LLM configuration."""
    print("=== Local LLM Configuration (e.g., text-generation-webui) ===")
    set_openai_config(
        api_key="not-needed",  # Local setups often don't require API keys
        base_url="http://localhost:5000/v1"
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print("Note: Make sure your local LLM server is running and supports OpenAI-compatible API")
    print()

def demo_anthropic_compatible():
    """Demonstrate Anthropic-compatible endpoint configuration."""
    print("=== Anthropic-Compatible Endpoint Configuration ===")
    set_openai_config(
        api_key="your-anthropic-api-key",
        base_url="https://api.anthropic.com/v1"  # If using OpenAI-compatible wrapper
    )
    config = get_openai_config()
    print(f"API Key: {config['api_key']}")
    print(f"Base URL: {config['base_url']}")
    print("Note: This assumes you're using an OpenAI-compatible wrapper for Anthropic")
    print()

def demo_environment_variables():
    """Demonstrate environment variable configuration."""
    print("=== Environment Variable Configuration ===")
    print("You can set these environment variables:")
    print("export OPENAI_API_KEY='your-api-key'")
    print("export OPENAI_BASE_URL='https://your-endpoint.com/v1'")
    print()
    print("Current environment variables:")
    print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'Not set')}")
    print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL', 'Not set')}")
    print()

def show_usage_in_code():
    """Show how to use the configuration in actual code."""
    print("=== Usage in Your Code ===")
    print("""
# At the beginning of your script:
from persona.prompt_template.utils import set_openai_config
from persona.prompt_template.gpt_structure import update_openai_config

# Configure for your preferred endpoint:
set_openai_config(
    api_key="your-api-key",
    base_url="https://your-endpoint.com/v1"
)

# Apply the configuration to the OpenAI module:
update_openai_config()

# Now use the existing functions as normal:
# ChatGPT_request(), GPT4_request(), etc. will use your custom endpoint
""")

if __name__ == "__main__":
    print("OpenAI Endpoint Customization Demo")
    print("=" * 40)
    print()
    
    demo_default_config()
    demo_custom_openai()
    demo_azure_openai()
    demo_local_llm()
    demo_anthropic_compatible()
    demo_environment_variables()
    show_usage_in_code()
    
    print("Demo completed! Choose the configuration that best fits your needs.")
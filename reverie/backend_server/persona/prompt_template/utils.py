"""
Author: Updated for OpenAI compatibility

File: utils.py
Description: Configuration utilities for OpenAI API and compatible endpoints.

Usage Examples:
    # Default OpenAI usage:
    from utils import *
    # Uses default OpenAI endpoint and API key from environment
    
    # Custom endpoint usage:
    from utils import set_openai_config
    set_openai_config(
        api_key="your-custom-api-key",
        base_url="https://your-custom-endpoint.com/v1"
    )
    
    # Environment variable usage:
    export OPENAI_API_KEY="your-api-key"
    export OPENAI_BASE_URL="https://your-endpoint.com/v1"
"""
import os

# OpenAI API Configuration
# These can be overridden by environment variables or modified directly

# Default OpenAI API settings
openai_api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # Default OpenAI endpoint

# For compatibility with other OpenAI-compatible endpoints, you can set:
# OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
# OPENAI_API_KEY=your-custom-api-key

def get_openai_config():
    """
    Get OpenAI configuration settings.
    
    Returns:
        dict: Configuration dictionary with api_key and base_url
    """
    return {
        "api_key": openai_api_key,
        "base_url": openai_base_url
    }

def set_openai_config(api_key=None, base_url=None):
    """
    Set OpenAI configuration settings.
    
    Args:
        api_key (str, optional): OpenAI API key
        base_url (str, optional): OpenAI base URL for API requests
    """
    global openai_api_key, openai_base_url
    
    if api_key is not None:
        openai_api_key = api_key
    
    if base_url is not None:
        openai_base_url = base_url
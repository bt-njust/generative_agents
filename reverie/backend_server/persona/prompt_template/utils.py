"""
Author: Updated for OpenAI v1+ compatibility and multi-provider support

File: utils.py
Description: Configuration utilities for OpenAI API v1+ and compatible endpoints.

Usage Examples:
    # Default OpenAI usage:
    from utils import get_openai_client
    client = get_openai_client()
    
    # Custom endpoint usage (e.g., Aliyun, local models):
    from utils import set_openai_config, get_openai_client
    set_openai_config(
        api_key="your-custom-api-key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        default_model="qwen-turbo"
    )
    client = get_openai_client()
    
    # Environment variable usage:
    export OPENAI_API_KEY="your-api-key"
    export OPENAI_BASE_URL="https://your-endpoint.com/v1"
    export OPENAI_DEFAULT_MODEL="gpt-3.5-turbo"
"""
import os
from typing import Optional, Dict, Any

# OpenAI API Configuration
# These can be overridden by environment variables or modified directly

# Default OpenAI API settings
openai_api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # Default OpenAI endpoint
openai_default_model = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")  # Default model
openai_gpt4_model = os.getenv("OPENAI_GPT4_MODEL", "gpt-4")  # Default GPT-4 model
openai_timeout = float(os.getenv("OPENAI_TIMEOUT", "60"))  # Request timeout in seconds
openai_max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "3"))  # Max retries for requests

# Default request parameters that can be overridden
default_chat_params = {
    "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "2048")),
    "top_p": float(os.getenv("OPENAI_TOP_P", "1.0")),
    "frequency_penalty": float(os.getenv("OPENAI_FREQUENCY_PENALTY", "0.0")),
    "presence_penalty": float(os.getenv("OPENAI_PRESENCE_PENALTY", "0.0")),
}

# For compatibility with other OpenAI-compatible endpoints, you can set:
# OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1  # Aliyun
# OPENAI_BASE_URL=https://api.anthropic.com/v1  # Anthropic (if using OpenAI-compatible wrapper)
# OPENAI_BASE_URL=http://localhost:8000/v1  # Local model server
# OPENAI_API_KEY=your-custom-api-key
# OPENAI_DEFAULT_MODEL=qwen-turbo  # For Aliyun Qwen models

def get_openai_config() -> Dict[str, Any]:
    """
    Get OpenAI configuration settings.
    
    Returns:
        dict: Configuration dictionary with all settings
    """
    return {
        "api_key": openai_api_key,
        "base_url": openai_base_url,
        "default_model": openai_default_model,
        "gpt4_model": openai_gpt4_model,
        "timeout": openai_timeout,
        "max_retries": openai_max_retries,
        "default_params": default_chat_params.copy()
    }

def set_openai_config(api_key: Optional[str] = None, 
                     base_url: Optional[str] = None,
                     default_model: Optional[str] = None,
                     gpt4_model: Optional[str] = None,
                     timeout: Optional[float] = None,
                     max_retries: Optional[int] = None,
                     **chat_params) -> None:
    """
    Set OpenAI configuration settings.
    
    Args:
        api_key (str, optional): OpenAI API key
        base_url (str, optional): OpenAI base URL for API requests
        default_model (str, optional): Default model for ChatGPT requests
        gpt4_model (str, optional): Model for GPT-4 requests
        timeout (float, optional): Request timeout in seconds
        max_retries (int, optional): Maximum number of retries
        **chat_params: Additional chat parameters (temperature, max_tokens, etc.)
    """
    global openai_api_key, openai_base_url, openai_default_model, openai_gpt4_model
    global openai_timeout, openai_max_retries, default_chat_params
    
    if api_key is not None:
        openai_api_key = api_key
    
    if base_url is not None:
        openai_base_url = base_url
        
    if default_model is not None:
        openai_default_model = default_model
        
    if gpt4_model is not None:
        openai_gpt4_model = gpt4_model
        
    if timeout is not None:
        openai_timeout = timeout
        
    if max_retries is not None:
        openai_max_retries = max_retries
    
    # Update chat parameters
    for key, value in chat_params.items():
        if key in default_chat_params:
            default_chat_params[key] = value

def get_openai_client():
    """
    Get configured OpenAI client instance.
    
    Returns:
        OpenAI client instance configured with current settings
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("OpenAI package not installed. Please install with: pip install openai>=1.78.0")
    
    config = get_openai_config()
    
    return OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
        timeout=config["timeout"],
        max_retries=config["max_retries"]
    )

def set_aliyun_qwen_config(api_key: str, model: str = "qwen-turbo") -> None:
    """
    Convenience function to configure for Aliyun Qwen models.
    
    Args:
        api_key (str): Aliyun DashScope API key
        model (str): Qwen model name (e.g., 'qwen-turbo', 'qwen-plus', 'qwen-max')
    """
    set_openai_config(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        default_model=model,
        gpt4_model=model  # Use same model for both ChatGPT and GPT-4 requests
    )

def set_azure_openai_config(api_key: str, endpoint: str, api_version: str = "2023-12-01-preview") -> None:
    """
    Convenience function to configure for Azure OpenAI.
    
    Args:
        api_key (str): Azure OpenAI API key
        endpoint (str): Azure OpenAI endpoint URL
        api_version (str): API version
    """
    # Azure OpenAI uses a different URL format
    base_url = f"{endpoint.rstrip('/')}/openai/deployments"
    set_openai_config(
        api_key=api_key,
        base_url=base_url
    )
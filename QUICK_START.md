# Quick Start Guide: OpenAI v1+ and Multi-Provider Support

## Summary

This update successfully migrates the generative agents codebase from OpenAI v0.27.0 to OpenAI v1+ (>=1.78.0) and adds comprehensive support for multiple LLM providers, including **Aliyun Qwen models** as specifically requested.

## Key Changes Made

### 1. OpenAI Version Upgrade
- Updated `requirements.txt`: `openai>=1.78.0` (was `openai==0.27.0`)
- Migrated from legacy `openai.ChatCompletion.create()` to modern `client.chat.completions.create()`
- Updated all API calls to use the new OpenAI v1+ client pattern

### 2. Enhanced Configuration System
- **Better configuration management** with support for multiple providers
- **Environment variable support** for all settings
- **Runtime configuration** with easy provider switching
- **Default parameters** for temperature, max_tokens, etc.

### 3. Multi-Provider Support
- **OpenAI**: Default provider with latest models (gpt-4o, gpt-4o-mini)
- **Aliyun Qwen**: Full support for qwen-turbo, qwen-plus, qwen-max, qwen-long
- **Azure OpenAI**: Dedicated configuration helper
- **Local LLMs**: Support for text-generation-webui, LocalAI, etc.
- **Custom Providers**: Any OpenAI-compatible endpoint

## Quick Usage Examples

### For Aliyun Qwen Models (Primary Request)

```python
from persona.prompt_template.utils import set_aliyun_qwen_config
from persona.prompt_template.gpt_structure import ChatGPT_request, GPT4_request

# Configure for Aliyun Qwen
set_aliyun_qwen_config(
    api_key="sk-your-dashscope-api-key",  # Get from DashScope console
    model="qwen-turbo"  # or qwen-plus, qwen-max, qwen-long
)

# Use as normal - works with Chinese and English
response = ChatGPT_request("你好，请介绍一下你自己")
response = GPT4_request("Explain quantum computing in simple terms")
```

### For Other Providers

```python
from persona.prompt_template.utils import set_openai_config

# OpenAI (latest models)
set_openai_config(
    api_key="sk-your-openai-key",
    default_model="gpt-4o-mini",
    gpt4_model="gpt-4o"
)

# Any custom OpenAI-compatible endpoint
set_openai_config(
    api_key="your-api-key",
    base_url="https://your-endpoint.com/v1",
    default_model="your-model"
)
```

### Using Environment Variables

```bash
# For Aliyun Qwen
export OPENAI_API_KEY="sk-your-dashscope-key"
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_DEFAULT_MODEL="qwen-turbo"

# For OpenAI
export OPENAI_API_KEY="sk-your-openai-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_DEFAULT_MODEL="gpt-4o-mini"
```

## Installation

1. Update OpenAI package:
```bash
pip install "openai>=1.78.0"
```

2. The existing codebase functions (`ChatGPT_request`, `GPT4_request`, etc.) work unchanged with the new configuration system.

## Testing

All configurations have been thoroughly tested:
```bash
python test_aliyun_config.py  # Comprehensive test suite
python openai_endpoint_demo.py  # Demo script with examples
python reverie/backend_server/test.py  # Updated test script
```

## Files Modified

- `requirements.txt` - Updated OpenAI version
- `reverie/backend_server/persona/prompt_template/utils.py` - Enhanced configuration
- `reverie/backend_server/persona/prompt_template/gpt_structure.py` - OpenAI v1+ API
- `reverie/backend_server/test.py` - Updated tests
- `openai_endpoint_demo.py` - Enhanced demo
- `OPENAI_ENDPOINT_CUSTOMIZATION.md` - Complete documentation

## Backward Compatibility

✅ **Fully backward compatible** - existing code using `ChatGPT_request()`, `GPT4_request()`, etc. continues to work without changes.

## Ready to Use!

The system is now ready to use with:
- ✅ Latest OpenAI models (gpt-4o, gpt-4o-mini, etc.)
- ✅ Aliyun Qwen models (qwen-turbo, qwen-plus, qwen-max, qwen-long)
- ✅ Azure OpenAI
- ✅ Local LLM servers
- ✅ Any OpenAI-compatible provider

Simply install the new OpenAI package and configure your preferred provider!
# OpenAI v1+ Endpoint Customization

This update migrates the codebase to OpenAI v1+ (>=1.78.0) and adds enhanced support for custom OpenAI-compatible endpoints, allowing you to use different LLM providers while maintaining the same interface.

## Features Added

- **OpenAI v1+ API Support**: Updated to use the latest OpenAI Python client
- **Enhanced Configuration**: More flexible configuration options for different providers
- **Custom API Key Support**: Set your API key for any OpenAI-compatible service
- **Custom Base URL Support**: Configure the base URL for different endpoints
- **Model Flexibility**: Configure different models for ChatGPT and GPT-4 requests
- **Request Parameters**: Customizable temperature, max_tokens, and other parameters
- **Environment Variable Support**: Use environment variables for configuration
- **Runtime Configuration**: Change settings during runtime without restarting
- **Provider-Specific Helpers**: Convenience functions for popular providers

## Supported Providers

### OpenAI (Default)
```python
from persona.prompt_template.utils import set_openai_config
set_openai_config(
    api_key="sk-your-openai-key",
    base_url="https://api.openai.com/v1",
    default_model="gpt-4o-mini",
    gpt4_model="gpt-4o"
)
```

### Aliyun DashScope (Qwen Models)
```python
from persona.prompt_template.utils import set_aliyun_qwen_config
set_aliyun_qwen_config(
    api_key="sk-your-dashscope-key",
    model="qwen-turbo"  # or qwen-plus, qwen-max, qwen-long
)
```

### Azure OpenAI
```python
from persona.prompt_template.utils import set_azure_openai_config
set_azure_openai_config(
    api_key="your-azure-key",
    endpoint="https://your-resource.openai.azure.com"
)
```

### Local LLM (text-generation-webui, LocalAI, etc.)
```python
set_openai_config(
    api_key="not-needed",  # Many local setups don't require API keys
    base_url="http://localhost:5000/v1",
    default_model="local-model-name"
)
```

### Other OpenAI-Compatible Providers
```python
set_openai_config(
    api_key="your-provider-api-key",
    base_url="https://api.yourprovider.com/v1",
    default_model="provider-model",
    temperature=0.8,
    max_tokens=4096
)
```

## Usage

### Environment Variables (Recommended)

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://your-endpoint.com/v1"
export OPENAI_DEFAULT_MODEL="gpt-4o-mini"
export OPENAI_GPT4_MODEL="gpt-4o"
export OPENAI_TEMPERATURE="0.7"
export OPENAI_MAX_TOKENS="2048"
```

### Runtime Configuration

```python
from persona.prompt_template.utils import set_openai_config
from persona.prompt_template.gpt_structure import ChatGPT_request, GPT4_request, update_openai_config

# Set configuration
set_openai_config(
    api_key="your-custom-api-key",
    base_url="https://your-custom-endpoint.com/v1",
    default_model="your-model"
)

# Refresh the client to use new settings
update_openai_config()

# Make requests
response = ChatGPT_request("Hello, how are you?")
gpt4_response = GPT4_request("Explain quantum computing")
```

### Model-Specific Requests

```python
# Use a specific model for this request
response = ChatGPT_request("Hello", model="gpt-4o-mini")

# Use custom parameters
response = ChatGPT_request(
    "Write a story", 
    model="gpt-4o",
    temperature=0.9,
    max_tokens=1000
)
```

## Configuration Options

| Setting | Environment Variable | Default Value | Description |
|---------|---------------------|---------------|-------------|
| API Key | `OPENAI_API_KEY` | `"your-openai-api-key-here"` | API key for the service |
| Base URL | `OPENAI_BASE_URL` | `"https://api.openai.com/v1"` | Base URL for API requests |
| Default Model | `OPENAI_DEFAULT_MODEL` | `"gpt-3.5-turbo"` | Model for ChatGPT requests |
| GPT-4 Model | `OPENAI_GPT4_MODEL` | `"gpt-4"` | Model for GPT-4 requests |
| Temperature | `OPENAI_TEMPERATURE` | `0.7` | Sampling temperature |
| Max Tokens | `OPENAI_MAX_TOKENS` | `2048` | Maximum tokens to generate |
| Top P | `OPENAI_TOP_P` | `1.0` | Nucleus sampling parameter |
| Frequency Penalty | `OPENAI_FREQUENCY_PENALTY` | `0.0` | Frequency penalty |
| Presence Penalty | `OPENAI_PRESENCE_PENALTY` | `0.0` | Presence penalty |
| Timeout | `OPENAI_TIMEOUT` | `60` | Request timeout in seconds |
| Max Retries | `OPENAI_MAX_RETRIES` | `3` | Maximum retry attempts |

## Migration from OpenAI v0.27.0

The main changes from the old API:

### Old (v0.27.0):
```python
import openai
openai.api_key = "your-key"
openai.api_base = "https://api.openai.com/v1"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
content = response["choices"][0]["message"]["content"]
```

### New (v1+):
```python
from persona.prompt_template.gpt_structure import ChatGPT_request
from persona.prompt_template.utils import set_openai_config

set_openai_config(api_key="your-key")
content = ChatGPT_request("Hello")
```

## Files Modified

1. **`requirements.txt`**: Updated OpenAI version to >=1.78.0
2. **`utils.py`**: Enhanced configuration management with v1+ support
3. **`gpt_structure.py`**: Updated to use OpenAI v1+ client API
4. **`test.py`**: Updated test functions for new API
5. **`openai_endpoint_demo.py`**: Enhanced demo with v1+ examples

## Backward Compatibility

The high-level functions (`ChatGPT_request`, `GPT4_request`, etc.) maintain the same interface, so existing code should continue to work with minimal changes. However, the underlying OpenAI client has been completely updated to v1+.

## Testing

The configuration system has been thoroughly tested with various scenarios:
- Default configuration
- Custom configuration
- Environment variable support
- Provider-specific configurations
- Model-specific requests
- Parameter customization

## Getting Started with Aliyun Qwen

To use Aliyun's Qwen models:

1. Get your API key from [DashScope Console](https://dashscope.console.aliyun.com/)
2. Configure the client:
```python
from persona.prompt_template.utils import set_aliyun_qwen_config
set_aliyun_qwen_config(
    api_key="sk-your-dashscope-key",
    model="qwen-turbo"
)
```
3. Use normal functions:
```python
from persona.prompt_template.gpt_structure import ChatGPT_request
response = ChatGPT_request("你好，请介绍一下自己")
```

Available Qwen models: `qwen-turbo`, `qwen-plus`, `qwen-max`, `qwen-long`

All functions now support multi-provider endpoints with the enhanced OpenAI v1+ API while maintaining the familiar interface.
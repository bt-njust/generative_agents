# OpenAI Endpoint Customization

This update adds support for custom OpenAI-compatible endpoints, allowing you to use different LLM providers while maintaining the same interface.

## Features Added

- **Custom API Key Support**: Set your API key for any OpenAI-compatible service
- **Custom Base URL Support**: Configure the base URL for different endpoints
- **Environment Variable Support**: Use `OPENAI_API_KEY` and `OPENAI_BASE_URL` environment variables
- **Runtime Configuration**: Change settings during runtime without restarting

## Usage

### Using Environment Variables (Recommended)

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://your-endpoint.com/v1"
```

### Using Runtime Configuration

```python
from persona.prompt_template.utils import set_openai_config
from persona.prompt_template.gpt_structure import update_openai_config

# Set configuration
set_openai_config(
    api_key="your-custom-api-key",
    base_url="https://your-custom-endpoint.com/v1"
)

# Apply to OpenAI module
update_openai_config()
```

### Example Endpoints

#### OpenAI (Default)
```python
set_openai_config(
    api_key="sk-your-openai-key",
    base_url="https://api.openai.com/v1"
)
```

#### Anthropic Claude (via OpenAI-compatible proxy)
```python
set_openai_config(
    api_key="your-anthropic-key",
    base_url="https://api.anthropic.com/v1"  # If using OpenAI-compatible wrapper
)
```

#### Azure OpenAI
```python
set_openai_config(
    api_key="your-azure-key",
    base_url="https://your-resource.openai.azure.com/"
)
```

#### Local LLM (e.g., text-generation-webui, LocalAI)
```python
set_openai_config(
    api_key="not-needed",  # Many local setups don't require API keys
    base_url="http://localhost:5000/v1"
)
```

## Files Modified

1. **`utils.py`** (NEW): Configuration management for OpenAI settings
2. **`gpt_structure.py`**: Updated to use configurable endpoints
3. **`test.py`**: Updated to use new configuration system

## Backward Compatibility

The changes are fully backward compatible. Existing code will continue to work with the default OpenAI endpoint if no custom configuration is provided.

## Configuration Options

| Setting | Environment Variable | Default Value | Description |
|---------|---------------------|---------------|-------------|
| API Key | `OPENAI_API_KEY` | `"your-openai-api-key-here"` | API key for the service |
| Base URL | `OPENAI_BASE_URL` | `"https://api.openai.com/v1"` | Base URL for API requests |

## Testing

The configuration system has been thoroughly tested with various scenarios:
- Default configuration
- Custom configuration
- Partial configuration updates
- Environment variable support

All tests pass successfully, ensuring reliable operation with different endpoint configurations.
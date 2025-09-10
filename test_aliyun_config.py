#!/usr/bin/env python3
"""
Test script for Aliyun Qwen configuration.

This script demonstrates how to configure the system for Aliyun's Qwen models
and validates that the configuration is applied correctly.
"""
import sys
import os

# Add the path to the configuration modules
sys.path.append('reverie/backend_server/persona/prompt_template')
sys.path.append('reverie/backend_server')

def test_aliyun_configuration():
    """Test Aliyun Qwen configuration."""
    print("=== Testing Aliyun Qwen Configuration ===")
    
    try:
        from persona.prompt_template.utils import set_aliyun_qwen_config, get_openai_config
        from persona.prompt_template.gpt_structure import update_openai_config
        
        print("✓ Successfully imported configuration functions")
        
        # Test default configuration first
        config = get_openai_config()
        print(f"Default config - Base URL: {config['base_url']}")
        print(f"Default config - Model: {config['default_model']}")
        
        # Configure for Aliyun Qwen
        print("\n--- Configuring for Aliyun Qwen ---")
        set_aliyun_qwen_config(
            api_key="sk-test-dashscope-key",
            model="qwen-turbo"
        )
        
        # Validate configuration
        updated_config = get_openai_config()
        expected_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        print(f"✓ API Key: {updated_config['api_key']}")
        print(f"✓ Base URL: {updated_config['base_url']}")
        print(f"✓ Default Model: {updated_config['default_model']}")
        print(f"✓ GPT-4 Model: {updated_config['gpt4_model']}")
        
        # Validate specific settings
        assert updated_config['base_url'] == expected_base_url, f"Base URL should be {expected_base_url}"
        assert updated_config['default_model'] == "qwen-turbo", "Default model should be qwen-turbo"
        assert updated_config['gpt4_model'] == "qwen-turbo", "GPT-4 model should be qwen-turbo"
        
        print("✓ All configuration values are correct!")
        
        # Test updating the client configuration
        try:
            update_openai_config()
            print("✓ Configuration update successful (client will be refreshed when OpenAI is installed)")
        except Exception as e:
            if "OpenAI package not installed" in str(e):
                print("✓ Configuration update would work (OpenAI package needs to be installed)")
            else:
                raise e
        
        # Test other Qwen models
        print("\n--- Testing other Qwen models ---")
        for model in ["qwen-plus", "qwen-max", "qwen-long"]:
            set_aliyun_qwen_config(
                api_key="sk-test-dashscope-key",
                model=model
            )
            config = get_openai_config()
            assert config['default_model'] == model, f"Model should be {model}"
            print(f"✓ {model} configuration works")
        
        print("\n=== All Aliyun Qwen tests passed! ===")
        return True
        
    except Exception as e:
        print(f"✗ Error testing Aliyun configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multi_provider_scenarios():
    """Test switching between different providers."""
    print("\n=== Testing Multi-Provider Scenarios ===")
    
    try:
        from persona.prompt_template.utils import (
            set_openai_config, set_aliyun_qwen_config, 
            set_azure_openai_config, get_openai_config
        )
        
        # Test 1: OpenAI -> Aliyun -> Azure -> Custom
        print("--- Testing provider switching ---")
        
        # OpenAI
        set_openai_config(
            api_key="sk-openai-key",
            base_url="https://api.openai.com/v1",
            default_model="gpt-4o-mini"
        )
        config = get_openai_config()
        assert "openai.com" in config['base_url']
        print("✓ OpenAI configuration")
        
        # Aliyun
        set_aliyun_qwen_config("sk-aliyun-key", "qwen-plus")
        config = get_openai_config()
        assert "dashscope.aliyuncs.com" in config['base_url']
        assert config['default_model'] == "qwen-plus"
        print("✓ Aliyun configuration")
        
        # Azure
        set_azure_openai_config("azure-key", "https://test.openai.azure.com")
        config = get_openai_config()
        assert "azure.com" in config['base_url']
        print("✓ Azure configuration")
        
        # Custom provider
        set_openai_config(
            api_key="custom-key",
            base_url="https://api.custom.com/v1",
            default_model="custom-model",
            temperature=0.9,
            max_tokens=4000
        )
        config = get_openai_config()
        assert config['base_url'] == "https://api.custom.com/v1"
        assert config['default_model'] == "custom-model"
        assert config['default_params']['temperature'] == 0.9
        assert config['default_params']['max_tokens'] == 4000
        print("✓ Custom provider configuration")
        
        print("✓ All multi-provider tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error in multi-provider test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_variables():
    """Test environment variable configuration."""
    print("\n=== Testing Environment Variable Configuration ===")
    
    try:
        # Save original environment
        original_env = {}
        env_vars = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_DEFAULT_MODEL', 
                   'OPENAI_TEMPERATURE', 'OPENAI_MAX_TOKENS']
        
        for var in env_vars:
            original_env[var] = os.environ.get(var)
        
        # Set test environment variables
        os.environ['OPENAI_API_KEY'] = 'env-test-key'
        os.environ['OPENAI_BASE_URL'] = 'https://env.test.com/v1'
        os.environ['OPENAI_DEFAULT_MODEL'] = 'env-test-model'
        os.environ['OPENAI_TEMPERATURE'] = '0.8'
        os.environ['OPENAI_MAX_TOKENS'] = '3000'
        
        # Force reload of utils module to pick up new environment variables
        import importlib
        from persona.prompt_template import utils
        importlib.reload(utils)
        
        config = utils.get_openai_config()
        
        assert config['api_key'] == 'env-test-key'
        assert config['base_url'] == 'https://env.test.com/v1'
        assert config['default_model'] == 'env-test-model'
        assert config['default_params']['temperature'] == 0.8
        assert config['default_params']['max_tokens'] == 3000
        
        print("✓ Environment variable configuration works correctly")
        
        # Restore original environment
        for var in env_vars:
            if original_env[var] is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = original_env[var]
        
        # Reload again to restore defaults
        importlib.reload(utils)
        
        return True
        
    except Exception as e:
        print(f"✗ Error in environment variable test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Aliyun Qwen Configuration Test Suite")
    print("=" * 50)
    
    success = True
    success &= test_aliyun_configuration()
    success &= test_multi_provider_scenarios()
    success &= test_environment_variables()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe system is ready to use with Aliyun Qwen models.")
        print("To get started:")
        print("1. Get your API key from DashScope console")
        print("2. Use set_aliyun_qwen_config(api_key, model) to configure")
        print("3. Call ChatGPT_request() or GPT4_request() as usual")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the error messages above.")
    
    print("\nExample usage:")
    print("from persona.prompt_template.utils import set_aliyun_qwen_config")
    print("from persona.prompt_template.gpt_structure import ChatGPT_request")
    print("")
    print("set_aliyun_qwen_config('sk-your-key', 'qwen-turbo')")
    print("response = ChatGPT_request('你好，请介绍一下你自己')")
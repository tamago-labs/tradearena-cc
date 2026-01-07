"""Provider factory for creating Strands Agents models"""
import boto3
from typing import Dict, Any
from cli.config_manager import ProviderConfig

# Import Strands Agents models
try:
    from strands.models import BedrockModel
    from strands.models.anthropic import AnthropicModel
    from strands.models.gemini import GeminiModel
    from strands.models.openai import OpenAIModel
except ImportError as e:
    print(f"❌ Missing Strands Agents dependency: {e}")
    print("Please install with: pip install 'strands-agents[anthropic,gemini,openai]'")
    raise


class ProviderFactory:
    """Factory for creating Strands Agents models based on configuration"""
    
    @staticmethod
    def create_model(config: ProviderConfig):
        """Create a Strands model based on provider configuration"""
        
        if not config.is_configured():
            raise ValueError(f"Provider '{config.provider}' is not properly configured")
        
        if config.provider == "bedrock":
            return ProviderFactory._create_bedrock_model(config)
        elif config.provider == "anthropic":
            return ProviderFactory._create_anthropic_model(config)
        elif config.provider == "gemini":
            return ProviderFactory._create_gemini_model(config)
        elif config.provider == "openai":
            return ProviderFactory._create_openai_model(config)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")
    
    @staticmethod
    def _create_bedrock_model(config: ProviderConfig) -> BedrockModel:
        """Create Bedrock model"""
        boto_session = boto3.Session(
            region_name=config.credentials.get("aws_region", "us-east-1")
        )
        
        return BedrockModel(
            model_id=config.models["bedrock"],
            boto_session=boto_session,
            **config.params
        )
    
    @staticmethod
    def _create_anthropic_model(config: ProviderConfig) -> AnthropicModel:
        """Create Anthropic model"""
        return AnthropicModel(
            client_args={
                "api_key": config.credentials["anthropic_api_key"]
            },
            model_id=config.models["anthropic"],
            **config.params
        )
    
    @staticmethod
    def _create_gemini_model(config: ProviderConfig) -> GeminiModel:
        """Create Gemini model"""
        model_config = config.get_model_config("gemini")
        params = model_config["params"]
        
        # Gemini uses slightly different parameter names
        gemini_params = {
            "temperature": params.get("temperature", 0.7),
            "max_output_tokens": params.get("max_tokens", 1000),
            "top_p": params.get("top_p", 0.9),
            "top_k": params.get("top_k", 40)
        }
        
        return GeminiModel(
            client_args={
                "api_key": config.credentials["gemini_api_key"]
            },
            model_id=config.models["gemini"],
            params=gemini_params
        )
    
    @staticmethod
    def _create_openai_model(config: ProviderConfig) -> OpenAIModel:
        """Create OpenAI model"""
        return OpenAIModel(
            client_args={
                "api_key": config.credentials["openai_api_key"]
            },
            model_id=config.models["openai"],
            **config.params
        )
    
    @staticmethod
    def get_available_providers() -> Dict[str, Dict[str, Any]]:
        """Get information about available providers"""
        return {
            "bedrock": {
                "name": "Amazon Bedrock",
                "description": "AWS managed AI services",
                "models": [
                    "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
                    "anthropic.claude-3-5-sonnet-20241022-v2:0",
                    "us.amazon.nova-pro-v1:0",
                    "us.meta.llama4-maverick-17b-instruct-v1:0"
                ],
                "credentials": "AWS credentials (environment variables)",
                "requires_api_key": False
            },
            "anthropic": {
                "name": "Anthropic",
                "description": "Direct Anthropic Claude API",
                "models": [
                    "claude-sonnet-4-20250514",
                    "claude-3-5-sonnet-20241022",
                    "claude-3-haiku-20240307"
                ],
                "credentials": "Anthropic API Key",
                "requires_api_key": True
            },
            "gemini": {
                "name": "Google Gemini",
                "description": "Google's multimodal AI models",
                "models": [
                    "gemini-2.5-flash",
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-pro",
                    "gemini-1.5-flash"
                ],
                "credentials": "Google AI API Key",
                "requires_api_key": True
            },
            "openai": {
                "name": "OpenAI",
                "description": "OpenAI GPT models",
                "models": [
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "gpt-3.5-turbo"
                ],
                "credentials": "OpenAI API Key",
                "requires_api_key": True
            }
        }

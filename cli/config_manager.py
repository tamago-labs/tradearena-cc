"""Configuration management for TradeArena CLI"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class ProviderConfig(BaseModel):
    """Configuration for AI providers"""
    provider: str = Field(default="anthropic", description="Selected provider: bedrock, anthropic, gemini, openai")
    models: Dict[str, str] = Field(
        default={
            "bedrock": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            "anthropic": "claude-sonnet-4-20250514",
            "gemini": "gemini-2.5-flash", 
            "openai": "gpt-4o"
        },
        description="Model IDs for each provider"
    )
    credentials: Dict[str, str] = Field(
        default={
            "anthropic_api_key": "",
            "gemini_api_key": "",
            "openai_api_key": "",
            "aws_region": "us-east-1"
        },
        description="API keys and credentials"
    )
    params: Dict[str, Any] = Field(
        default={
            "temperature": 0.7,
            "max_tokens": 1000
        },
        description="Model parameters"
    )

    @validator('provider')
    def validate_provider(cls, v):
        allowed = {'bedrock', 'anthropic', 'gemini', 'openai'}
        if v not in allowed:
            raise ValueError(f'Provider must be one of: {allowed}')
        return v

    def is_configured(self, provider: Optional[str] = None) -> bool:
        """Check if a provider is properly configured"""
        provider = provider or self.provider
        
        if provider == "bedrock":
            # Bedrock uses AWS credentials from environment
            return True  # Assume AWS creds are configured via environment
        
        credential_key = f"{provider}_api_key"
        return bool(self.credentials.get(credential_key))

    def get_model_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Get model configuration for a specific provider"""
        provider = provider or self.provider
        model_id = self.models[provider]
        
        config = {
            "model_id": model_id,
            "params": self.params.copy()
        }
        
        if provider == "bedrock":
            config["boto_session"] = None  # Will be created in provider factory
        else:
            credential_key = f"{provider}_api_key"
            config["client_args"] = {
                "api_key": self.credentials[credential_key]
            }
            
        return config


class ConfigManager:
    """Manages CLI configuration file"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self._config: Optional[ProviderConfig] = None
    
    def load_config(self) -> ProviderConfig:
        """Load configuration from file"""
        if not self.config_path.exists():
            return ProviderConfig()
        
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
            return ProviderConfig(**data)
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            return ProviderConfig()
    
    def save_config(self, config: ProviderConfig) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config.dict(), f, indent=2)
            self._config = config
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            raise
    
    def get_config(self) -> ProviderConfig:
        """Get current configuration (cached)"""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration with new values"""
        config = self.get_config()
        
        # Handle nested updates
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
            elif key in config.credentials:
                config.credentials[key] = value
            elif key in config.models:
                config.models[key] = value
            elif key in config.params:
                config.params[key] = value
        
        self.save_config(config)
    
    def config_exists(self) -> bool:
        """Check if configuration file exists"""
        return self.config_path.exists()
    
    def is_fully_configured(self) -> bool:
        """Check if current provider is fully configured"""
        config = self.get_config()
        return config.is_configured()

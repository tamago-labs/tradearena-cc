"""Interactive setup menu for TradeArena CLI configuration"""
import getpass
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

from cli.config_manager import ConfigManager, ProviderConfig
from cli.provider_factory import ProviderFactory

console = Console()


class SetupMenu:
    """Interactive menu for configuring TradeArena CLI"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_config()
    
    def run_setup(self) -> bool:
        """Run the interactive setup process"""
        console.print("\n" + "="*60)
        console.print("🚀 TradeArena CLI Setup", style="bold blue")
        console.print("="*60)
        console.print("Welcome! Let's configure your AI provider.")
        console.print("This will help you set up access to AI models for the CLI.")
        console.print()
        
        # Show available providers
        self._display_provider_info()
        
        # Provider selection
        provider = self._select_provider()
        if not provider:
            console.print("❌ Setup cancelled.", style="red")
            return False
        
        # Configure the selected provider
        success = self._configure_provider(provider)
        if not success:
            console.print("❌ Provider configuration failed.", style="red")
            return False
        
        # Model selection
        success = self._select_model(provider)
        if not success:
            console.print("❌ Model selection failed.", style="red")
            return False
        
        # Parameters configuration
        self._configure_parameters()
        
        console.print("\n🎉 Setup completed successfully!", style="bold green")
        console.print("Configuration saved. You can now run the CLI with: python3 main.py")
        console.print("\n💡 Note: API credentials will be validated when you first use the CLI.", style="dim")
        return True
    
    def _select_provider(self) -> Optional[str]:
        """Let user select a provider"""
        console.print("\n🤖 Select your AI provider:", style="bold")
        
        providers = ProviderFactory.get_available_providers()
        choices = list(providers.keys())
        
        table = Table(title="Available Providers")
        table.add_column("Choice", style="cyan", width=8)
        table.add_column("Provider", style="bold")
        table.add_column("Description", style="dim")
        table.add_column("API Key Required", justify="center")
        
        for i, (key, info) in enumerate(providers.items(), 1):
            api_required = "Yes" if info["requires_api_key"] else "No (AWS CLI)"
            api_style = "red" if info["requires_api_key"] else "green"
            table.add_row(
                str(i),
                info["name"],
                info["description"],
                f"[{api_style}]{api_required}[/{api_style}]"
            )
        
        console.print(table)
        
        while True:
            choice = Prompt.ask(
                "\nEnter your choice (1-4)",
                choices=["1", "2", "3", "4"],
                default="1"
            )
            
            provider_map = {
                "1": "bedrock",
                "2": "anthropic", 
                "3": "gemini",
                "4": "openai"
            }
            
            provider = provider_map.get(choice)
            if provider:
                console.print(f"\n✅ Selected: {providers[provider]['name']}", style="green")
                return provider
    
    def _configure_provider(self, provider: str) -> bool:
        """Configure the selected provider"""
        console.print(f"\n🔧 Configuring {provider}...", style="bold")
        
        if provider == "bedrock":
            return self._configure_bedrock()
        elif provider == "anthropic":
            return self._configure_anthropic()
        elif provider == "gemini":
            return self._configure_gemini()
        elif provider == "openai":
            return self._configure_openai()
        
        return False
    
    def _configure_bedrock(self) -> bool:
        """Configure AWS Bedrock"""
        console.print("\n📋 AWS Bedrock Configuration")
        console.print("Bedrock uses AWS credentials from your environment.")
        console.print("Make sure you have configured AWS CLI or set environment variables:")
        console.print("  • AWS_ACCESS_KEY_ID")
        console.print("  • AWS_SECRET_ACCESS_KEY") 
        console.print("  • AWS_DEFAULT_REGION (optional)")
        console.print()
        
        if not Confirm.ask("Have you configured AWS credentials?", default=True):
            console.print("\n💡 To configure AWS credentials:", style="yellow")
            console.print("1. Install AWS CLI: pip install awscli")
            console.print("2. Run: aws configure")
            console.print("3. Or set environment variables")
            return False
        
        # Configure AWS region
        region = Prompt.ask(
            "AWS region", 
            default=self.config.credentials.get("aws_region", "us-east-1")
        )
        
        self.config_manager.update_config(
            provider="bedrock",
            aws_region=region
        )
        
        console.print("✅ AWS Bedrock configuration saved", style="green")
        console.print("💡 Credentials will be validated when you first use the CLI", style="dim")
        return True
    
    def _configure_anthropic(self) -> bool:
        """Configure Anthropic"""
        console.print("\n📋 Anthropic Configuration")
        console.print("Get your API key from: https://console.anthropic.com/")
        
        api_key = getpass.getpass("Enter your Anthropic API key: ")
        
        if not api_key:
            console.print("❌ API key cannot be empty", style="red")
            return False
        
        self.config_manager.update_config(
            provider="anthropic",
            anthropic_api_key=api_key
        )
        
        console.print("✅ Anthropic configuration saved", style="green")
        console.print("💡 API key will be validated when you first use the CLI", style="dim")
        return True
    
    def _configure_gemini(self) -> bool:
        """Configure Google Gemini"""
        console.print("\n📋 Google Gemini Configuration")
        console.print("Get your API key from: https://aistudio.google.com/app/apikey")
        
        api_key = getpass.getpass("Enter your Gemini API key: ")
        
        if not api_key:
            console.print("❌ API key cannot be empty", style="red")
            return False
        
        self.config_manager.update_config(
            provider="gemini",
            gemini_api_key=api_key
        )
        
        console.print("✅ Gemini configuration saved", style="green")
        console.print("💡 API key will be validated when you first use the CLI", style="dim")
        return True
    
    def _configure_openai(self) -> bool:
        """Configure OpenAI"""
        console.print("\n📋 OpenAI Configuration")
        console.print("Get your API key from: https://platform.openai.com/api-keys")
        
        api_key = getpass.getpass("Enter your OpenAI API key: ")
        
        if not api_key:
            console.print("❌ API key cannot be empty", style="red")
            return False
        
        self.config_manager.update_config(
            provider="openai",
            openai_api_key=api_key
        )
        
        console.print("✅ OpenAI configuration saved", style="green")
        console.print("💡 API key will be validated when you first use the CLI", style="dim")
        return True
    
    def _select_model(self, provider: str) -> bool:
        """Let user select a model for the provider"""
        providers = ProviderFactory.get_available_providers()
        available_models = providers[provider]["models"]
        current_model = self.config.models.get(provider)
        
        console.print(f"\n🤖 Select model for {providers[provider]['name']}:", style="bold")
        
        table = Table(title="Available Models")
        table.add_column("Choice", style="cyan", width=8)
        table.add_column("Model ID", style="bold")
        table.add_column("Description", style="dim")
        
        for i, model in enumerate(available_models, 1):
            description = self._get_model_description(model)
            marker = " (current)" if model == current_model else ""
            table.add_row(str(i), model + marker, description)
        
        console.print(table)
        
        while True:
            choice = Prompt.ask(
                f"\nEnter your choice (1-{len(available_models)})",
                choices=[str(i) for i in range(1, len(available_models) + 1)],
                default="1"
            )
            
            model_index = int(choice) - 1
            selected_model = available_models[model_index]
            
            console.print(f"\n✅ Selected: {selected_model}", style="green")
            
            # Update configuration
            models = self.config.models.copy()
            models[provider] = selected_model
            
            self.config_manager.update_config(models=models)
            return True
    
    def _get_model_description(self, model_id: str) -> str:
        """Get a human-readable description for a model"""
        if "claude-sonnet-4" in model_id:
            return "Latest Claude 4 Sonnet - Most capable"
        elif "claude-3-5-sonnet" in model_id:
            return "Claude 3.5 Sonnet - Balanced performance"
        elif "claude-3-haiku" in model_id:
            return "Claude 3 Haiku - Fast and cost-effective"
        elif "gemini-2.5" in model_id:
            return "Gemini 2.5 - Latest generation"
        elif "gemini-1.5-pro" in model_id:
            return "Gemini 1.5 Pro - Advanced capabilities"
        elif "gemini-1.5-flash" in model_id:
            return "Gemini 1.5 Flash - Fast responses"
        elif "gpt-4o" in model_id:
            return "GPT-4o - Multimodal flagship"
        elif "gpt-4o-mini" in model_id:
            return "GPT-4o Mini - Cost-effective"
        elif "gpt-4-turbo" in model_id:
            return "GPT-4 Turbo - High performance"
        elif "nova-pro" in model_id:
            return "Amazon Nova Pro - Amazon's flagship"
        elif "llama4" in model_id:
            return "Llama 4 - Meta's latest"
        else:
            return "Available model"
    
    def _configure_parameters(self):
        """Configure model parameters"""
        console.print("\n⚙️  Configure model parameters:", style="bold")
        
        # Temperature
        current_temp = self.config.params.get("temperature", 0.7)
        temperature = Prompt.ask(
            "Temperature (0.0-1.0, lower=more focused, higher=more creative)",
            default=str(current_temp)
        )
        
        try:
            temp_val = float(temperature)
            if 0.0 <= temp_val <= 1.0:
                self.config_manager.update_config(temperature=temp_val)
            else:
                console.print("⚠️  Temperature must be between 0.0 and 1.0, using default", style="yellow")
        except ValueError:
            console.print("⚠️  Invalid temperature value, using default", style="yellow")
        
        # Max tokens
        current_tokens = self.config.params.get("max_tokens", 1000)
        max_tokens = Prompt.ask(
            "Max tokens (response length limit)",
            default=str(current_tokens)
        )
        
        try:
            tokens_val = int(max_tokens)
            if tokens_val > 0:
                self.config_manager.update_config(max_tokens=tokens_val)
            else:
                console.print("⚠️  Max tokens must be positive, using default", style="yellow")
        except ValueError:
            console.print("⚠️  Invalid max tokens value, using default", style="yellow")
        
        console.print("✅ Parameters configured", style="green")
    
    def _display_provider_info(self):
        """Display information about available providers"""
        providers = ProviderFactory.get_available_providers()
        
        console.print("\n" + "="*60)
        console.print("🤖 AVAILABLE AI PROVIDERS", style="bold blue")
        console.print("="*60)
        
        for key, info in providers.items():
            panel = Panel(
                f"{info['description']}\n\n"
                f"📋 Available Models:\n"
                + "\n".join([f"  • {model}" for model in info["models"][:3]]) +
                (f"\n  • ... and {len(info['models'])-3} more" if len(info["models"]) > 3 else "") +
                f"\n\n🔐 Credentials: {info['credentials']}",
                title=f"[bold]{info['name']}[/bold] ({key})",
                border_style="blue"
            )
            console.print(panel)
            console.print()

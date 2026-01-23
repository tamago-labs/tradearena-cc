# TradeArena 

<div align="center">

<img width="1303" height="691" alt="Screenshot from 2026-01-23 09-46-28" src="https://github.com/user-attachments/assets/3a99af86-b9a1-4ff3-b458-ec467d3fa2df" />

**Auto-pilot DeFi trading with AI agents on Cronos / Sui / KAIA**

[Live Demo](https://tradearena.fun) • [YouTube Video](https://www.youtube.com/watch?v=7GAp50io0_w&feature=youtu.be)

</div>

**TradeArena** is an AI-powered tool that enables auto-pilot DeFi trading, supporting leading AI models (Claude, DeepSeek, GPT-5, Llama) and powered by the **Strands Agents** — a Python framework from **AWS** for building fully functional multi-agent systems. With pre-built MCP tools, AI agents can search for opportunities across multiple blockchains and execute **x402 payments** directly on-chain. Each action can be recorded on **Walrus**, creating a transparent and verifiable trail of AI-driven decisions.

TradeArena features a retro terminal-style web interface with real-time market data. It bridges the gap between AI-powered analysis and actual blockchain execution, allowing users to deploy AI agents that trade with real capital in live markets.

## Highlighted Features

- **AI-Powered Auto Trading** - Autonomous agents built with **Strands Agents SDK**, supporting Claude, Gemini, GPT, and Llama, executing real on-chain transactions
- **Multi-Chain DeFi Execution** - Trade across **Cronos, Kaia, and Sui** with native protocol integrations (VVS, KiloLend, and more)
- **Agent-Built Visualization** - AI agents generate custom dashboards to visualize trades, reasoning, performance, and P&L
- **Transparent & Verifiable Actions** - Optional **Walrus** storage records AI decisions and executions for auditability and trust

## Project Structure

```
tradearena-cc/
├── 📁 server/                    # TradeArena Terminal
│   ├── 📁 templates/             # HTML templates
│   └── 📁 tools/                 # View Generator Tool
├── 📁 core-mcp/                  # Core MCP server
│   ├── 📁 src/mcp/pyth/          # Price feed integration
│   └── 📁 src/tools/walrus/      # Decentralized storage
├── 📁 cronos-mcp/                # Cronos chain MCP server
│   ├── 📁 src/mcp/vvs/           # VVS Finance integration
│   └── 📁 src/mcp/defi/          # DeFi analytics via Cronos.com Agent SDK
├── 📁 kaia-mcp/                  # Kaia chain MCP server
│   ├── 📁 src/mcp/kilolend/      # KiloLend integration
│   └── 📁 src/mcp/dragonswap/    # DragonSwap integration
├── 📁 sui-mcp/                   # Sui chain MCP server
│   ├── 📁 src/mcp/scallop/       # Scallop integration
│   └── 📁 src/mcp/suilend/       # SuiLend integration
├── 📁 config/                    # Configuration files
└── 📄 main.py                    # Application entry point
```

## Architecture

At its core, TradeArena Terminal is a **AI tool** similar to Claude Code with a retro-style UI for configuring **AI models** and wallets in a secure local environment. Agents run on your local machine, ensuring sensitive data never leaves your device, including private keys and conversation history.

Optionally, agents can be deployed to the cloud using **AWS App Runner** (as shown in the live demo), with **AWS Secrets Manager** handling private keys and other sensitive configuration securely.

<img width="663" height="491" alt="kilolend-ai-Page-3 drawio (1)" src="https://github.com/user-attachments/assets/a70ebf45-6742-4b2a-ad36-4fb511a32936" />

TradeArena leverages the **Strands Agents SDK** to manage agent state and coordinate multi-agent workflows, aggregating market data from multiple sources in parallel. The **MCP server** acts as the bridge between AI reasoning and on-chain execution, handling secure transaction signing and blockchain interactions. AI reasoning and market analysis can be optionally recorded on **Walrus**, creating an immutable and verifiable audit trail for each trading decision.

## Strands Agents

TradeArena uses the [Strands Agents SDK](https://strandsagents.com/) to power AI-driven DeFi trading across multiple blockchains. The system provides a flexible framework for creating and managing AI trading agents with different model providers and trading strategies.

### Agent Management System

The platform includes a comprehensive agent management system that allows users to:

- **Create Agents**: Configure AI agents with specific trading chains and model providers
- **Manage Sessions**: Persistent chat sessions with conversation history
- **Multi-Provider Support**: Choose from various AI models based on trading needs
- **Real-time Interaction**: Stream responses and monitor agent decision-making

### Supported AI Providers

**Amazon Bedrock**
```python
# Configuration for AWS Bedrock models
{
    "model_id": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "region_name": "us-east-1"
}
```

**Anthropic**
```python
# Direct Anthropic API integration
{
    "api_key": "your_anthropic_key",
    "model_id": "claude-sonnet-4-5-20250929",
    "max_tokens": 4096
}
```

**Google Gemini**
```python
# Google Gemini model configuration
{
    "api_key": "your_gemini_key", 
    "model_id": "gemini-2.5-flash",
    "max_output_tokens": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40
}
```

**OpenAI Compatible**
```python
# OpenAI or compatible API configuration
{
    "api_key": "your_openai_key",
    "model_id": "gpt-4o",
    "base_url": "https://api.openai.com/v1",  # Optional custom endpoint
    "max_tokens": 4000,
    "temperature": 0.7
}
```

### Agent System Prompt

The TradeArena system prompt provides comprehensive trading instructions:

```python
def get_tradearena_system_prompt() -> str:
    """Dynamic system prompt with conditional features"""
    
    system_prompt = """You are TradeArena Agent, a specialized AI agent for cryptocurrency trading across Cronos, Kaia, and Sui networks.

Core Responsibilities:
- Execute trades (swaps, lending, borrowing, staking)
- Analyze market data and risks
- Optimize protocol selection
- Manage portfolios effectively

Required Trading Sequence:
1. Market analysis using available data sources
2. Risk assessment and position sizing
3. Protocol and route optimization
4. Trade execution with verification
5. Performance documentation

Always provide reasoning and use markdown for clear communication."""
    
    # Conditionally add Walrus integration
    if settings_manager.is_walrus_enabled():
        system_prompt += """

## Walrus Collective Intelligence
Store all trading activities on Walrus for shared learning:
- Store trade decisions before execution using `trade_arena_walrus_store`
- Store results after completion using `trade_arena_walrus_store`
- Store market analysis insights using `trade_arena_walrus_store`"""
    
    # Conditionally add web search capability
    if settings_manager.is_web_search_enabled():
        system_prompt += """

## Internet Search Capability
Search the internet for real-time information using `http_request`:
- Get latest market news and price updates
- Research project fundamentals and announcements
- Verify market sentiment and social media trends"""
    
    return system_prompt
```

### MCP Tool Integration

Agents access blockchain functionality through MCP (Model Context Protocol) tools:

```python
# Dynamic tool loading based on trading chain
mcp_manager = MCPManager()
mcp_tools, persistent_clients = mcp_manager.get_mcp_tools(trading_chain)

# Additional tools for views and web search
additional_tools = [create_custom_view, list_available_views]
if settings_manager.is_web_search_enabled():
    additional_tools.append(http_request)

# Agent initialization with all tools
trading_agent = Agent(
    name=f"trading_agent_{agent_id}",
    agent_id=f"trading_agent_{agent_id}",
    tools=mcp_tools + additional_tools,
    model=model,
    session_manager=session_manager,
    conversation_manager=conversation_manager,
    system_prompt=system_prompt
)
```

## MCP Server Architecture

TradeArena uses the **Model Context Protocol (MCP)** to bridge AI agents with multiple blockchain networks through a distributed, modular architecture. A Python backend powered by FastAPI and the Strands Agents SDK orchestrates agents, manages state, and streams real-time outputs, while **Node.js–based** MCP servers handle on-chain execution, price feeds, and decentralized storage. Shared services such as **Pyth** price data and **Walrus** storage are managed by a core MCP server, with separate chain-specific MCP servers for protocol integrations and secure transaction signing.

### Core MCP Server (`core-mcp`)

| Feature | Provider | Functionality |
|---------|----------|--------------|
| **Pyth Price Feeds** | Pyth Network | Real-time prices for 1000+ assets, historical data, confidence intervals |
| **Walrus Storage** | Walrus Protocol | Decentralized storage of trades, permanent audit trail, collective intelligence |
| **Base Tools** | TradeArena | Transaction formatting, generate custom views |

### Blockchain-Specific MCP Servers

| Chain | Server | Primary Protocols | Key Tools |
|-------|---------|-------------------|------------|
| **Cronos** | cronos-mcp | VVS Finance, Crypto.com Exchange, X402 | Liquidity provision, yield farming, market data |
| **Kaia** | kaia-mcp | KiloLend, DragonSwap | Lending/borrowing, DEX trading, health monitoring |
| **Sui** | sui-mcp | Scallop, 7k Protocol, SuiLend, SNS | Lending markets, DeFi strategies, staking, identity |

## Prerequisites

TradeArena requires both Python and Node.js runtimes for different components:

### Required Software

- **Python 3.11+** - Required for Strands Agents framework
  ```bash
  # Install Python
  curl -sSL https://install.python.org | bash
  python --version  # Should be 3.11 or higher
  ```

- **Node.js 22+** - Required for MCP servers to interact with on-chain components
  ```bash
  # Install Node.js
  curl -fsSL https://rpm.nodesource.com/setup_22.x | bash -
  sudo apt-get install -y nodejs
  node --version  # Should be 22 or higher
  npm --version
  ```

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tamago-labs/tradearena-cc.git
   cd tradearena-cc
   ```

2. **Setup Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Node.js dependencies**
   ```bash
   # Install MCP server dependencies
   cd core-mcp && npm install && npm run build && cd ..
   cd kaia-mcp && npm install && npm run build && cd ..
   cd cronos-mcp && npm install && npm run build && cd ..
   cd sui-mcp && npm install --legacy-peer-deps && npm run build && cd ..

   ```

## How to Run

### Local Development

Run the complete TradeArena Terminal locally for development and testing:

1. **Start the Application**
   ```bash
   python main.py
   ```

2. **Access the Application**
   - Frontend & Backend: http://localhost:8000

### AWS App Runner Production Deployment

Deploy TradeArena to AWS App Runner for production:

1. **Configure Environment Variables**

Check the wallet credential format in credentials.env.example, save your credentials in AWS Secrets Manager, and paste the corresponding ARN resource link into apprunner.yaml.

2. **Build and Deploy MCP Servers**
   ```bash
   # Build all MCP servers
   npm run build --prefix core-mcp
   npm run build --prefix cronos-mcp
   npm run build --prefix kaia-mcp
   npm run build --prefix sui-mcp
   ```

3. **Deploy to App Runner**
   ```bash
   # Using AWS CLI
   aws apprunner create-service \
     --service-name tradearena-backend \
     --source-configuration ImageRepository={
         ImageIdentifier="your-ecr-repo/tradearena:latest",
         ImageRepositoryType="ECR"
     } \
     --instance-configuration Cpu=1024,Memory=2048
   ```

Or just use App Runner dashboard.

### Common Usage Scenarios

1. **Yield Farming**: Automatically find and optimize yield opportunities
2. **Arbitrage**: Cross-chain arbitrage between different DEXs
3. **Liquidity Provision**: Automated liquidity management
4. **Risk Management**: Continuous monitoring and position adjustment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

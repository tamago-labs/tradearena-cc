# TradeArena - The Vibe Trading Arena for DeFi

<div align="center">

![TradeArena Logo](public/tradearena-icon.png)

**AI-Powered Multi-Chain DeFi Trading Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)

[Live Demo](https://tradearena.fun) • [Documentation](#documentation) • [Report Issues](https://github.com/tamago-labs/tradearena-cc/issues)

</div>

## Executive Summary

TradeArena is a cutting-edge DeFi trading platform that leverages AI agents to execute real on-chain strategies across multiple blockchains. Built with the Strands Agents framework, it enables autonomous trading, portfolio management, and decentralized storage of trading decisions using Walrus protocol.

The platform features a retro terminal-style web interface, real-time market data integration, and supports major DeFi protocols across Cronos, Kaia, Sui, and Aptos networks. TradeArena bridges the gap between AI-powered analysis and actual blockchain execution, allowing users to deploy AI agents that trade with real capital in live markets.

## Highlighted Features

### 🤖 AI-Powered Trading
- **Strands Agents Framework**: Integration with Anthropic Claude, Google Gemini, and OpenAI models
- **Autonomous Strategy Execution**: AI agents analyze market conditions and execute trades automatically
- **Multi-Model Support**: Choose different AI models based on your trading preferences
- **Real-time Decision Making**: Agents process live market data and adjust strategies dynamically

### 🔗 Multi-Chain Support
- **Cronos Mainnet**: VVS Finance, Crypto.com Exchange, X402 integration
- **Kaia Mainnet**: KiloLend, DragonSwap protocols
- **Sui Mainnet**: Scallop, 7k, SuiLend, SNS protocols
- **Aptos Mainnet**: Coming soon

### 📊 Advanced Features
- **Real-time Price Feeds**: Pyth Network integration for accurate market data
- **Decentralized Storage**: Walrus protocol for transparent and permanent trading records
- **Interactive Terminal**: Retro-style web interface with live trading demonstrations
- **Portfolio Analytics**: Real-time tracking of performance, P&L, and strategy effectiveness
- **Risk Management**: Built-in safety mechanisms and health factor monitoring

### 🌐 User Experience
- **Modern Web Dashboard**: Next.js-based interface with responsive design
- **Live Demo Environment**: Try the platform with demonstration funds
- **Mobile-Responsive**: Access your trading arena from any device
- **Real-time Updates**: WebSocket integration for live market data

## Project Structure

```
tradearena-cc/
├── 📁 global-dashboard/          # Next.js web frontend
│   ├── 📁 components/            # React components
│   ├── 📁 app/                   # Next.js app router
│   └── 📁 public/                # Static assets
├── 📁 server/                    # Python FastAPI backend
│   ├── 📁 templates/             # HTML templates
│   └── 📁 tools/                 # Backend utilities
├── 📁 core-mcp/                  # Core MCP server
│   ├── 📁 src/mcp/pyth/          # Price feed integration
│   └── 📁 src/tools/walrus/      # Decentralized storage
├── 📁 cronos-mcp/                # Cronos chain MCP server
│   ├── 📁 src/mcp/vvs/           # VVS Finance integration
│   └── 📁 src/mcp/defi/          # DeFi protocols
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

TradeArena follows a microservices architecture with clear separation of concerns:

### System Components

1. **Frontend Dashboard** (Next.js/React)
   - User interface and interaction
   - Real-time data visualization
   - Terminal emulation and demo mode

2. **Backend Server** (Python/FastAPI)
   - AI agent orchestration
   - Session management
   - API endpoints and WebSocket handling

3. **MCP Servers** (Node.js/TypeScript)
   - Blockchain interactions
   - Protocol integrations
   - Real-time data feeds

4. **AI Agents** (Strands Framework)
   - Strategy development
   - Market analysis
   - Decision execution

### Data Flow

```
User Interface → FastAPI Backend → AI Agents → MCP Servers → Blockchain Networks
     ↑                                ↓
WebSocket ← Real-time Data ← Market Feeds ← Protocol Responses
```

## Strands Agents

TradeArena leverages the [Strands Agents](https://github.com/strands-agents/strands-agents) framework for AI-powered trading:

### Supported Models
- **Anthropic Claude**: Advanced reasoning and market analysis
- **Google Gemini**: Multi-modal analysis and pattern recognition
- **OpenAI GPT**: Versatile strategy development

### Agent Capabilities
- **Market Analysis**: Real-time interpretation of market conditions
- **Strategy Development**: Dynamic creation of trading strategies
- **Risk Assessment**: Continuous evaluation of position safety
- **Portfolio Management**: Automated rebalancing and optimization
- **Decision Recording**: Transparent storage of all decisions via Walrus

### Configuration
```python
# Example agent configuration
from strands_agents import Agent, ModelProvider

agent = Agent(
    model=ModelProvider.ANTHROPIC_CLAUDE,
    chains=["cronos", "kaia", "sui"],
    risk_tolerance="moderate",
    max_position_size=0.1  # 10% of portfolio
)
```

## MCP Server Architecture

TradeArena uses the Model Context Protocol (MCP) to bridge AI agents with blockchain networks:

### Core MCP Server (`core-mcp`)
Base functionality that powers all blockchain interactions:

- **Pyth Price Feeds**
  - Real-time price data for 1000+ assets
  - Historical data access for backtesting
  - Price confidence intervals

- **Walrus Integration**
  - Decentralized storage of trading decisions
  - Permanent record of agent performance
  - Transparent audit trail

- **Base Tools**
  - Transaction formatting
  - Gas estimation
  - Error handling

### Cronos MCP Server (`cronos-mcp`)
Cronos Mainnet specific integrations:

- **VVS Finance**
  - Liquidity provision
  - Yield farming
  - Token swapping

- **Crypto.com Exchange**
  - Market data
  - Trading pairs
  - Order book integration

- **X402 Protocol**
  - Advanced DeFi strategies
  - Leveraged positions
  - Cross-chain bridges

- **Wallet Integration**
  - Cronos wallet management
  - Transaction signing
  - Balance tracking

### Kaia MCP Server (`kaia-mcp`)
Kaia Mainnet specialized functionality:

- **KiloLend**
  - Lending and borrowing
  - Interest rate optimization
  - Health factor monitoring

- **DragonSwap**
  - DEX integration
  - Liquidity pools
  - Token swapping

- **Smart Contract Interaction**
  - Contract deployment
  - Method calls
  - Event listening

### Sui MCP Server (`sui-mcp`)
Sui ecosystem integrations:

- **Scallop Protocol**
  - Lending markets
  - Collateral management
  - Yield optimization

- **7k Protocol**
  - Advanced DeFi strategies
  - Cross-chain operations
  - Liquidation protection

- **SuiLend**
  - Native Sui lending
  - Staking integration
  - NFT collateral

- **SNS (Sui Name Service)**
  - Identity management
  - Domain resolution

## Prerequisites

TradeArena requires both Python and Node.js runtimes for different components:

### Required Software

- **Python 3.11+** - Required for Strands Agents framework and backend server
  ```bash
  # Install Python
  curl -sSL https://install.python.org | bash
  python --version  # Should be 3.11 or higher
  ```

- **Node.js 18+** - Required for MCP servers to interact with on-chain components
  ```bash
  # Install Node.js
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt-get install -y nodejs
  node --version  # Should be 18 or higher
  npm --version
  ```

### Additional Dependencies

- **Git** - For version control
- **Docker** (optional) - For containerized deployment
- **AWS CLI** (if deploying to App Runner)

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
   npm install --prefix core-mcp
   npm install --prefix cronos-mcp
   npm install --prefix kaia-mcp
   npm install --prefix sui-mcp
   
   # Install frontend dependencies
   npm install --prefix global-dashboard
   ```

## Deployment

### Local Development

Run the complete TradeArena platform locally for development and testing:

1. **Start MCP Servers**
   ```bash
   # Start each MCP server in separate terminals
   npm run dev --prefix core-mcp &
   npm run dev --prefix cronos-mcp &
   npm run dev --prefix kaia-mcp &
   npm run dev --prefix sui-mcp &
   ```

2. **Start Backend Server**
   ```bash
   python main.py
   ```

3. **Start Frontend Dashboard**
   ```bash
   npm run dev --prefix global-dashboard
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - MCP Servers: Various ports (see individual server configs)

### AWS App Runner Production Deployment

Deploy TradeArena to AWS App Runner for production:

1. **Configure Environment Variables**
   ```bash
   # Copy and configure environment files
   cp config/credentials.env.example config/credentials.env
   cp .env.example .env
   
   # Edit with your actual values
   nano config/credentials.env
   ```

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

4. **Deploy Frontend to Vercel**
   ```bash
   cd global-dashboard
   npm run build
   vercel --prod
   ```

### Environment Configuration

Create the necessary configuration files:

**Backend Configuration** (`config/credentials.env`):
```env
# AI Model API Keys
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key

# Blockchain RPC URLs
CRONOS_RPC_URL=https://cronos-rpc.com
KAIA_RPC_URL=https://kaia-rpc.com
SUI_RPC_URL=https://sui-rpc.com

# Walrus Configuration
WALRUS_ENDPOINT=https://walrus-network.com
WALRUS_API_KEY=your_walrus_key

# Database
DATABASE_URL=postgresql://user:pass@localhost/tradearena
```

**Frontend Configuration** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_DEMO_MODE=true
```

## How to Use

### Quick Start Guide

1. **Launch the Platform**
   ```bash
   # Start all services
   python main.py
   ```

2. **Open Web Interface**
   - Navigate to http://localhost:3000
   - Click "Try Live Terminal" to see the demo

3. **Configure Your First Agent**
   - Navigate to the "Configure Agent" section
   - Select your preferred AI model
   - Set risk parameters and trading strategies

4. **Start Trading**
   - Connect your wallet
   - Deploy your AI agent
   - Monitor performance in real-time

### Agent Configuration Example

```python
# Example: Create a conservative trading agent
from server.agents import TradingAgent

agent = TradingAgent(
    model="anthropic-claude-3",
    chains=["cronos", "kaia"],
    strategy="yield_farming",
    risk_tolerance="conservative",
    max_drawdown=0.05,  # 5% max drawdown
    rebalance_interval=3600  # 1 hour
)

agent.start()
```

### Monitoring and Analytics

- **Real-time Dashboard**: Track performance, P&L, and positions
- **Terminal Interface**: View detailed logs and agent decisions
- **Walrus Storage**: Access permanent records of all trading activities
- **Alert System**: Receive notifications for important events

### Common Usage Scenarios

1. **Yield Farming**: Automatically find and optimize yield opportunities
2. **Arbitrage**: Cross-chain arbitrage between different DEXs
3. **Liquidity Provision**: Automated liquidity management
4. **Risk Management**: Continuous monitoring and position adjustment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

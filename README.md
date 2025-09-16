# 🤖 Finance Agent

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

**An intelligent multi-agent system for financial analysis and utility tasks**

[🚀 Live Demo](#-live-demo) • [📖 Documentation](#-documentation) • [🔧 Installation](#-installation) • [🧪 Testing](#-testing)

</div>

---

[🚀 Live Demo](#-live-demo) • [📖 Documentation](#-documentation) • [🔧 Installation](#-installation) • [🧪 Testing](#-testing)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Live Demo](#-live-demo)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🧪 Testing](#-testing)
- [📡 API Reference](#-api-reference)
- [🔍 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👤 Author](#-author)

---

## 🎯 Overview

**Finance Agent** is a sophisticated AI-powered assistant that combines financial expertise with general utility functions. Built with modern AI frameworks, it provides intelligent responses to complex queries about stock markets, financial news, weather updates, and more.

The system employs a **dual-agent architecture** with specialized agents for financial and utility tasks, each equipped with a comprehensive toolkit of integrated services and APIs.

### 🎯 Key Capabilities

- **Financial Analysis**: Real-time stock data, market trends, news sentiment
- **Utility Services**: Weather updates, Wikipedia search, unit conversions
- **Intelligent Processing**: Chain-of-thought reasoning with tool integration
- **Multi-modal Input**: Support for text and image queries
- **Streaming Responses**: Real-time response delivery for better UX

---

## ✨ Features

### 🤖 Dual-Agent System

#### 💰 Financial Assistant
- **Real-time Stock Data**: Live price quotes from multiple sources
- **Historical Analysis**: Comprehensive market data and trends
- **Financial News**: Latest market news and sentiment analysis
- **Cryptocurrency**: BTC and altcoin market data
- **Trend Analysis**: Technical indicators and market insights

#### 🛠️ Utility Assistant
- **Weather Updates**: Global weather information
- **Wikipedia Search**: Knowledge base queries
- **Unit Conversions**: Comprehensive conversion tools
- **Time Management**: Timezone conversions and scheduling
- **Web Search**: General information retrieval

### 🔧 Integrated Tools

| Category | Tools | Description |
|----------|-------|-------------|
| 📈 **Financial** | Stock Market, Historical Data, News API, Sentiment Analysis | Market data and analysis |
| 💱 **Currency** | Exchange Rates, Crypto Markets | Financial conversions |
| 🌤️ **Weather** | Weather API, Location Services | Global weather data |
| 🔍 **Search** | Wikipedia, Web Search, News | Information retrieval |
| ⚙️ **Utilities** | Calculator, Unit Converter, Timezone, Calendar | General utilities |

### 🎨 Advanced Features

- **🔄 Streaming Responses**: Real-time response streaming
- **🖼️ Image Processing**: Multi-modal input support
- **💬 Conversation Memory**: Context-aware interactions
- **🔧 Tool Integration**: Dynamic tool loading and execution
- **📊 Data Visualization**: Chart and graph generation
- **🌐 RESTful API**: Clean, documented endpoints

---

## 🏗️ Architecture

### 🏛️ System Components

#### **Backend Architecture**
- **FastAPI Server**: High-performance async web framework
- **Agent Manager**: Orchestrates specialized agents
- **Tool Registry**: Dynamic loading of utility tools
- **LangGraph Engine**: Chain-of-thought reasoning pipeline

#### **Agent Architecture**
- **Financial Agent**: Specialized for market analysis
- **Utility Agent**: General-purpose assistant
- **Tool Integration**: LangChain-compatible tools
- **Memory Management**: Conversation context handling

---

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)

### Infrastructure
![Uvicorn](https://img.shields.io/badge/Uvicorn-000000?style=flat&logo=gunicorn&logoColor=white)

### Tools & Libraries
- **Data Processing**: pandas, numpy, yfinance
- **APIs**: NewsAPI, OpenWeather, Financial Modeling Prep
- **ML/AI**: transformers, torch, scikit-learn
- **Async**: aiohttp, asyncio
- **Testing**: pytest, requests

---

## 🚀 Live Demo

The Finance Agent is currently running and accessible via (**might break over time, replace with localhost**):

**🌐 Public URL**: [https://financeagent-3o3nqpokdvwxjzv7xwbswl.streamlit.app/](https://financeagent-3o3nqpokdvwxjzv7xwbswl.streamlit.app/)

### Quick Test Commands

```bash
# Health Check
curl https://lively-intimate-treefrog.ngrok-free.app/health

# Stock Price Query
curl -X POST https://lively-intimate-treefrog.ngrok-free.app/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Apple stock price?", "agent_type": "financial_assistant"}'

# Weather Query
curl -X POST https://lively-intimate-treefrog.ngrok-free.app/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Weather in New York?", "agent_type": "utility_assistant"}'
```

---

## 📦 Installation

### Prerequisites

- **Python**: 3.11 or higher
- **pip**: Latest version
- **Git**: For cloning the repository

### 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/tarunk42/finance_agent.git
   cd finance_agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 10000 --reload
   ```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Financial APIs
FMP_API_KEY=your_fmp_api_key_here
NEWS_API_KEY=your_news_api_key_here
SERP_API_KEY=your_serp_api_key_here

# Utility APIs
OPEN_WEATHER_API_KEY=your_weather_api_key_here
SERPER_API_KEY=your_serper_api_key_here
EXCHANGE_RATE_API_KEY=your_exchange_api_key_here
```

### API Key Sources

| Service | Website | Free Tier |
|---------|---------|-----------|
| OpenAI | [openai.com](https://openai.com) | $5 credit |
| Financial Modeling Prep | [fmpcloud.io](https://fmpcloud.io) | 250 requests/day |
| NewsAPI | [newsapi.org](https://newsapi.org) | 100 requests/day |
| OpenWeather | [openweathermap.org](https://openweathermap.org) | 1000 calls/day |
| Serper | [serper.dev](https://serper.dev) | 2500 searches/month |

---

## 🧪 Testing

### Manual Testing

#### Health Check
```bash
curl http://localhost:10000/health
# Expected: {"status": "healthy"}
```

#### Financial Queries
```bash
# Stock Price
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current price of AAPL?",
    "agent_type": "financial_assistant"
  }'

# Market News
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Latest news about Tesla",
    "agent_type": "financial_assistant"
  }'
```

#### Utility Queries
```bash
# Weather
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Weather in London",
    "agent_type": "utility_assistant"
  }'

# Wikipedia Search
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "agent_type": "utility_assistant"
  }'
```

#### Advanced Queries
```bash
# With conversation history
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the trend?",
    "agent_type": "financial_assistant",
    "history": [
      {
        "role": "user",
        "content": "Show me AAPL stock data for last 30 days"
      },
      {
        "role": "assistant",
        "content": "Here is the historical data for AAPL..."
      }
    ]
  }'
```

---

## 📡 API Reference

### Base URL
```
http://localhost:10000  # Local development
https://your-domain.com  # Production
```

### Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "Finance Agent API is running."
}
```

#### `GET /health`
Detailed health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-02T23:00:00Z",
  "version": "1.0.0"
}
```

#### `POST /chat`
Main chat endpoint for agent interaction.

**Request Body:**
```json
{
  "query": "string",           // Required: User's question
  "agent_type": "string",      // Required: "financial_assistant" or "utility_assistant"
  "history": [                 // Optional: Conversation history
    {
      "role": "user",
      "content": "Previous message"
    }
  ],
  "image": {                   // Optional: Image input
    "type": "base64",
    "media_type": "image/png",
    "data": "base64_encoded_string"
  }
}
```

**Response:**
```json
{
  "response": "AI-generated response text",
  "tool_outputs": [
    {
      "tool_name": "StockMarketTool",
      "tool_call_id": "call_123",
      "data": {
        "ticker": "AAPL",
        "latest_price": 229.72,
        "high": 230.78,
        "low": 226.97,
        "volume": 36141577
      }
    }
  ]
}
```

### Error Responses

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

---

## 🔍 Project Structure

```
finance_agent/
├── 📁 agents/                 # Agent implementations
│   ├── __init__.py
│   ├── agent_manager.py      # Main agent orchestration
│   ├── market_insight_agent.py
│   └── utility_agent.py
├── 📁 tools/                  # Tool implementations
│   ├── __init__.py
│   ├── stock_market_tool.py   # Financial tools
│   ├── weather_tool.py        # Utility tools
│   ├── news_api_tool.py
│   └── ... (15+ tools)
├── 📁 data/                   # Data storage
│   ├── calendar_reminders.json
│   └── tools_db.json
├── 📁 notebooks/              # Jupyter notebooks
│   ├── setup_check.ipynb
│   └── Data_Retrieval Agent.ipynb
├── 📄 api.py                  # FastAPI application
├── 📄 config.py               # Configuration and constants
├── 📄 main.py                 # Application entry point
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                    # Environment variables
└── 📄 README.md              # This file
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```
4. **Run tests**
   ```bash
   pytest
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Guidelines

- **Code Style**: Follow PEP 8
- **Tests**: Add tests for new features
- **Documentation**: Update README for significant changes
- **Commits**: Use clear, descriptive commit messages

---

## 📸 Demo Screenshots

Here are some screenshots of the Finance Agent in action:

### 1. Application Interface
![Finance Agent Interface](https://github.com/tarunk42/finance_agent/blob/main/run_example/Screenshot%202025-09-02%20at%2022.54.35.png)

### 2. Chat Interaction
![Chat Example](https://github.com/tarunk42/finance_agent/blob/main/run_example/Screenshot%202025-09-02%20at%2022.54.55.png)

### 3. Response Output
![Response Example](https://github.com/tarunk42/finance_agent/blob/main/run_example/Screenshot%202025-09-02%20at%2023.10.18.png)

---

## 👤 Author

**Tarun Kashyap**

- **GitHub**: [@tarunk42](https://github.com/tarunk42)
- **LinkedIn**: [tarun-kashyap](https://linkedin.com/in/tarun-kashyap)
- **Website**: [tarunk42.github.io](https://tarunk42.github.io)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">


[⬆️ Back to Top](#-finance-agent)

---

*For questions or support, please open an issue on GitHub.*

</div>

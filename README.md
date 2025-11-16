# Python MCP Server (Market Crypto Proxy)

## Overview
This project is a minimal, production-minded **MCP** (Market Crypto Proxy) server that:
- Fetches realtime ticker data from major exchanges via `ccxt`.
- Provides historical OHLCV queries.
- Exposes an SSE endpoint for realtime streaming (polling-based).
- Includes caching and robust error handling.
- Comes with unit and API tests (pytest).

This repository is intended as an internship assignment submission: it demonstrates structured code, test coverage, and best-practices.

## Requirements
- Python 3.10+
- `pip` to install dependencies.

Install:
```bash

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Project Requirements (Simplified)

1. Health Check
GET http://localhost:8000/health

2. Live Price
GET http://localhost:8000/price?exchange=binance&symbol=BTC/USDT

3. Historical OHLCV
GET http://localhost:8000/history?exchange=binance&symbol=BTC/USDT&timeframe=1m&limit=10

4. Streaming Prices
GET http://localhost:8000/stream/price?exchange=binance&symbol=BTC/USDT&interval=5

Features
- FastAPI-based server
- CCXT for market data
- TTL caching
- Error handling
- Test cases using pytest

Run the server
uvicorn app.main:app --reload



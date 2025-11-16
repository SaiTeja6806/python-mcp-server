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

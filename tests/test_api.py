import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@patch("app.exchanges.fetch_ticker")
def test_price_endpoint(mock_fetch):
    mock_fetch.return_value = {
        "symbol": "BTC/USDT",
        "last": 50000,
        "timestamp": 12345
    }
    resp = client.get("/price?exchange=binance&symbol=BTC/USDT")
    assert resp.status_code == 200
    body = resp.json()
    assert body["symbol"] == "BTC/USDT"
    assert "last" in body

@patch("app.exchanges.fetch_ohlcv")
def test_history_endpoint(mock_ohlcv):
    mock_ohlcv.return_value = [
        [1620000000000, 100, 110, 90, 105, 10],
        [1620000060000, 105, 115, 95, 110, 12],
    ]
    resp = client.get("/history?exchange=binance&symbol=BTC/USDT")
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body
    assert len(body["data"]) == 2

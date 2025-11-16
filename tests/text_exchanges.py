import pytest
from unittest.mock import patch, MagicMock
import ccxt
from app import exchanges
from app.exceptions import ExchangeNotSupported, ExternalAPIError

def test_get_exchange_not_supported():
    with pytest.raises(ExchangeNotSupported):
        exchanges.get_exchange("unknown-exchange")

@patch("app.exchanges.ccxt.binance")
def test_fetch_ticker_success(mock_binance):
    # make a fake exchange instance with fetch_ticker
    instance = MagicMock()
    instance.fetch_ticker.return_value = {
        "symbol": "BTC/USDT",
        "timestamp": 1234567890,
        "last": 50000,
        "bid": 49990,
        "ask": 50010,
        "baseVolume": 12.3
    }
    mock_binance.return_value = instance

    data = exchanges.fetch_ticker("binance", "BTC/USDT")
    assert data["symbol"] == "BTC/USDT"
    assert data["last"] == 50000
    assert "raw" in data

@patch("app.exchanges.ccxt.binance")
def test_fetch_ticker_ccxt_error(mock_binance):
    instance = MagicMock()
    instance.fetch_ticker.side_effect = ccxt.NetworkError("network down")
    mock_binance.return_value = instance

    with pytest.raises(ExternalAPIError):
        exchanges.fetch_ticker("binance", "BTC/USDT")

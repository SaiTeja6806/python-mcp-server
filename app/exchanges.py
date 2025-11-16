import ccxt
import time
from typing import Dict, Any, Optional, List
from .exceptions import ExchangeNotSupported, SymbolNotFound, ExternalAPIError
from .cache import DEFAULT_CACHE
from cachetools import cached

# supported exchanges: add more by name (ccxt id)
SUPPORTED = {
    "binance": "binance",
    "kraken": "kraken",
    "coinbase": "coinbasepro",  # coinbasepro in ccxt
    "huobi": "huobipro",
    # add more or allow any ccxt-exchange after whitelist
}

def get_exchange(exchange_name: str):
    if exchange_name not in SUPPORTED:
        raise ExchangeNotSupported(f"Exchange '{exchange_name}' not supported.")
    ex_id = SUPPORTED[exchange_name]
    try:
        exchange = getattr(ccxt, ex_id)()
        return exchange
    except Exception as e:
        raise ExternalAPIError(f"Failed to init exchange {exchange_name}: {e}") from e


# cache core market fetch for a short TTL to avoid rate limits
@cached(DEFAULT_CACHE)
def fetch_ticker(exchange_name: str, symbol: str) -> Dict[str, Any]:
    """Fetch current ticker from exchange (synchronous)."""
    exchange = get_exchange(exchange_name)
    try:
        ticker = exchange.fetch_ticker(symbol)
        # normalize essential fields
        return {
            "symbol": ticker.get("symbol") or symbol,
            "timestamp": ticker.get("timestamp") or int(time.time() * 1000),
            "datetime": ticker.get("datetime"),
            "last": ticker.get("last"),
            "bid": ticker.get("bid"),
            "ask": ticker.get("ask"),
            "high": ticker.get("high"),
            "low": ticker.get("low"),
            "volume": ticker.get("baseVolume") or ticker.get("volume"),
            "raw": ticker,
        }
    except ccxt.BaseError as e:
        raise ExternalAPIError(f"ccxt error: {e}") from e
    except Exception as e:
        raise ExternalAPIError(f"unexpected error: {e}") from e


def fetch_ohlcv(exchange_name: str, symbol: str, timeframe: str = "1m", since: Optional[int] = None, limit: int = 100) -> List:
    """
    Fetch historical OHLCV data.
    since: ms timestamp
    """
    exchange = get_exchange(exchange_name)
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        # return list of ohlc arrays [timestamp, open, high, low, close, volume]
        return ohlcv
    except ccxt.BaseError as e:
        raise ExternalAPIError(f"ccxt error: {e}") from e
    except Exception as e:
        raise ExternalAPIError(f"unexpected error: {e}") from e

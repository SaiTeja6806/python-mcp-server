import os
import time
import asyncio
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse  # lightweight SSE helper
from typing import Optional
from .exchanges import fetch_ticker, fetch_ohlcv
from .exceptions import MCPError, ExchangeNotSupported, ExternalAPIError, SymbolNotFound

app = FastAPI(title="MCP - Market Crypto Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(MCPError)
async def mcp_error_handler(request, exc: MCPError):
    return JSONResponse(status_code=400, content={"error": str(exc)})

@app.get("/health")
async def health():
    return {"status": "ok", "time": int(time.time()*1000)}

@app.get("/price")
async def price(exchange: str = Query(..., description="exchange short name e.g. binance"), symbol: str = Query(..., description="symbol e.g. BTC/USDT")):
    """
    Return current ticker for the symbol on given exchange.
    Uses cached fetch to reduce rate limits.
    """
    try:
        data = fetch_ticker(exchange, symbol)
        return data
    except ExchangeNotSupported as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def history(exchange: str = Query(...), symbol: str = Query(...), timeframe: str = Query("1m"), since: Optional[int] = Query(None), limit: int = Query(100)):
    """
    Return historical OHLCV data: [timestamp, open, high, low, close, volume]
    since is ms timestamp (optional)
    """
    try:
        data = fetch_ohlcv(exchange, symbol, timeframe=timeframe, since=since, limit=limit)
        return {"symbol": symbol, "exchange": exchange, "timeframe": timeframe, "data": data}
    except ExchangeNotSupported as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stream/price")
async def stream_price(exchange: str = Query(...), symbol: str = Query(...), interval: int = Query(5, ge=1, description="poll interval seconds")):
    """
    SSE endpoint streaming the latest price every `interval` seconds.
    Clients can connect and receive JSON messages.
    """

    async def event_generator():
        # continuously poll (in production prefer websockets / exchange websockets)
        try:
            while True:
                try:
                    data = fetch_ticker(exchange, symbol)
                    payload = {
                        "symbol": data.get("symbol"),
                        "last": data.get("last"),
                        "bid": data.get("bid"),
                        "ask": data.get("ask"),
                        "timestamp": data.get("timestamp"),
                    }
                    yield {"event": "ticker", "data": JSONResponse(content=payload).body.decode()}
                except Exception as e:
                    # send error message to client but continue streaming
                    yield {"event": "error", "data": str(e)}
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            # client disconnected
            return

    return EventSourceResponse(event_generator())

class MCPError(Exception):
    """Base MCP error."""
    pass

class ExchangeNotSupported(MCPError):
    pass

class SymbolNotFound(MCPError):
    pass

class ExternalAPIError(MCPError):
    pass

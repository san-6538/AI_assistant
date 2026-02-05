import httpx
from tools.base import BaseTool

class YahooFinanceTool(BaseTool):
    async def run(self, params: dict):
        symbol = params["symbol"]
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
            quote = r.json()["quoteResponse"]["result"][0]
            return {
                "symbol": symbol,
                "price": quote.get("regularMarketPrice"),
                "currency": quote.get("currency")
            }

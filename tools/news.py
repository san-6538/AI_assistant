import os
import httpx
from tools.base import BaseTool

API_KEY = os.getenv("NEWS_API_KEY")

class NewsTool(BaseTool):
    async def run(self, params: dict):
        query = params["query"]
        url = "https://newsapi.org/v2/everything"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params={
                "q": query,
                "apiKey": API_KEY,
                "pageSize": 3
            })
            r.raise_for_status()
            articles = r.json()["articles"]
            return [
                {"title": a["title"], "source": a["source"]["name"]}
                for a in articles
            ]

import httpx
from tools.base import BaseTool

class WikipediaTool(BaseTool):
    async def run(self, params: dict):
        title = params["query"]
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            return {
                "title": data.get("title"),
                "summary": data.get("extract")
            }

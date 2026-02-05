import httpx
from tools.base import BaseTool

class GeocodingTool(BaseTool):
    async def run(self, params: dict):
        city = params["city"]
        url = "https://nominatim.openstreetmap.org/search"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params={
                "q": city,
                "format": "json",
                "limit": 1
            }, headers={
                "User-Agent": "AI_Assistant_Demo/1.0"
            })
            r.raise_for_status()
            if not r.json():
                raise ValueError(f"Could not find coordinates for city: {city}")
            data = r.json()[0]
            return {
                "latitude": float(data["lat"]),
                "longitude": float(data["lon"]),
                "city": city
            }

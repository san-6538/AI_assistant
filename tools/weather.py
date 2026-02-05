import httpx
from tools.base import BaseTool

class WeatherTool(BaseTool):
    async def run(self, params: dict):
        lat = params["latitude"]
        lon = params["longitude"]

        url = "https://api.open-meteo.com/v1/forecast"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            })
            r.raise_for_status()
            weather = r.json()["current_weather"]

            return {
                "temperature": weather["temperature"],
                "windspeed": weather["windspeed"],
                "weathercode": weather["weathercode"]
            }

from tools.wikipedia import WikipediaTool
from tools.weather import WeatherTool
from tools.yahoo_finance import YahooFinanceTool
from tools.news import NewsTool
from tools.geocoding import GeocodingTool

TOOL_REGISTRY = {
    "wikipedia": WikipediaTool(),
    "weather": WeatherTool(),
    "yahoo_finance": YahooFinanceTool(),
    "news": NewsTool(),
    "geocoding": GeocodingTool(),
}

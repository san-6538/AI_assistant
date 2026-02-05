from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    async def run(self, params: dict):
        pass

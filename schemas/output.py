from pydantic import BaseModel
from typing import List, Optional, Any

class FinalResponse(BaseModel):
    summary: str
    data: Any
    sources: List[str]

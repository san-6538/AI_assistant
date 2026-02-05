from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Step(BaseModel):
    id: str
    tool: str
    params: Dict[str, Any]

class ExecutionPlan(BaseModel):
    steps: List[Step]

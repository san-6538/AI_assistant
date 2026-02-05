from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from core.orchestrator import Orchestrator

app = FastAPI()
orchestrator = Orchestrator()

@app.post("/run-task")
async def run_task(payload: dict):
    return await orchestrator.run(payload["task"])

from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.verifier = VerifierAgent()

    async def run(self, task: str):
        plan = self.planner.run(task)
        data = await self.executor.run(plan)
        return self.verifier.run(data)

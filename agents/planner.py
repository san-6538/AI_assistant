import json
from agents.base import BaseAgent
from llm.client import LLMClient
from llm.prompts import planner_prompt
from schemas.plan import ExecutionPlan
from core.logger import setup_logger

logger = setup_logger("PlannerAgent")

class PlannerAgent(BaseAgent):
    def run(self, task: str) -> dict:
        logger.info(f"Generating plan for task: {task}")
        response = LLMClient.complete(planner_prompt(task))
        with open("planner_debug.log", "w", encoding="utf-8") as f:
            f.write(response)
        logger.info("Plan generated, parsing JSON...")
        print(f"DEBUG_PLANNER_RESPONSE: {repr(response)}")
        import re
        # Sanitize response
        match = re.search(r"```json(.*?)```", response, re.DOTALL)
        if match:
            plan_str = match.group(1).strip()
        else:
            plan_str = response.replace("```", "").strip()
            
        print(f"DEBUG_PLAN_STR: {repr(plan_str)}")
        try:
            plan = json.loads(plan_str)
        except json.JSONDecodeError as e:
            # Fallback or error logging could go here
            print(f"Failed to parse JSON: {e}")
            print(f"FAILING STRING HEX: {plan_str.encode('utf-8').hex()}")
            raise
            
        return ExecutionPlan.model_validate(plan).dict()

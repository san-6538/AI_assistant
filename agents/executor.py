import asyncio
from agents.base import BaseAgent
from tools.registry import TOOL_REGISTRY
from core.retry import retry_async
from core.logger import setup_logger

logger = setup_logger("ExecutorAgent")

class ExecutorAgent(BaseAgent):
    def resolve_params(self, params: dict, context: dict) -> dict:
        resolved = {}
        for k, v in params.items():
            if isinstance(v, str) and v.startswith("{{") and v.endswith("}}"):
                # Format: {{step_id.key}}
                step_id, key = v.strip("{}").split(".")
                if step_id in context and context[step_id]:
                    val = context[step_id].get(key)
                    if val is None:
                        logger.warning(f"Key '{key}' not found in results for step '{step_id}'")
                        resolved[k] = v # Leave unresolved
                    else:
                        resolved[k] = val
                else:
                    logger.error(f"Step '{step_id}' not found in context or failed")
                    resolved[k] = v 
            else:
                resolved[k] = v
        return resolved

    async def run(self, plan: dict) -> dict:
        results = {}
        
        # Sort steps by ID dependency if needed, but for now assuming linear or pre-sorted plan 
        # Actually need to execute sequentially for dependencies to work
        for step in plan["steps"]:
            tool_name = step["tool"]
            step_id = step["id"]
            
            logger.info(f"Executing step '{step_id}' with tool '{tool_name}'")
            
            if tool_name not in TOOL_REGISTRY:
                results[step_id] = {"error": f"Tool {tool_name} not found"}
                continue

            tool = TOOL_REGISTRY[tool_name]
            
            # Resolve parameters using previous results
            resolved_params = self.resolve_params(step["params"], results)
            
            try:
                # We need to await each step now if dependencies exist
                # If we want parallel execution for independent tasks, we'd need a DAG runner
                # For this specific update (weather depends on geo), simple sequential or smart sequential is needed
                # The prompt implies a simple sequential execution for dependent steps or update to support it
                # I will switch to sequential execution to strictly support dependencies as per the request "Planner -> Executor" flow enhancement
                
                result = await retry_async(tool.run, resolved_params)
                results[step_id] = result
            except Exception as e:
                 results[step_id] = {"error": str(e)}

        return results

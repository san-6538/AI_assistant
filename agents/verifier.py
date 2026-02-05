import json
from agents.base import BaseAgent
from llm.client import LLMClient
from llm.prompts import verifier_prompt
from schemas.output import FinalResponse
from core.logger import setup_logger

logger = setup_logger("VerifierAgent")

class VerifierAgent(BaseAgent):
    def run(self, execution_data: dict) -> dict:
        logger.info("Verifying execution data...")
        response = LLMClient.complete(verifier_prompt(execution_data))
        
        # Sanitize response
        import re
        match = re.search(r"```json(.*?)```", response, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
        else:
            json_str = response.replace("```json", "").replace("```", "").strip()
            
        data = json.loads(json_str)
        logger.info("Verification complete.")
        return FinalResponse.model_validate(data).dict()

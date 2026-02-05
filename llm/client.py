from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMClient:
    @staticmethod
    def complete(prompt: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4o", # Using a clearer model name, or keep gpt-4 if preferred. sticking to original but updating syntax
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content

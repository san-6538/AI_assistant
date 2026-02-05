def planner_prompt(task: str) -> str:
    return f"""
You are a Planner Agent.
Convert the task into a JSON plan using ONLY the available tools.

Available Tools:
1. geocoding
   - params: "city" (str)
   - output: latitude, longitude
2. weather
   - params: "latitude" (float), "longitude" (float)
   - note: ALWAYS requires coordinates from geocoding first
3. wikipedia
   - params: "query" (str)
4. yahoo_finance
   - params: "ticker" (str)
5. news
   - params: "query" (str)

Task: {task}

Rules:
- Plan may need multiple steps (e.g. Geocoding -> Weather)
- Use {{{{step_id.key}}}} to reference outputs from previous steps
- Output valid JSON only (no markdown, no comments)

Example Plan (Weather):
{{
  "steps": [
    {{ "id": "geo", "tool": "geocoding", "params": {{ "city": "London" }} }},
    {{ "id": "weather", "tool": "weather", "params": {{ "latitude": "{{{{geo.latitude}}}}", "longitude": "{{{{geo.longitude}}}}" }} }}
  ]
}}
"""

def verifier_prompt(data: dict) -> str:
    return f"""
You are a Verifier Agent.
Validate completeness and format final response.

Execution data:
{data}

Rules:
- 'summary': Concise text summary.
- 'data': Use MARKDOWN TABLES for structured data (e.g. weather stats, stock prices, news list).
- 'sources': List of tools used.

Output JSON only:
{{
  "summary": "...",
  "data": "Markdown string here...",
  "sources": [...]
}}
"""

from backend.tools import TOOLS
import json
from backend.gemini import generate_answer
def run_agent(prompt):
    response=generate_answer(prompt)
    try:
        data=json.loads(response)
        tool=data.pop("tool")
        if tool in TOOLS:
            return TOOLS[tool](**data)
    except:
        return response

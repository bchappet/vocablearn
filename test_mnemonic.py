import os
import sys
from pydantic_ai.models.groq import GroqModel
from pydantic_ai import Agent

api_key = os.environ["GROQ_API_KEY"]

model_name = "llama-3.3-70b-versatile"
model = GroqModel(model_name=model_name, api_key=api_key)

fpath = os.path.join('routers', 'quiz', 'ai', 'system_prompt.txt')
with open(fpath, encoding="utf8") as f:
    system_prompt = f.readlines()
    agent = Agent(model, system_prompt=system_prompt)

arg = sys.argv[1]
if not arg:
    raise AssertionError("You need to provide a word")
result =  agent.run_sync(f'Please give me a mnemonic to remember the word {arg}')
print(result.data)
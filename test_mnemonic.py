import os
import sys
from pydantic_ai.models.groq import GroqModel
from pydantic_ai import Agent


def remove_think_tags(text):
    # Define the pattern to match text between <think> and </think> tags
    pattern = r'<think>.*?</think>'
    # Use re.sub to replace the matched pattern with an empty string
    result = re.sub(pattern, '', text, flags=re.DOTALL)
    return result

api_key = os.environ["GROQ_API_KEY"]

model_name = "deepseek-r1-distill-llama-70b"
model = GroqModel(model_name=model_name, api_key=api_key)

fpath = os.path.join('routers', 'quiz', 'ai', 'prompts','claude_generated_prompt.txt')
with open(fpath, encoding="utf8") as f:
    system_prompt = f.readlines()
    agent = Agent(model, system_prompt=system_prompt)

arg = sys.argv[1]
if not arg:
    raise AssertionError("You need to provide a word")
result =  agent.run_sync(f'Please give me a mnemonic to remember the word {arg}')
print(result.data)
import re
match = re.search(r'```(.*?)```', result.data)
if match:
    extracted = match.group(1) 

breakpoint()
print()


import requests
import json
import os
from openai import OpenAI

MY_API_KEY = "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"



client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=MY_API_KEY,
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "localhost:3000", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "Vocablearnpro", # Optional. Site title for rankings on openrouter.ai.
  },
  model="deepseek/deepseek-r1:free",
  messages=[
    {
      "role": "user",
      "content": "Can you give me a mnemonic for the word 'apple' in russian?"
    }
  ]
)
print(completion.choices[0].message.content)
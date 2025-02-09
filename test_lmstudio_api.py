import requests


API_URL = "http://localhost:1234/v1/chat/completions" 

payload = {
    "model": "llama-3.2-1b-instruct",  # Replace with the model name you loaded in LM Studio
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},  # Context/pre-prompt
        {"role": "user", "content": "Explain the theory of relativity in simple terms."}  # User's question
    ],
    "temperature": 0.7,
    "max_tokens": 500,
}
 

# Define headers
headers = {
    "Content-Type": "application/json"
}

# Send the request to the LM Studio API with streaming
print("Sending request to LM Studio API...")
response = requests.post(API_URL, headers=headers, json=payload, stream=True)

print(response.status_code)
print(response.json())
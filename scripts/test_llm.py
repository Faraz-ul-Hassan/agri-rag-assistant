import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "In one sentence, what is retrieval-augmented generation?"}
    ],
    temperature=0.2,
)

print(response.choices[0].message.content)
print(f"\nTokens used: {response.usage.total_tokens}")

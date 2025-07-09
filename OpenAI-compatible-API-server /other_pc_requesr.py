from openai import OpenAI

client = OpenAI(
    base_url="http://0.0.0.0:8000/v1",
    api_key="key_pc1"  # Phải khớp trong api_keys.json
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello from another PC!"}]
)

print(response.choices[0].message.content)

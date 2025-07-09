from openai import OpenAI

client = OpenAI(
    base_url="http://YOUR_PC_IP:8000/v1",  # ví dụ 192.168.1.10
    api_key="key_pc1"
)

response = client.chat.completions.create(
    model="330",  # tên này bạn chỉ cần để đúng định dạng, không ảnh hưởng
    messages=[{"role": "user", "content": "Hello! Compare this for me"}],
    temperature=0.5,
    top_p=0.9,
    max_tokens=1024
)

print(response.choices[0].message.content)

import requests

url = "http://127.0.0.1:8000/chat"  # Gọi ngay trên máy bạn
headers = {
    "Content-Type": "application/json",
    "x-api-key": "key_pc1"  # Nhớ dùng đúng key trong API_KEYS
}
data = {
    "prompt": "Xin chào AI! Bạn đang chạy không?"
}
response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("✅ Kết quả:")
    print("Text thô từ server:", response.text)  # 👈 kiểm tra trước
    try:
        print("Dạng JSON:", response.json())
    except Exception as e:
        print("❌ Lỗi khi parse JSON:", e)
else:
    print("❌ Gặp lỗi:", response.status_code)
    print(response.text)

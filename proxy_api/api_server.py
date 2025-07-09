import sys

from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
import requests
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from xml_compare.prompt import compare_xml_with_prompt


app = FastAPI()

# 🔑 Danh sách key hợp lệ và gán tên
API_KEYS = {
    "key_pc1": "PC_1",
    "key_test": "Máy Test",
    "key_admin": "Admin"
}

# 🚫 Giới hạn số lần gọi mỗi ngày cho từng key
MAX_REQUESTS_PER_DAY = {
    "key_pc1": 100,
    "key_test": 10,
    "key_admin": 1000
}
REAL_API_KEY = os.getenv("REAL_API_KEY")
REAL_API_BASE = os.getenv("REAL_API_BASE")
class PromptInput(BaseModel):
    prompt: str

# ✅ Ghi log chi tiết truy cập
def log_access_to_file(user_name, key, client_ip, prompt_text):
    log_line = (
        f"[{datetime.now()}] IP: {client_ip} | KEY: {key} | USER: {user_name} | PROMPT: {prompt_text}\n"
    )
    with open("access.log", "a", encoding="utf-8") as f:
        print(log_line)
        f.write(log_line)

# ✅ Ghi và kiểm tra số lượt dùng mỗi key theo ngày
def track_key_usage_and_check_limit(key):
    today = datetime.now().strftime("%Y-%m-%d")
    usage_file = "key_usage.json"

    # Nếu chưa có file thì tạo mới
    if not os.path.exists(usage_file):
        with open(usage_file, "w") as f:
            json.dump({}, f)

    # Đọc dữ liệu hiện tại
    with open(usage_file, "r") as f:
        data = json.load(f)

    # Tạo ngày nếu chưa có
    if today not in data:
        data[today] = {}

    # Tạo key nếu chưa có
    if key not in data[today]:
        data[today][key] = 0

    # Kiểm tra vượt giới hạn
    current_count = data[today][key]
    max_allowed = MAX_REQUESTS_PER_DAY.get(key, 100)
    if current_count >= max_allowed:
        raise HTTPException(
            status_code=429,
            detail=f"🚫 Key '{key}' đã vượt giới hạn {max_allowed} lượt/ngày."
        )

    # Tăng số lượt
    data[today][key] += 1

    # Ghi lại
    with open(usage_file, "w") as f:
        json.dump(data, f, indent=2)




@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/chats")
async def proxy_chat(
    request: Request,
    data: PromptInput,
    x_api_key: Optional[str] = Header(None)
):
#     # Check API key
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API key")

    # Ghi log IP và key
    client_ip = request.client.host
    user_name = API_KEYS[x_api_key]

    log_access_to_file(user_name, x_api_key, client_ip, data.prompt)
    track_key_usage_and_check_limit(x_api_key)
    # Gọi model nội bộ

    try:
        # response = requests.post(
        #     f"{REAL_API_BASE}/chat/completions",  # API model thực
        #     json={
        #         "model": "gpt2",  # Hoặc tên model thật
        #         "messages": [{"role": "user", "content": data.prompt}]
        #     }
        # )
        # # result = response.json()
        # # Giả lập phản hồi thay vì gọi model
        # result = {
        #     "choices": [
        #         {
        #             "message": {
        #                 "role": "assistant",
        #                 "content": f"Chào {user_name}, bạn vừa hỏi: '{data.prompt}'"
        #             }
        #         }
        #     ]
        # }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer YOUR_API_KEY",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",  # hoặc anthropic/claude-3-sonnet, meta-llama/llama-3-70b-instruct,...
                "messages": [
                    {"role": "user", "content": "Viết 1 bài thơ 4 câu về Hà Nội"}
                ]
            }
        )
        result = response.json()
        return {
            "user": user_name,
            "ip": client_ip,
            "response": result
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/compare_xml")
async def compare_xml_api(
    tablet_xml: Annotated[UploadFile, File(...)],
    phone_xml: Annotated[UploadFile, File(...)]
):
    try:
        tablet_xml_str = (await tablet_xml.read()).decode("utf-8")
        print("✅ Tablet XML string OK")
        phone_xml_str = (await phone_xml.read()).decode("utf-8")
        print("✅ Phone XML string OK")
    except Exception as e:
        print(f"Failed to read uploaded files: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded files: {str(e)}")
    print("Tablet XML snippet: >>>", repr(tablet_xml_str[:300]), "<<<")
    print("Phone XML snippet: >>>", repr(phone_xml_str[:300]), "<<<")

    # Gọi hàm so sánh đã sửa để nhận string XML
    try:
        result = compare_xml_with_prompt.compare_xml_with_prompt(tablet_xml_str, phone_xml_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

    # Nếu result trả về dict có lỗi, trả về 400
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return JSONResponse(content=result)


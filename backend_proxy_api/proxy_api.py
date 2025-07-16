import sys

from fastapi.responses import RedirectResponse
from fastapi import Request, Header,Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend_proxy_api.xml_compare.code_compare import compare_xml_with_logic_code, code_gauss


from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",  # ← THÊM DÒNG NÀY
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    from typing import Optional
@app.post("/compare_xml_by_gauss")
async def compare_xml_by_gauss(
    request: Request,
    tablet_xml: Annotated[UploadFile, File(..., description="Tablet XML file")],
    phone_xml: Annotated[UploadFile, File(..., description="Phone XML file")],
        # prompt_txt: Annotated[Optional[UploadFile], File(description="Prompt txt file")] = None,
        prompt_txt: Annotated[Optional[str], Form()]= None,
    x_api_key: Optional[str] = Header(None)
):
    # ✅ Kiểm tra API key
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="❌ Forbidden: Invalid API key")

    user_name = API_KEYS[x_api_key]
    client_ip = request.client.host
    log_access_to_file(user_name, x_api_key, client_ip, "[COMPARE_XML_BY_GAUSS]")
    track_key_usage_and_check_limit(x_api_key)

    # ✅ Kiểm tra định dạng file
    if not tablet_xml.filename.endswith(".xml"):
        raise HTTPException(status_code=400, detail="❌ tablet_xml phải là file .xml")

    if not phone_xml.filename.endswith(".xml"):
        raise HTTPException(status_code=400, detail="❌ phone_xml phải là file .xml")

    prompt_txt_content = ""

    if prompt_txt is not None:
        prompt_txt_content =prompt_txt
        # if not prompt_txt.filename.endswith(".txt"):
        #     raise HTTPException(status_code=400, detail="❌ prompt_txt phải là file .txt")
        # prompt_txt_content = (await prompt_txt.read()).decode("utf-8")
        print("Tablet XML snippet: >>> prompt_txt_content", "<<<")
    else:
        print("Tablet XML snippet: >>> Nones", "<<<")
    # ✅ Đọc nội dung file
    try:
        tablet_content = (await tablet_xml.read()).decode("utf-8")
        phone_content = (await phone_xml.read()).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Không thể đọc file: {str(e)}")
    #
    # print("Tablet XML snippet: >>>", repr(tablet_content[:300]), "<<<")
    # print("Phone XML snippet: >>>", repr(phone_content[:300]), "<<<")

    # ✅ Gọi hàm xử lý AI
    try:
        result = code_gauss.compare_xml_by_gauss(tablet_content, phone_content, prompt_txt_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Lỗi xử lý AI: {str(e)}")

    if not isinstance(result, dict):
        raise HTTPException(status_code=500, detail="❌ Kết quả không hợp lệ từ model.")

    return JSONResponse(content=result)




@app.post("/compare_xml_by_logic_code")
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
    # print("Tablet XML snippet: >>>", repr(tablet_xml_str[:300]), "<<<")
    # print("Phone XML snippet: >>>", repr(phone_xml_str[:300]), "<<<")

    # Gọi hàm so sánh đã sửa để nhận string XML
    try:
        result = compare_xml_with_logic_code.compare_xml_lgcode(tablet_xml_str, phone_xml_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

    # Nếu result trả về dict có lỗi, trả về 400
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return JSONResponse(content=result)


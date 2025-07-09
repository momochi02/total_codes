from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import requests
import json
import datetime

load_dotenv()

REAL_API_KEY = os.getenv("REAL_API_KEY")
REAL_API_BASE = os.getenv("REAL_API_BASE")

# Load key map
with open("api_keys.json", "r") as f:
    API_KEYS = json.load(f)

USAGE_FILE = "usage_stats.json"
LOG_FILE = "access.log"
app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024
    stream: Optional[bool] = False

def log_access_to_file(client_ip, key, name, prompt, response):
    now = datetime.datetime.now().isoformat()
    log_line = f"[{now}] IP: {client_ip} | KEY: {key} ({name}) | Prompt: {prompt} | Response: {response}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

def update_usage_stats(key):
    today = datetime.date.today().isoformat()
    try:
        with open(USAGE_FILE, "r") as f:
            stats = json.load(f)
    except FileNotFoundError:
        stats = {}

    if key not in stats:
        stats[key] = {}
    if today not in stats[key]:
        stats[key][today] = 0
    stats[key][today] += 1

    with open(USAGE_FILE, "w") as f:
        json.dump(stats, f, indent=2)


@app.post("/v1/chat_gauss/completions")
async def proxy_chat(request: Request, body: ChatRequest, authorization: Optional[str] = Header(None)):
    # --- Check API key ---
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(content={"error": "Missing or invalid Authorization header"}, status_code=401)

    api_key = authorization.split(" ")[1]
    if api_key not in API_KEYS:
        return JSONResponse(content={"error": "Invalid API key"}, status_code=403)

    client_name = API_KEYS[api_key]
    client_ip = request.client.host

    # --- Lấy prompt ---
    user_prompt = body.messages[-1].content if body.messages else ""

    # --- Lấy LLM model ID ---

    _apim_host_url = "https://fabrix"
    _apim_openapi_key = "Bearer 1234sdfsf"
    _apim_generative_key = "xpZW50U2V"
    _apim_endpoint_model_url = "/openapi/chat/v1/models"
    _apim_endpoint_chat_url = "/openapi/chat/v1/messages"
    _apim_ad_id = "chi.dtp@samsung.com"
    try:
        # headers = {
        #     "x-openapi-token": "Bearer 1234sdfsf",
        #     "x-generative-ai-client": "xpZW50U2V",
        #     "x-generative-ai-user-email": "ch@gmail.com",
        #     "Content-Type": "application/json"
        # }

        headers: dict = {
            'x-openapi-token': _apim_openapi_key,
            'x-generative-ai-client': _apim_generative_key,
            'x-generative-ai-user-email': _apim_ad_id,
            'Content-Type': 'application/json'
        }
        response: requests.Response = requests.get(_apim_host_url + _apim_endpoint_model_url,
                                                   headers=headers)
        print("1. Get LLM Model Response", response.json())
        llm_id = response.json()[0]['modelId']  # The first model ID that can be inquired.
        print(f"llm_id: {llm_id}")
    except Exception as e:
        return JSONResponse(content={"error": f"Không thể lấy modelId: {str(e)}"}, status_code=500)
        # llmId = 330

    # --- Gọi API model ---
    payload = {
        "llmId": llm_id,
        "contents": [user_prompt],
        "llmConfig": {
            "do_sample": True,
            "max_new_tokens": body.max_tokens or 1024,
            "return_full_text": False,
            "top_k": 14,
            "top_p": body.top_p or 0.94,
            "temperature": body.temperature or 0.4,
            "repetition_penalty": 1.04,
            "decoder_input_details": False,
            "details": False
        },
        "isStream": body.stream or False
    }

    try:

        response: requests.Response = requests.post(_apim_host_url + _apim_endpoint_chat_url, json=body,
                                                    headers=headers)
        response.raise_for_status()
        ai_result = response.json()
        model_response = ai_result.get('content', '')

        log_access_to_file(client_ip, api_key, client_name, user_prompt, model_response)
        update_usage_stats(api_key)

        # Trả về định dạng OpenAI-compatible
        return {
            "id": "chatcmpl-fakeid123",
            "object": "chat.completion",
            "created": int(datetime.datetime.now().timestamp()),
            "model": body.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": model_response
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

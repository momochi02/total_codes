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

@app.post("/v1/chat/completions")
async def proxy_chat(request: Request, body: ChatRequest, authorization: Optional[str] = Header(None)):
    # --- Auth check ---
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(content={"error": "Missing or invalid Authorization header"}, status_code=401)

    api_key = authorization.split(" ")[1]
    if api_key not in API_KEYS:
        return JSONResponse(content={"error": "Invalid API key"}, status_code=403)

    client_name = API_KEYS[api_key]
    client_ip = request.client.host

    # --- Relay to real API ---
    headers = {
        "Authorization": f"Bearer {REAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": body.model,
        "messages": [msg.dict() for msg in body.messages],
        "temperature": body.temperature,
        "top_p": body.top_p,
        "max_tokens": body.max_tokens,
        "stream": body.stream
    }

    try:
        response = requests.post(
            f"{REAL_API_BASE}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        # --- Log and update ---
        user_prompt = body.messages[-1].content
        model_response = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        log_access_to_file(client_ip, api_key, client_name, user_prompt, model_response)
        update_usage_stats(api_key)

        return JSONResponse(content=data)

    except requests.exceptions.RequestException as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

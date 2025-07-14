import subprocess
import os
import threading

# Đường dẫn đến backend (FastAPI) và frontend (React)
BACKEND_DIR = "//Users/game/Desktop/chi/auto_app_update/backend_proxy_api"
FRONTEND_DIR = "/Users/game/Desktop/chi/auto_app_update/frontend"

def run_backend():
    os.chdir(BACKEND_DIR)
    subprocess.run(["uvicorn", "backend_proxy_api.proxy_api:app", "--host", "127.0.0.1", "--port", "8000"])

def run_frontend():
    os.chdir(FRONTEND_DIR)
    subprocess.run(["npm", "start"])

# Tạo 2 luồng song song để chạy backend & frontend
backend_thread = threading.Thread(target=run_backend)
frontend_thread = threading.Thread(target=run_frontend)

backend_thread.start()
frontend_thread.start()

# Đợi cả 2 luồng kết thúc (chạy song song mãi đến khi Ctrl+C)
backend_thread.join()
frontend_thread.join()

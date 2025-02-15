import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """檢查並安裝所需依賴"""
    try:
        import streamlit
        import flask
        import requests
        from annotated_text import annotated_text
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_web.txt"])

def run_services():
    """運行 Flask 後端和 Streamlit 前端"""
    web_dir = Path(__file__).parent
    
    # 檢查依賴
    check_dependencies()
    
    try:
        # 啟動 Flask 後端
        print("Starting Flask backend...")
        flask_process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=web_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # 等待 Flask 啟動
        
        # 啟動 Streamlit 前端
        print("Starting Streamlit frontend...")
        streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend.py"],
            cwd=web_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("\n✨ Services started successfully!")
        print("🌐 Flask API: http://localhost:5000")
        print("🚀 Streamlit UI: http://localhost:8501")
        print("\nPress Ctrl+C to stop all services...")
        
        # 等待進程結束
        flask_process.wait()
        streamlit_process.wait()
        
    except KeyboardInterrupt:
        print("\n\nShutting down services...")
        flask_process.terminate()
        streamlit_process.terminate()
        
        print("Waiting for services to close...")
        flask_process.wait(timeout=5)
        streamlit_process.wait(timeout=5)
        
        print("Services stopped successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_services()
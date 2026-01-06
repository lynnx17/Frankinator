import threading
import time
import webbrowser
import uvicorn
from frankinator.web import app


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")


threading.Thread(target=start_server, daemon=True).start()

time.sleep(1)
webbrowser.open("http://127.0.0.1:8000")

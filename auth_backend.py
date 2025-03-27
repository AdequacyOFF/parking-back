import os

import uvicorn

if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("SERVER_PORT", 8080))
    hot_reload = bool(os.getenv("HOT_RELOAD", False))

    uvicorn.run("app.app:create_app", host=host, port=port, reload=hot_reload)

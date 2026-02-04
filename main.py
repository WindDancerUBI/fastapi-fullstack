from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# 挂载静态文件目录
frontend_dist_dir = os.path.join(os.path.dirname(__file__), "./frontend/dist")
app.mount("/static", StaticFiles(directory=frontend_dist_dir), name="static")

@app.get("/hello")
async def hello_world():
    return "hello world"

# 处理根路径请求，返回 index.html
@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dist_dir, "index.html"))
    # return 'hello world'

# 可选：处理其他路由回退到 index.html（适用于 SPA）
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = os.path.join(frontend_dist_dir, full_path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dist_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import json, os, uvicorn, sys

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("🚀 API Server has successfully booted up!", flush=True)
    print("✅ New changes have fully reflected on Hugging Face!", flush=True)
    print("📡 Active and listening for inbound traffic...", flush=True)

@app.api_route("/api/master.json", methods=["GET", "HEAD"])
def master():
    print("📥 REQUEST: /api/master.json", flush=True)
    with open("api/master.json") as f:
        return JSONResponse(json.load(f), headers={"Cache-Control": "no-store"})

@app.api_route("/api/current/{filename}", methods=["GET", "HEAD"])
def current(filename: str):
    print(f"📥 REQUEST: /api/current/{filename}", flush=True)
    path = f"api/current/{filename}"
    if os.path.exists(path):
        with open(path) as f:
            return JSONResponse(json.load(f), headers={"Cache-Control": "no-store"})

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import json, os, uvicorn

app = FastAPI()

@app.get("/api/master.json")
def master():
    with open("api/master.json") as f:
        return JSONResponse(json.load(f), headers={"Cache-Control": "no-store"})

@app.get("/api/current/{filename}")
def current(filename: str):
    path = f"api/current/{filename}"
    if os.path.exists(path):
        with open(path) as f:
            return JSONResponse(json.load(f), headers={"Cache-Control": "no-store"})

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

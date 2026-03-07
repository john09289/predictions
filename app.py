import json
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, PlainTextResponse

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
    return JSONResponse({"error": "not found"}, status_code=404)

@app.get("/api/predictions.json")
def predictions():
    with open("api/predictions.json") as f:
        return JSONResponse(json.load(f), headers={"Cache-Control": "no-store"})

@app.get("/style.css")
def css():
    with open("style.css") as f:
        return PlainTextResponse(f.read(), media_type="text/css")

@app.get("/app.js")
def appjs():
    with open("app.js") as f:
        return PlainTextResponse(f.read(), media_type="application/javascript")

@app.get("/predictions.js")
def predictionsjs():
    with open("predictions.js") as f:
        return PlainTextResponse(f.read(), media_type="application/javascript")

@app.get("/scoring.js")
def scoringjs():
    with open("scoring.js") as f:
        return PlainTextResponse(f.read(), media_type="application/javascript")

@app.get("/weekly.js")
def weeklyjs():
    with open("weekly.js") as f:
        return PlainTextResponse(f.read(), media_type="application/javascript")

@app.get("/")
def root():
    with open("index.html") as f:
        return HTMLResponse(f.read())

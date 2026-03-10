import json
import os
import logging
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.exceptions import HTTPException
import traceback

# Configure logging to stdout so it appears in HF logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("dome_registry")

app = FastAPI(title="Dome Cosmology Registry API")

# No-cache headers for all API responses
NO_CACHE_HEADERS = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0"
}

# Helper to safely read JSON files with no-cache headers
def safe_json_response(filepath: str):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return JSONResponse(content=data, headers=NO_CACHE_HEADERS)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return JSONResponse(status_code=404, content={"error": "Not found"}, headers=NO_CACHE_HEADERS)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {filepath}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"}, headers=NO_CACHE_HEADERS)
    except Exception as e:
        logger.error(f"Unexpected error reading {filepath}: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"}, headers=NO_CACHE_HEADERS)

# Helper to safely read static files (CSS, JS)
def safe_text_response(filepath: str, media_type: str):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return PlainTextResponse(content, media_type=media_type)
    except FileNotFoundError:
        logger.error(f"Static file not found: {filepath}")
        return PlainTextResponse("/* not found */", status_code=404, media_type=media_type)
    except Exception as e:
        logger.error(f"Error reading static file {filepath}: {traceback.format_exc()}")
        return PlainTextResponse("/* error */", status_code=500, media_type=media_type)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "version": "50.4"}

# API endpoints — all with no-cache headers
@app.get("/api/master.json")
async def master():
    return safe_json_response("api/master.json")

@app.get("/api/current/{filename}")
async def current(filename: str):
    # Prevent path traversal
    if ".." in filename or "/" in filename:
        return JSONResponse(status_code=400, content={"error": "Invalid filename"}, headers=NO_CACHE_HEADERS)
    path = f"api/current/{filename}"
    return safe_json_response(path)

@app.get("/api/predictions.json")
async def predictions():
    return safe_json_response("api/predictions.json")

@app.get("/api/current/scorecard.json")
async def scorecard():
    return safe_json_response("api/current/scorecard.json")

@app.get("/api/current/results.json")
async def results():
    return safe_json_response("api/current/results.json")

@app.get("/api/current/formulas.json")
async def formulas():
    return safe_json_response("api/current/formulas.json")

@app.get("/api/current/data.json")
async def data():
    return safe_json_response("api/current/data.json")

@app.get("/api/current/code.json")
async def code():
    return safe_json_response("api/current/code.json")

# Static files
@app.get("/style.css")
async def style_css():
    return safe_text_response("style.css", "text/css")

@app.get("/app.js")
async def app_js():
    return safe_text_response("app.js", "application/javascript")

@app.get("/predictions.js")
async def predictions_js():
    return safe_text_response("predictions.js", "application/javascript")

@app.get("/scoring.js")
async def scoring_js():
    return safe_text_response("scoring.js", "application/javascript")

@app.get("/weekly.js")
async def weekly_js():
    return safe_text_response("weekly.js", "application/javascript")

@app.get("/")
async def root():
    try:
        with open("index.html", "r") as f:
            content = f.read()
        return HTMLResponse(content)
    except FileNotFoundError:
        logger.error("index.html not found")
        return HTMLResponse("<h1>Error: index.html missing</h1>", status_code=500)
    except Exception as e:
        logger.error(f"Error serving index.html: {traceback.format_exc()}")
        return HTMLResponse("<h1>Internal Server Error</h1>", status_code=500)

# Catch-all for 404
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    logger.warning(f"404 for path: {request.url.path}")
    return PlainTextResponse("Not found", status_code=404)

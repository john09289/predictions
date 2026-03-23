#!/usr/bin/env python3
"""
ECM Dome Model — Pipeline v2 Orchestrator
Runs every 6 hours via GitHub Actions.
Fetches live data, updates persistent logs, triggers HTML rebuild.
"""

import json
import os
import subprocess
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "docs", "data")
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

os.makedirs(DATA_DIR, exist_ok=True)

NOW_UTC = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

print(f"ECM Pipeline v2 running at {NOW_UTC}")


# ── HELPERS ──

def load_json(filename, default):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            print(f"  Warning: could not load {filename}: {e}")
    return default


def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved {filename}")


# ── FETCH ALL DATA ──

# Import fetchers from same directory
import sys
sys.path.insert(0, SCRIPTS_DIR)
from fetchers import (
    fetch_kp, fetch_nmp, fetch_aao,
    fetch_noaa_alerts, fetch_sr_image, evaluate_predictions,
)

print("Fetching Kp index...")
kp = fetch_kp()
print(f"  Kp max 24h: {kp['kp_max_24h']} ({kp['storm_class']})")

print("Fetching NMP position...")
nmp = fetch_nmp()
print(f"  NMP: {nmp.get('lat')}°N, {nmp.get('lon')}°E (ratio: {nmp.get('ratio')})")

print("Fetching AAO index...")
aao = fetch_aao()
print(f"  AAO latest: {aao.get('latest')}σ, 7d mean: {aao.get('weekly_mean')}σ")

print("Fetching NOAA alerts...")
alerts = fetch_noaa_alerts()
print(f"  Storm alerts 48h: {alerts['alert_count_48h']}")

print("Fetching SR image (Tomsk)...")
sr = fetch_sr_image()
print(f"  Tomsk live: {sr['tomsk_live']}, amplitude_index: {sr.get('amplitude_index')}, status: {sr.get('status')}")


# ── WRITE live_data.json ──

live_data = {
    "updated": NOW_UTC,
    "date": TODAY,
    "kp": kp,
    "nmp": nmp,
    "aao": aao,
    "alerts": alerts,
    "schumann": sr,
}
save_json("live_data.json", live_data)


# ── UPDATE PERSISTENT LOGS ──

# NMP log — append once per calendar month if data is newer than last entry
nmp_log = load_json("nmp_log.json", [])
if nmp.get("lat") and nmp.get("year"):
    # Use today's UTC calendar month as the key (not the NP.xy year which may lag)
    month_key = datetime.now(timezone.utc).strftime("%Y-%m")
    last_month = nmp_log[-1].get("month") if nmp_log else None
    # Only append if this month is strictly after the last logged month
    if last_month is None or month_key > last_month:
        nmp_log.append({
            "month": month_key,
            "lat": nmp.get("lat"),
            "lon": nmp.get("lon"),
            "delta_lat": nmp.get("delta_lat"),
            "delta_lon": nmp.get("delta_lon"),
            "ratio": nmp.get("ratio"),
            "fetched": NOW_UTC,
        })
        save_json("nmp_log.json", nmp_log)

# AAO log — append once per day if new data available
aao_log = load_json("aao_log.json", [])
if aao.get("weekly_mean") is not None:
    last_date = aao_log[-1].get("date") if aao_log else None
    if TODAY != last_date:
        aao_log.append({
            "date": TODAY,
            "latest": aao.get("latest"),
            "weekly_mean": aao.get("weekly_mean"),
            "days_positive_7d": aao.get("days_positive_7d"),
            "fetched": NOW_UTC,
        })
        aao_log = aao_log[-90:]  # rolling 90-day window
        save_json("aao_log.json", aao_log)


# ── STORM LOG — auto-append if G1+ and not already logged today ──

storm_log = load_json("storm_log.json", [])
if kp.get("is_storm"):
    last_storm_date = storm_log[-1].get("date") if storm_log else None
    if TODAY != last_storm_date:
        storm_log.append({
            "date": TODAY,
            "kp_peak": kp["kp_max_24h"],
            "storm_class": kp["storm_class"],
            "phase": "auto-logged",
            "dst": None,
            "sw_speed": None,
            "sr_freq": None,
            "sr_amp_ratio": sr.get("amplitude_index"),
            "tomsk_status": sr.get("status"),
            "sr_suppressed": "YES" if sr.get("suppression_flag") else "PENDING",
            "notes": (
                f"Auto-logged by pipeline. "
                f"Amp index: {sr.get('amplitude_index')}. "
                f"SR status: {sr.get('status')}. Manual review required."
            ),
            "eval": "NEEDS_REVIEW",
        })
        save_json("storm_log.json", storm_log)


# ── PREDICTION EVALUATOR ──

flags = evaluate_predictions(live_data, storm_log)
if flags:
    print(f"Prediction flags ({len(flags)}):")
    for flag in flags:
        marker = "!!" if flag.get("requires_human") else "--"
        print(f"  [{flag['pred']}] {flag['status']}: {flag['detail']} {marker}")
else:
    print("Prediction evaluator: no flags this run.")


# ── REBUILD tracking.html ──

print("Rebuilding tracking.html...")
result = subprocess.run(
    [sys.executable, os.path.join(SCRIPTS_DIR, "build_tracking.py")],
    capture_output=True, text=True, cwd=REPO_ROOT,
)
if result.stdout:
    print(f"  {result.stdout.strip()}")
if result.returncode != 0:
    print(f"  build_tracking.py error:\n{result.stderr}")
    raise SystemExit(1)

print("Pipeline v2 complete.")

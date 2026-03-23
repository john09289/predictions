#!/usr/bin/env python3
"""
ECM Dome Model — Automated Data Pipeline
Runs every 6 hours via GitHub Actions.
Pulls live geomagnetic and SR data, updates tracking.html.
"""

import requests
import json
import re
import os
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

# ── CONFIG ──
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKING_FILE = os.path.join(REPO_ROOT, "docs", "tracking.html")
DATA_DIR = os.path.join(REPO_ROOT, "docs", "data")
DATA_FILE = os.path.join(DATA_DIR, "live_data.json")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW_UTC = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

os.makedirs(DATA_DIR, exist_ok=True)

print(f"ECM Pipeline running at {NOW_UTC}")


# ═══════════════════════════════════════════════════════════════
# DATA FETCHERS
# ═══════════════════════════════════════════════════════════════

def fetch_kp_today():
    """Pull current Kp from NOAA SWPC JSON endpoint."""
    try:
        url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
        r = requests.get(url, timeout=15)
        data = r.json()
        # data[0] = header, rest = [time, kp, observed/estimated, ...]
        # Get last 8 entries (past 24h)
        recent = data[-8:]
        kp_values = []
        for row in recent:
            try:
                kp_values.append(float(row[1]))
            except Exception:
                pass
        kp_max = max(kp_values) if kp_values else 0
        kp_current = kp_values[-1] if kp_values else 0

        if kp_max >= 8:
            storm_class = "G4"
        elif kp_max >= 7:
            storm_class = "G3"
        elif kp_max >= 6:
            storm_class = "G2"
        elif kp_max >= 5:
            storm_class = "G1"
        else:
            storm_class = "G0 (quiet)"

        return {
            "kp_max_24h": kp_max,
            "kp_current": kp_current,
            "storm_class": storm_class,
            "is_storm": kp_max >= 5,
            "recent_values": kp_values,
            "source": "NOAA SWPC",
            "fetched": NOW_UTC,
        }
    except Exception as e:
        print(f"Kp fetch failed: {e}")
        return {"kp_max_24h": "ERROR", "storm_class": "UNKNOWN", "is_storm": False, "fetched": NOW_UTC}


def fetch_nmp():
    """Pull latest NMP position from NOAA NP.xy."""
    try:
        url = "https://www.ngdc.noaa.gov/geomag/data/poles/NP.xy"
        r = requests.get(url, timeout=15)
        lines = r.text.strip().split("\n")

        data_lines = [l for l in lines if l.strip() and not l.startswith("#")]

        entries = []
        for line in data_lines[-5:]:
            parts = line.split()
            if len(parts) >= 3:
                try:
                    entries.append({
                        "year": float(parts[0]),
                        "lat": float(parts[1]),
                        "lon": float(parts[2]),
                    })
                except Exception:
                    pass

        if len(entries) >= 2:
            current = entries[-1]
            prev = entries[-2]
            delta_lat = current["lat"] - prev["lat"]
            delta_lon = current["lon"] - prev["lon"]
            ratio = abs(delta_lon) / abs(delta_lat) if abs(delta_lat) > 0.001 else 99.9

            return {
                "lat": current["lat"],
                "lon": current["lon"],
                "year": current["year"],
                "delta_lat": round(delta_lat, 4),
                "delta_lon": round(delta_lon, 4),
                "ratio": round(ratio, 2),
                "win043_target": ">=2.0x",
                "ratio_ok": ratio >= 2.0,
                "source": "NOAA NGDC NP.xy",
                "fetched": NOW_UTC,
            }
        elif len(entries) == 1:
            return {
                "lat": entries[0]["lat"],
                "lon": entries[0]["lon"],
                "year": entries[0]["year"],
                "ratio": None,
                "fetched": NOW_UTC,
            }
    except Exception as e:
        print(f"NMP fetch failed: {e}")
    return {"lat": "ERROR", "lon": "ERROR", "ratio": "ERROR", "fetched": NOW_UTC}


def fetch_aao():
    """Pull latest AAO index from CPC/NOAA."""
    try:
        url = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/daily_aao.shtml"
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "lxml")

        pre = soup.find("pre")
        if pre:
            text = pre.get_text()
            lines = [l for l in text.strip().split("\n") if l.strip()]

            recent_values = []
            for line in lines[-10:]:
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        val = float(parts[-1])
                        recent_values.append(val)
                    except Exception:
                        pass

            if recent_values:
                weekly_mean = sum(recent_values[-7:]) / len(recent_values[-7:])
                latest = recent_values[-1]
                return {
                    "latest": round(latest, 3),
                    "weekly_mean": round(weekly_mean, 3),
                    "days_positive_7d": sum(1 for v in recent_values[-7:] if v > 0),
                    "dome_target": ">+0.3sigma rolling",
                    "fetched": NOW_UTC,
                    "source": "CPC/NOAA AAO",
                }
    except Exception as e:
        print(f"AAO fetch failed: {e}")
    return {"latest": "ERROR", "weekly_mean": "ERROR", "fetched": NOW_UTC}


def fetch_noaa_alerts():
    """Pull NOAA space weather alerts for storm detection."""
    try:
        url = "https://services.swpc.noaa.gov/products/alerts.json"
        r = requests.get(url, timeout=15)
        alerts = r.json()

        storm_alerts = []
        for alert in alerts[:20]:
            msg = alert.get("message", "")
            issue_time = alert.get("issue_datetime", "")

            if any(kw in msg for kw in ["Geomagnetic Storm", "G1", "G2", "G3", "G4", "G5"]):
                storm_alerts.append({
                    "time": issue_time,
                    "summary": msg[:200].replace("\n", " "),
                })

        return {
            "recent_storm_alerts": storm_alerts[:5],
            "alert_count_48h": len(storm_alerts),
            "fetched": NOW_UTC,
        }
    except Exception as e:
        print(f"Alert fetch failed: {e}")
    return {"recent_storm_alerts": [], "alert_count_48h": 0, "fetched": NOW_UTC}


def check_schumann_status():
    """Check sos70.ru for Schumann status via HTTP head request."""
    try:
        url = "https://sos70.ru/provider.php?file=sra.jpg"
        r = requests.head(url, timeout=10)
        if r.status_code == 200:
            return {
                "tomsk_live": True,
                "status": "Live — check manually at sos70.ru/provider.php?file=sra.jpg",
                "heartmath_backup": "https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/",
                "fetched": NOW_UTC,
            }
    except Exception:
        pass
    return {
        "tomsk_live": False,
        "status": "Tomsk unreachable — use HeartMath backup",
        "heartmath_backup": "https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/",
        "fetched": NOW_UTC,
    }


# ═══════════════════════════════════════════════════════════════
# PULL ALL DATA
# ═══════════════════════════════════════════════════════════════

print("Fetching Kp index...")
kp = fetch_kp_today()
print(f"  Kp max 24h: {kp['kp_max_24h']} ({kp['storm_class']})")

print("Fetching NMP position...")
nmp = fetch_nmp()
print(f"  NMP: {nmp.get('lat')}°N, {nmp.get('lon')}°E (ratio: {nmp.get('ratio')})")

print("Fetching AAO index...")
aao = fetch_aao()
print(f"  AAO latest: {aao.get('latest')}σ, 7d mean: {aao.get('weekly_mean')}σ")

print("Fetching NOAA alerts...")
alerts = fetch_noaa_alerts()
print(f"  Storm alerts (48h): {alerts['alert_count_48h']}")

print("Checking Schumann status...")
sr = check_schumann_status()
print(f"  Tomsk live: {sr['tomsk_live']}")

# Save JSON
live_data = {
    "updated": NOW_UTC,
    "date": TODAY,
    "kp": kp,
    "nmp": nmp,
    "aao": aao,
    "alerts": alerts,
    "schumann": sr,
}

with open(DATA_FILE, "w") as f:
    json.dump(live_data, f, indent=2)
print(f"Saved {DATA_FILE}")


# ═══════════════════════════════════════════════════════════════
# GENERATE STATUS BAR HTML
# ═══════════════════════════════════════════════════════════════

def kp_color(kp_val):
    try:
        k = float(kp_val)
        if k >= 7: return "#e74c3c"
        if k >= 5: return "#e67e22"
        if k >= 3: return "#f1c40f"
        return "#2ecc71"
    except Exception:
        return "#888"


def ratio_color(ratio):
    try:
        r = float(ratio)
        if r >= 2.0: return "#2ecc71"
        if r >= 1.5: return "#f1c40f"
        return "#e74c3c"
    except Exception:
        return "#888"


storm_active = kp.get("is_storm", False)
storm_banner = ""
if storm_active:
    storm_banner = (
        f'\n<div style="background:#1a0000;border-left:4px solid #e74c3c;'
        f'padding:0.75rem 1.5rem;margin-bottom:1rem;font-size:0.85rem;color:#e74c3c;">'
        f'&#9889; <strong>ACTIVE STORM: {kp["storm_class"]} (Kp {kp["kp_max_24h"]})</strong>'
        f' &mdash; Check HeartMath for SR suppression. Log to DW-001 and DW-006.'
        f' This is a PRED-SR-SUPPRESS test event.'
        f' &rarr; <a href="https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/"'
        f' style="color:#e74c3c;">HeartMath GCI</a></div>'
    )

nmp_lat = nmp.get("lat", "?")
nmp_lon = nmp.get("lon", "?")
nmp_ratio = nmp.get("ratio", "?")
aao_mean = aao.get("weekly_mean", "?")
aao_color = "#2ecc71" if isinstance(aao_mean, float) and aao_mean > 0.3 else "#888"
tomsk_color = "#2ecc71" if sr["tomsk_live"] else "#e74c3c"
tomsk_label = "Live" if sr["tomsk_live"] else "Down"
alert_color = "#e74c3c" if alerts["alert_count_48h"] > 0 else "#2ecc71"

status_bar_html = (
    f'<div id="live-status" style="display:flex;flex-wrap:wrap;gap:1rem;'
    f'padding:0.75rem 1rem;background:#0d0d1a;border:1px solid #1a1a2e;'
    f'border-radius:6px;margin-bottom:1.5rem;font-size:0.82rem;">'
    f'<span style="color:#555;align-self:center;">&#x1F504; Auto-updated {NOW_UTC}</span>'
    f'<span style="background:#111;padding:3px 10px;border-radius:4px;">'
    f'Kp: <strong style="color:{kp_color(kp["kp_max_24h"])};">{kp["kp_max_24h"]} ({kp["storm_class"]})</strong>'
    f'</span>'
    f'<span style="background:#111;padding:3px 10px;border-radius:4px;">'
    f'NMP: <strong>{nmp_lat}&deg;N, {nmp_lon}&deg;E</strong>'
    f'&nbsp;ratio: <strong style="color:{ratio_color(nmp_ratio)};">{nmp_ratio}&times;</strong>'
    f'</span>'
    f'<span style="background:#111;padding:3px 10px;border-radius:4px;">'
    f'AAO: <strong style="color:{aao_color};">{aao_mean}&sigma; (7d)</strong>'
    f'</span>'
    f'<span style="background:#111;padding:3px 10px;border-radius:4px;">'
    f'Tomsk: <strong style="color:{tomsk_color};">{tomsk_label}</strong>'
    f'</span>'
    f'<span style="background:#111;padding:3px 10px;border-radius:4px;">'
    f'Alerts 48h: <strong style="color:{alert_color};">{alerts["alert_count_48h"]}</strong>'
    f'</span>'
    f'</div>'
    f'{storm_banner}'
)


# ═══════════════════════════════════════════════════════════════
# INJECT INTO tracking.html
# ═══════════════════════════════════════════════════════════════

with open(TRACKING_FILE, "r", encoding="utf-8") as f:
    html = f.read()

STATUS_MARKER = '<div id="live-status"'

if STATUS_MARKER in html:
    # Replace existing block: find it and replace up to its closing </div>
    start = html.index(STATUS_MARKER)
    depth = 0
    found_end = start
    for i in range(start, len(html) - 5):
        if html[i:i+4] == "<div":
            depth += 1
        elif html[i:i+6] == "</div>":
            depth -= 1
            if depth == 0:
                found_end = i + 6
                break
    # Also consume an immediately following storm banner div if present
    tail = html[found_end:]
    storm_div = '<div style="background:#1a0000'
    if tail.lstrip().startswith(storm_div):
        # consume the storm banner too
        offset = html.index(storm_div, found_end)
        depth = 0
        for i in range(offset, len(html) - 5):
            if html[i:i+4] == "<div":
                depth += 1
            elif html[i:i+6] == "</div>":
                depth -= 1
                if depth == 0:
                    found_end = i + 6
                    break
    html = html[:start] + status_bar_html + html[found_end:]
else:
    # Inject after the model stats bar (the div that contains "Last updated:")
    inject_marker = "Last updated:</strong>"
    if inject_marker in html:
        pos = html.index(inject_marker)
        end_pos = html.index("</div>", pos) + 6
        html = html[:end_pos] + "\n" + status_bar_html + html[end_pos:]
    else:
        # Fallback: inject right after <h1>
        h1_end = html.index("</h1>") + 5
        html = html[:h1_end] + "\n" + status_bar_html + html[h1_end:]

# Update the "Last updated" date stamp in the stats bar
html = re.sub(
    r'(<strong>Last updated:</strong>)[^<]*',
    rf'\g<1> {TODAY}',
    html,
)

with open(TRACKING_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated {TRACKING_FILE}")
print("Pipeline complete.")

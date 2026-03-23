#!/usr/bin/env python3
"""
ECM Pipeline v2 — Data Fetchers
All data fetchers with robust fallbacks + SR image pixel analysis + prediction evaluator.
"""

import requests
import io
from datetime import datetime, timezone

NOW_UTC = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def fetch_kp():
    """Pull current Kp from NOAA SWPC JSON endpoint."""
    try:
        url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
        r = requests.get(url, timeout=15)
        data = r.json()
        recent = data[-8:]  # last 24h (3h intervals)
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
        print(f"  Kp fetch failed: {e}")
        return {"kp_max_24h": 0, "storm_class": "UNKNOWN", "is_storm": False, "fetched": NOW_UTC}


def fetch_nmp():
    """
    Pull latest NMP position from NOAA NP.xy.
    Uses heuristic column detection to handle format variations.
    """
    try:
        url = "https://www.ngdc.noaa.gov/geomag/data/poles/NP.xy"
        r = requests.get(url, timeout=15)
        lines = r.text.strip().split("\n")
        data_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]

        entries = []
        for line in data_lines[-6:]:
            parts = line.split()
            if len(parts) < 3:
                continue
            try:
                vals = []
                for p in parts[:4]:
                    try:
                        vals.append(float(p))
                    except Exception:
                        break

                if len(vals) < 3:
                    continue

                # Auto-detect columns by value ranges
                year_val = lat_val = lon_val = None
                used = set()
                for i, v in enumerate(vals):
                    if 1900 <= v <= 2200 and year_val is None:
                        year_val = v
                        used.add(i)
                for i, v in enumerate(vals):
                    if i in used:
                        continue
                    if 80 <= v <= 90 and lat_val is None:
                        lat_val = v
                        used.add(i)
                for i, v in enumerate(vals):
                    if i in used:
                        continue
                    if -180 <= v <= 360 and lon_val is None:
                        lon_val = v
                        used.add(i)

                if year_val is not None and lat_val is not None and lon_val is not None:
                    # Normalize lon to 0-360
                    if lon_val < 0:
                        lon_val += 360
                    entries.append({"year": year_val, "lat": lat_val, "lon": round(lon_val, 3)})
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
                "source": "NOAA NGDC NP.xy",
                "fetched": NOW_UTC,
            }
    except Exception as e:
        print(f"  NMP fetch failed: {e}")
    return {"lat": None, "lon": None, "ratio": None, "fetched": NOW_UTC}


def fetch_aao():
    """Pull latest AAO index from CPC/NOAA — multi-URL fallback."""
    def _parse_aao_text(text):
        recent_values = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#") or line.lower().startswith("year"):
                continue
            parts = line.split()
            for part in reversed(parts):
                try:
                    val = float(part)
                    if -10 < val < 10:
                        recent_values.append(val)
                        break
                except Exception:
                    continue
        return recent_values

    for url in [
        "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/monthly.aao.index.b79.current.ascii",
        "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/daily_aao.shtml",
        "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/aao.shtml",
    ]:
        try:
            r = requests.get(url, timeout=15)
            recent_values = _parse_aao_text(r.text)
            if len(recent_values) >= 7:
                last7 = recent_values[-7:]
                return {
                    "latest": round(recent_values[-1], 3),
                    "weekly_mean": round(sum(last7) / len(last7), 3),
                    "days_positive_7d": sum(1 for v in last7 if v > 0),
                    "source": f"CPC/NOAA ({url.split('/')[-1]})",
                    "fetched": NOW_UTC,
                }
            print(f"  AAO: insufficient values from {url} ({len(recent_values)} found)")
        except Exception as e:
            print(f"  AAO attempt failed ({url}): {e}")

    return {
        "latest": None,
        "weekly_mean": None,
        "days_positive_7d": None,
        "source": "CPC/NOAA — all attempts failed",
        "fetched": NOW_UTC,
    }


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
                    "summary": msg[:200].replace("\n", " ").replace("\r", " "),
                })
        return {
            "recent_storm_alerts": storm_alerts[:5],
            "alert_count_48h": len(storm_alerts),
            "fetched": NOW_UTC,
        }
    except Exception as e:
        print(f"  Alert fetch failed: {e}")
    return {"recent_storm_alerts": [], "alert_count_48h": 0, "fetched": NOW_UTC}


def fetch_sr_image():
    """
    Download Tomsk SR amplitude image (sra.jpg) and analyze pixel brightness.
    High brightness = active SR; low brightness = suppressed.
    Samples the right third of the image (most recent time window).
    Falls back to HEAD check if Pillow unavailable.
    """
    result = {
        "tomsk_live": False,
        "amplitude_index": None,
        "suppression_flag": False,
        "heartmath_backup": "https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/",
        "status": "Not analyzed",
        "fetched": NOW_UTC,
    }
    url = "https://sos70.ru/provider.php?file=sra.jpg"
    try:
        from PIL import Image
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            result["status"] = f"HTTP {r.status_code}"
            return result

        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        w, h = img.size

        # Sample right third, middle 60% vertically (signal band)
        pixels = []
        for x in range(int(w * 0.67), w):
            for y in range(int(h * 0.2), int(h * 0.8)):
                px = img.getpixel((x, y))
                brightness = (px[0] + px[1] + px[2]) / 3
                pixels.append(brightness)

        if pixels:
            avg_brightness = sum(pixels) / len(pixels)
            # Normalize: 128 = baseline 1.0
            amplitude_index = round(avg_brightness / 128.0, 3)
            suppressed = amplitude_index < 0.7
            result.update({
                "tomsk_live": True,
                "amplitude_index": amplitude_index,
                "suppression_flag": suppressed,
                "status": "Suppressed (auto-flagged — needs human confirm)" if suppressed else "Normal",
                "pixel_count": len(pixels),
            })
    except ImportError:
        # Pillow not available — HEAD check only
        try:
            r = requests.head(url, timeout=10)
            if r.status_code == 200:
                result.update({
                    "tomsk_live": True,
                    "status": "Live — image analysis requires Pillow",
                })
        except Exception:
            result["status"] = "Tomsk unreachable"
    except Exception as e:
        print(f"  SR image analysis failed: {e}")
        result["status"] = f"Error: {e}"
        # Attempt HEAD fallback
        try:
            r = requests.head(url, timeout=10)
            if r.status_code == 200:
                result["tomsk_live"] = True
        except Exception:
            pass
    return result


def evaluate_predictions(live_data, storm_log):
    """
    Auto-flag prediction candidates for human review.
    NEVER auto-confirms — only generates CANDIDATE flags.
    Returns list of flagged items.
    """
    flags = []

    kp = live_data.get("kp", {})
    aao = live_data.get("aao", {})
    sr = live_data.get("schumann", {})

    # PRED-SR-SUPPRESS: G3+ storm — check SR amplitude index
    if kp.get("is_storm") and kp.get("kp_max_24h", 0) >= 7:
        amp = sr.get("amplitude_index")
        if amp is not None:
            if amp < 0.7:
                flags.append({
                    "pred": "PRED-SR-SUPPRESS",
                    "status": "CANDIDATE_CONFIRM",
                    "detail": f"G3+ storm Kp={kp.get('kp_max_24h')} + amplitude_index={amp} < 0.7",
                    "requires_human": True,
                })
            else:
                flags.append({
                    "pred": "PRED-SR-SUPPRESS",
                    "status": "CANDIDATE_DISCONFIRM",
                    "detail": f"G3+ storm Kp={kp.get('kp_max_24h')} but amplitude_index={amp} >= 0.7",
                    "requires_human": True,
                })

    # DW-003 AAO: monitor weekly mean trend
    weekly_mean = aao.get("weekly_mean")
    if weekly_mean is not None:
        if weekly_mean > 1.5:
            flags.append({
                "pred": "DW-003-AAO",
                "status": "STRONG_POSITIVE",
                "detail": f"weekly_mean={weekly_mean}σ >> +0.3σ target",
                "requires_human": False,
            })
        elif weekly_mean < -0.5:
            flags.append({
                "pred": "DW-003-AAO",
                "status": "WATCH_NEGATIVE",
                "detail": f"weekly_mean={weekly_mean}σ — monitor; dome predicts sustained positive",
                "requires_human": True,
            })

    return flags

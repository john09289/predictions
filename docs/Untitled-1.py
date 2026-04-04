#!/usr/bin/env python3
"""
FIXED κ-coupling data acquisition — corrected endpoints for each failure.
Run this on your machine. No bypasses, no auth tricks — just correct URLs.
"""
import requests, ftplib, io, os
from pathlib import Path
DATA = Path("./kappa_data"); DATA.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════
# FIX 1: INTERMAGNET — use anonymous FTP, not broken HTTP API
# The BGS HTTP GIN API returns 400 for historical data because
# the 'dataDuration' parameter needs to be in minutes as integer,
# AND historical data requires 'publicationState=definitive' not 'reported'
# SIMPLEST FIX: anonymous FTP — always worked, still works
# ═══════════════════════════════════════════════════════════
def fetch_bou_ftp(date="2003-10-30"):
    """
    BOU 1-minute definitive data via anonymous FTP.
    No credentials. No API. Direct file download.
    File path: /minute/bou/2003/bou2003303.min  (DOY 303 = Oct 30)
    """
    out = DATA / f"BOU_{date}_H.txt"
    if out.exists():
        print(f"Cached: {out}"); return out

    import datetime as dt
    d = dt.datetime.strptime(date, "%Y-%m-%d")
    doy = d.timetuple().tm_yday
    year = d.year
    filename = f"bou{year}{doy:03d}.min"
    ftp_path = f"/minute/bou/{year}/{filename}"

    print(f"FTP: imag-ftp.bgs.ac.uk{ftp_path}")
    try:
        ftp = ftplib.FTP("imag-ftp.bgs.ac.uk")
        ftp.login("ftp", "your@email.com")      # anonymous login
        buf = io.BytesIO()
        ftp.retrbinary(f"RETR {ftp_path}", buf.write)
        ftp.quit()
        out.write_bytes(buf.getvalue())
        print(f"  ✓ Saved {len(buf.getvalue())} bytes → {out}")
        return out
    except Exception as e:
        print(f"  ✗ FTP failed: {e}")
        return None

# ═══════════════════════════════════════════════════════════
# FIX 2: INTERMAGNET HAPI endpoint (alternative to FTP)
# Completely different URL from the broken GINServices API
# ═══════════════════════════════════════════════════════════
def fetch_bou_hapi(date="2003-10-30"):
    """
    INTERMAGNET HAPI endpoint — separate from GINServices, works for historical.
    """
    out = DATA / f"BOU_{date}_HAPI.json"
    if out.exists():
        print(f"Cached: {out}"); return out

    url = (f"https://imag-data.bgs.ac.uk/GIN_V1/hapi/data"
           f"?id=BOU/definitive/PT1M/H"
           f"&time.min={date}T00:00:00Z"
           f"&time.max={date}T23:59:00Z"
           f"&format=json")
    print(f"HAPI: {url}")
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            out.write_text(r.text)
            print(f"  ✓ {len(r.text)} bytes")
            return out
        else:
            print(f"  ✗ HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"  ✗ {e}")
    return None

# ═══════════════════════════════════════════════════════════
# FIX 3: GRACE L1A — correct collection name + correct CMR query
# The collection 'GRACE_L1A_GRAV_JPL_RL03' does exist for 2003
# The earthaccess search was probably hitting wrong provider or collection
# ═══════════════════════════════════════════════════════════
def find_grace_l1a_cmr():
    """
    Query NASA CMR directly — no earthaccess library needed.
    Find the exact granule URLs for GRACE-A ACC1A Oct 29-30 2003.
    """
    print("\nSearching NASA CMR for GRACE L1A ACC1A 2003...")
    
    # Try multiple collection short names — NASA renamed things
    collections = [
        "GRACE_L1A_GRAV_JPL_RL03",
        "GRACE_L1A_GRAV_JPL_RL04", 
        "GRACE-FO_L1A_GRAV_JPL_RL04",
    ]
    
    for coll in collections:
        url = (f"https://cmr.earthdata.nasa.gov/search/granules.json"
               f"?short_name={coll}"
               f"&temporal=2003-10-29T00:00:00Z,2003-10-31T00:00:00Z"
               f"&page_size=20")
        try:
            r = requests.get(url, timeout=15)
            data = r.json()
            hits = data.get("feed", {}).get("entry", [])
            print(f"  {coll}: {len(hits)} granules found")
            for g in hits[:3]:
                print(f"    → {g.get('title','?')}")
                for link in g.get("links", []):
                    if "ACC" in link.get("href","") or ".dat" in link.get("href",""):
                        print(f"      URL: {link['href']}")
        except Exception as e:
            print(f"  {coll}: error — {e}")

# ═══════════════════════════════════════════════════════════
# FIX 4: GRACE L1A — podaac-data-downloader correct command
# The issue was likely wrong collection or missing date format
# ═══════════════════════════════════════════════════════════
def print_correct_grace_commands():
    print("""
═══════════════════════════════════════════════════════════
CORRECT GRACE L1A DOWNLOAD COMMANDS
═══════════════════════════════════════════════════════════

The earthaccess 'Granules found: 0' means wrong collection name.
Try these exact commands:

# Option A — podaac-data-downloader (not subscriber):
podaac-data-downloader \\
  -c GRACE_L1A_GRAV_JPL_RL03 \\
  -d ./kappa_data/grace_acc \\
  -sd 2003-10-29T00:00:00Z \\
  -ed 2003-10-31T23:59:59Z

# Option B — direct CMR search in browser:
https://cmr.earthdata.nasa.gov/search/granules?
  short_name=GRACE_L1A_GRAV_JPL_RL03&
  temporal=2003-10-29T00:00:00Z,2003-10-31T00:00:00Z

# Option C — Earthdata Search UI (manual):
https://search.earthdata.nasa.gov/search?q=GRACE+L1A+ACC1A+2003

# Option D — GFZ ISDC (separate copy of L1A, sometimes more accessible):
https://isdc.gfz.de/grace/

═══════════════════════════════════════════════════════════
GFZ SFTP AUTH FIX
═══════════════════════════════════════════════════════════

The 'Authentication failed' is likely expired password or
the account needs re-registration for SFTP (separate from web).

Fix: Go to https://isdc.gfz.de/grace/ → Register/Login
     Check if SFTP access requires separate application.
     GFZ IGETS page: https://igets-data.u-strasbg.fr/

Alternative — IGETS data is ALSO available via:
  https://isdc.gfz-potsdam.de/igets-data-base/

Re-register at: https://igets-data.u-strasbg.fr/pub/REGISTRATION/
Then request SFTP key authentication (not password).
""")

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("KAPPA TEST — FIXED DATA ACQUISITION")
    print()

    # Try FTP first (most reliable for historical INTERMAGNET)
    f1 = fetch_bou_ftp("2003-10-30")

    # If FTP fails, try HAPI
    if not f1:
        print("FTP failed, trying HAPI endpoint...")
        f1 = fetch_bou_hapi("2003-10-30")

    # CMR search for GRACE
    find_grace_l1a_cmr()

    # Print correct manual commands
    print_correct_grace_commands()

    if f1:
        print(f"\n✓ INTERMAGNET data secured: {f1}")
        print("Next: download GRACE ACC1A then run the κ test from grace_kappa_test.py")
    else:
        print("\n✗ INTERMAGNET still failing — check network or use manual download:")
        print("  https://imag-data.bgs.ac.uk/GIN_V1/GINForms2")
        print("  Select: BOU | 2003-10-30 | 1-minute | H | Definitive")
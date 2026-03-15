#!/usr/bin/env python3
import urllib.request
import urllib.error
import urllib.parse
import json
import os
import datetime

# --- CONFIGURATION ---
SUPABASE_URL = "https://qiwmcggdbouqwpobpiqh.supabase.co"

def get_secret_key():
    creds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".supabase_credentials")
    try:
        with open(creds_path, "r") as f:
            content = f.read()
            # Extract SUPABASE_SECRET_KEY="sb_secret_..."
            for line in content.splitlines():
                if line.startswith("SUPABASE_SECRET_KEY="):
                    return line.split("=")[1].strip('"\'')
    except FileNotFoundError:
        print("Error: .supabase_credentials file not found.")
        exit(1)
    return None

def fetch_analytics():
    key = get_secret_key()
    if not key:
        print("Error: Could not find secret key.")
        exit(1)

    url = f"{SUPABASE_URL}/rest/v1/page_views?order=created_at.desc&limit=50"
    
    req = urllib.request.Request(url)
    req.add_header('apikey', key)
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('Accept', 'application/json')

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.URLError as e:
        print(f"Failed to connect to Supabase: {e.reason}")
        exit(1)

def print_dashboard():
    print("=" * 100)
    print(" 📡 DOME REGISTRY PRIVATE ANALYTICS DASHBOARD ".center(100, "="))
    print("=" * 100)
    
    data = fetch_analytics()
    
    if not data:
        print("\nNo views recorded yet. Go visit your site at https://john09289.github.io/predictions to test it!\n")
        return

    # Filter out test views from the AI agent if any exist
    data = [row for row in data if "Agent Tester" not in row.get("user_agent", "")]

    print(f"\nTotal Real Visitors Retrieved: {len(data)}\n")
    print(f"{'Time (UTC)':<22} | {'Path':<25} | {'Timezone':<20} | {'Platform'}")
    print("-" * 100)

    for row in data[:20]: # Show top 20
        # Format date
        raw_date = row.get("created_at", "")
        formatted_date = raw_date[:19].replace('T', ' ') if raw_date else "Unknown"
        
        path = row.get("path", "/")[:25]
        tz = row.get("timezone", "Unknown")[:20]
        
        ua = row.get("user_agent", "")
        platform = "Unknown"
        if 'Windows' in ua: platform = "Windows"
        elif 'Mac OS' in ua: platform = "Mac OS"
        elif 'Linux' in ua: platform = "Linux"
        elif 'Android' in ua: platform = "Android"
        elif 'iPhone' in ua or 'iPad' in ua: platform = "iOS"

        print(f"{formatted_date:<22} | {path:<25} | {tz:<20} | {platform}")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    print_dashboard()

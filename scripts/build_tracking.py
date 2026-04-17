#!/usr/bin/env python3
"""
ECM Pipeline v2 — Tracking HTML Builder
Rebuilds docs/tracking.html from scratch each run.
Reads all docs/data/*.json — never injects into existing HTML.
"""

import json
import os
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "docs", "data")
TRACKING_FILE = os.path.join(REPO_ROOT, "docs", "tracking.html")

NOW_UTC = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ── DATA LOADING ──

def load(filename, default):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            print(f"  Warning: could not load {filename}: {e}")
    return default


live     = load("live_data.json", {})
storm_log  = load("storm_log.json", [])
nmp_log    = load("nmp_log.json", [])
aao_log    = load("aao_log.json", [])
dw006_log  = load("dw006_log.json", [])
dst_log    = load("dst_log.json", [])
daily_review = load("daily_review.json", {})
ai_manifest = {}
manifest_path = os.path.join(REPO_ROOT, "docs", "ai_manifest.json")
if os.path.exists(manifest_path):
    try:
        with open(manifest_path) as f:
            ai_manifest = json.load(f)
    except Exception as e:
        print(f"  Warning: could not load ai_manifest.json: {e}")

kp_data   = live.get("kp", {})
nmp_data  = live.get("nmp", {})
aao_data  = live.get("aao", {})
alerts    = live.get("alerts", {})
sr_data   = live.get("schumann", {})
updated   = live.get("updated", "—")
registry_counts = ai_manifest.get("counts", {})
registry_confirmed = registry_counts.get("confirmed", 69)
registry_refined = registry_counts.get("refined", 4)
registry_ratio = registry_counts.get("registry_accuracy_pct", 94.5)
review_generated = daily_review.get("generated_human", updated)
review_brief = daily_review.get("ai_brief", {})
review_summary = review_brief.get("summary", "")
review_actions = review_brief.get("next_actions", [])
review_focus = review_brief.get("prediction_focus", [])
review_provider = review_brief.get("provider", "local")
review_model = review_brief.get("model", "deterministic-summary")
accuracy_review = daily_review.get("accuracy_review", {})
monitor_score = accuracy_review.get("monitor_score_pct", "—")
avg_monitor_score = accuracy_review.get("avg_monitor_score_7d", "—")
passed_over_scored = accuracy_review.get("passed_over_scored", "—")


# ── COLOR HELPERS ──

def kp_color(val):
    try:
        k = float(str(val).replace("~", "").split("\u2013")[-1].split("-")[-1])
        if k >= 7: return "var(--accent-red)"
        if k >= 5: return "var(--accent-orange, #e67e22)"
        if k >= 3: return "var(--accent-gold)"
        return "var(--accent-green)"
    except Exception:
        return "var(--text-secondary)"

def ratio_color(val):
    try:
        r = float(str(val).split()[0])
        if r >= 2.0: return "var(--accent-green)"
        if r >= 1.5: return "var(--accent-gold)"
        return "var(--accent-red)"
    except Exception:
        return "var(--text-secondary)"

def aao_color(val):
    try:
        v = float(val)
        return "var(--accent-green)" if v > 0.3 else ("var(--accent-red)" if v < -0.3 else "var(--text-secondary)")
    except Exception:
        return "var(--text-secondary)"


# ── TABLE ROW BUILDERS ──


def dw001_rows():
    rows = []
    for e in storm_log:
        date = e.get("date", "?")
        kp_val = e.get("kp_peak", "?")
        sc = str(e.get("storm_class", "?"))
        phase = e.get("phase") or "\u2014"
        dst = e.get("dst") or "\u2014"
        sw = e.get("sw_speed") or "\u2014"
        sr_freq = e.get("sr_freq")
        sr_amp = e.get("sr_amp_ratio")
        tomsk = e.get("tomsk_status") or "\u2014"
        suppressed = str(e.get("sr_suppressed", "PENDING")).upper()
        notes = e.get("notes", "")

        sc_class = "suppressed" if any(x in sc for x in ("G3", "G4", "G5")) else (
            "normal" if "G0" in sc else "")

        # SR freq cell
        if sr_freq is None:
            freq_td = '<td class="unknown-cell">&mdash;</td>'
        else:
            freq_td = f"<td>{sr_freq}</td>"

        # SR amplitude cell
        if sr_amp is None:
            amp_td = '<td class="pending-cell">PENDING</td>'
        elif "suppress" in str(sr_amp).lower() or str(sr_amp).startswith("<0.7"):
            amp_td = f'<td class="suppressed">{sr_amp}</td>'
        elif "baseline" in str(sr_amp).lower() or str(sr_amp).startswith("1.00"):
            amp_td = f'<td class="normal">{sr_amp}</td>'
        else:
            amp_td = f"<td>{sr_amp}</td>"

        # Tomsk status cell
        if tomsk in ("Unknown", "Saturated/unknown", "\u2014"):
            tomsk_td = f'<td class="unknown-cell">{tomsk}</td>'
        else:
            tomsk_td = f'<td class="normal">{tomsk}</td>'

        # SR suppressed cell
        if suppressed == "YES":
            supp_td = '<td class="suppressed">&#10003; YES</td>'
        elif suppressed in ("N/A", "NA"):
            supp_td = '<td class="normal">N/A</td>'
        elif suppressed == "CANDIDATE":
            supp_td = '<td class="pending-tag" style="font-style:italic;">&#9888; CANDIDATE &mdash; verify HeartMath</td>'
        elif suppressed == "PENDING":
            supp_td = '<td class="pending-cell">&#10067; PENDING</td>'
        else:
            supp_td = f"<td>{suppressed}</td>"

        rows.append(f"""      <tr>
        <td>{date}</td>
        <td>{kp_val}</td>
        <td class="{sc_class}">{sc}</td>
        <td>{phase}</td>
        <td>{dst}</td>
        <td>{sw}</td>
        {freq_td}
        {amp_td}
        {tomsk_td}
        {supp_td}
        <td>{notes}</td>
      </tr>""")
    return "\n".join(rows)


def dw002_rows():
    rows = []
    for e in nmp_log:
        month = e.get("month", "?")
        lat = e.get("lat", "?")
        lon = e.get("lon", "?")
        dl = e.get("delta_lat")
        dlo = e.get("delta_lon")
        ratio = e.get("ratio")
        rolling = e.get("rolling_4mo") or "\u2014"
        vs_pred = e.get("vs_pred", "On track")

        dl_td = "<td>&mdash;</td>" if dl is None else f"<td>{dl}</td>"
        dlo_td = "<td>&mdash;</td>" if dlo is None else f"<td>{dlo}</td>"
        if ratio is None:
            ratio_td = "<td>&mdash;</td>"
        else:
            rc = ratio_color(ratio)
            ratio_td = f'<td style="color:{rc};font-weight:600;">{ratio}&times;</td>'

        rows.append(f"""      <tr>
        <td>{month}</td>
        <td>{lat}&deg;N</td>
        <td>{lon}&deg;E</td>
        {dl_td}
        {dlo_td}
        {ratio_td}
        <td>{rolling}</td>
        <td class="normal">{vs_pred}</td>
      </tr>""")
    return "\n".join(rows)


def dw003_rows():
    rows = []
    for e in aao_log:
        date = e.get("date", "?")
        wm = e.get("weekly_mean")
        dp = e.get("days_positive_7d", "\u2014")
        notes = e.get("notes", "")

        if isinstance(wm, (int, float)):
            wm_str = f"{wm:+.3f}&sigma;"
            wm_class = "normal" if wm > 0.3 else ("suppressed" if wm < -0.3 else "")
        else:
            wm_str = str(wm) if wm else "\u2014"
            wm_class = ""

        rows.append(f"""      <tr>
        <td>{date}</td>
        <td class="{wm_class}">{wm_str}</td>
        <td>{dp}/7</td>
        <td>&mdash;</td>
        <td>&mdash; (insufficient)</td>
        <td>{notes}</td>
      </tr>""")
    return "\n".join(rows)


def dw006_rows():
    rows = []
    for e in dw006_log:
        date = e.get("date", "?")
        sc = str(e.get("storm_class", "?"))
        kp_val = e.get("kp_peak", "?")
        phase = e.get("phase_checked", "?")
        pct = e.get("sr_suppression_pct")
        confirmed = str(e.get("confirmed", "PENDING")).upper()
        note = e.get("note", "")
        source = e.get("source", "")

        sc_class = "suppressed" if any(x in sc for x in ("G3", "G4", "G5")) else ""
        pct_td = '<td class="pending-cell">PENDING</td>' if not pct else f'<td class="suppressed">{pct}</td>'

        win_tag = f' &mdash; <span class="win-tag">{note}</span>' if note else ""
        if confirmed == "YES":
            conf_td = f'<td class="suppressed">&#10003; YES{win_tag}</td>'
        elif confirmed == "PENDING":
            conf_td = '<td class="pending-cell">&#10067; PRIORITY CHECK</td>'
        else:
            conf_td = f"<td>{confirmed}</td>"

        rows.append(f"""      <tr>
        <td>{date}</td>
        <td class="{sc_class}">{sc}</td>
        <td>{kp_val}</td>
        <td>{phase}</td>
        {pct_td}
        {conf_td}
        <td>{source}</td>
      </tr>""")
    return "\n".join(rows)


def dst_rows():
    rows = []
    for e in dst_log:
        date = e.get("storm_date", "?")
        dst_min = e.get("dst_min") or '<span class="pending-cell">PENDING</span>'
        rec = e.get("recovery_time") or '<span class="pending-cell">PENDING</span>'
        sc = e.get("storm_class", "?")
        saa = e.get("saa_month_after") or '<span class="pending-cell">Check INTERMAGNET</span>'
        coupling = e.get("ecm_coupling") or '<span class="pending-cell">&mdash;</span>'
        source = e.get("source", "")
        rows.append(f"""      <tr>
        <td>{date}</td>
        <td>{dst_min}</td>
        <td>{rec}</td>
        <td>{sc}</td>
        <td>{saa}</td>
        <td>{coupling}</td>
        <td>{source}</td>
      </tr>""")
    return "\n".join(rows)


# ── STATUS BAR ──

kp_max = kp_data.get("kp_max_24h", "?")
storm_class = kp_data.get("storm_class", "?")
nmp_lat = nmp_data.get("lat", "?")
nmp_lon = nmp_data.get("lon", "?")
nmp_ratio = nmp_data.get("ratio", "?")
aao_mean = aao_data.get("weekly_mean")
aao_disp = f"{aao_mean}&sigma;" if aao_mean is not None else "unavailable"
aao_col = aao_color(aao_mean)
tomsk_live = sr_data.get("tomsk_live", False)
tomsk_col = "var(--accent-green)" if tomsk_live else "var(--accent-red)"
tomsk_lbl = "Live" if tomsk_live else "Down"
amp_idx = sr_data.get("amplitude_index")
amp_extra = f"&nbsp;Amp: {amp_idx}" if amp_idx is not None else ""
alert_count = alerts.get("alert_count_48h", 0)
alert_col = "var(--accent-red)" if alert_count > 0 else "var(--accent-green)"

status_bar = f"""<div id="live-status" style="display:flex;flex-wrap:wrap;gap:1rem;padding:0.75rem 1rem;background:var(--bg-code);border:1px solid var(--border-light);border-radius:var(--radius-sm);margin-bottom:1.5rem;font-size:0.82rem;">
  <span style="color:var(--text-tertiary);align-self:center;">&#x1F504; Auto-updated {updated}</span>
  <span style="background:var(--bg-primary);padding:3px 10px;border-radius:4px;border:1px solid var(--border-light);">Kp: <strong style="color:{kp_color(kp_max)};">{kp_max} ({storm_class})</strong></span>
  <span style="background:var(--bg-primary);padding:3px 10px;border-radius:4px;border:1px solid var(--border-light);">NMP: <strong>{nmp_lat}&deg;N, {nmp_lon}&deg;E</strong>&nbsp;ratio: <strong style="color:{ratio_color(nmp_ratio)};">{nmp_ratio}&times;</strong></span>
  <span style="background:var(--bg-primary);padding:3px 10px;border-radius:4px;border:1px solid var(--border-light);">AAO: <strong style="color:{aao_col};">{aao_disp} (7d)</strong></span>
  <span style="background:var(--bg-primary);padding:3px 10px;border-radius:4px;border:1px solid var(--border-light);">Tomsk: <strong style="color:{tomsk_col};">{tomsk_lbl}</strong>{amp_extra}</span>
  <span style="background:var(--bg-primary);padding:3px 10px;border-radius:4px;border:1px solid var(--border-light);">Alerts 48h: <strong style="color:{alert_col};">{alert_count}</strong></span>
</div>"""

daily_review_html = ""
if daily_review:
    actions_html = "".join(
        f"<li>{action}</li>" for action in review_actions[:3]
    ) or "<li>No actions queued.</li>"
    focus_html = "".join(
        f"<li>{item}</li>" for item in review_focus[:3]
    ) or "<li>No prediction focus note yet.</li>"
    daily_review_html = f"""
<section class="tracking-section" id="daily-review">
  <div class="tracking-header">
    <h3>Daily Review &amp; Accuracy Snapshot</h3>
    <span class="cadence-label">Auto-generated</span>
  </div>
  <p class="section-intro">Fresh site summary generated from the canonical registry counts plus the latest live monitor snapshot. If <code>GROQ_API_KEY</code> is configured in GitHub Actions, the narrative summary is AI-written from the structured data; otherwise a deterministic local summary is used.</p>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">Review generated</span><span class="stat-value">{review_generated}</span></div>
    <div class="stat"><span class="stat-label">Registry ratio</span><span class="stat-value">{registry_ratio}%</span></div>
    <div class="stat"><span class="stat-label">Monitor score</span><span class="stat-value">{monitor_score}%</span></div>
    <div class="stat"><span class="stat-label">7d avg monitor score</span><span class="stat-value">{avg_monitor_score}%</span></div>
    <div class="stat"><span class="stat-label">Passed / scored</span><span class="stat-value">{passed_over_scored}</span></div>
    <div class="stat"><span class="stat-label">Review engine</span><span class="stat-value">{review_provider}: {review_model}</span></div>
  </div>
  <div style="padding:1rem 1.5rem;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">
    <div style="background:var(--bg-code);border:1px solid var(--border-light);border-radius:var(--radius-sm);padding:0.9rem 1rem;">
      <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-tertiary);margin-bottom:0.35rem;">Summary</div>
      <div style="font-size:0.84rem;color:var(--text-primary);line-height:1.55;">{review_summary or 'Awaiting first review summary.'}</div>
    </div>
    <div style="background:var(--bg-code);border:1px solid var(--border-light);border-radius:var(--radius-sm);padding:0.9rem 1rem;">
      <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-tertiary);margin-bottom:0.35rem;">Next Actions</div>
      <ul style="margin:0;padding-left:1.1rem;font-size:0.82rem;color:var(--text-primary);line-height:1.55;">{actions_html}</ul>
    </div>
    <div style="background:var(--bg-code);border:1px solid var(--border-light);border-radius:var(--radius-sm);padding:0.9rem 1rem;">
      <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-tertiary);margin-bottom:0.35rem;">Prediction Focus</div>
      <ul style="margin:0;padding-left:1.1rem;font-size:0.82rem;color:var(--text-primary);line-height:1.55;">{focus_html}</ul>
    </div>
  </div>
</section>"""

storm_active = kp_data.get("is_storm", False)
storm_banner = ""
if storm_active:
    storm_banner = f"""<div style="background:#fff5f5;border-left:4px solid var(--accent-red);padding:0.75rem 1.5rem;margin-bottom:1rem;font-size:0.85rem;color:var(--accent-red);border-radius:0 var(--radius-sm) var(--radius-sm) 0;">
  &#9889; <strong>ACTIVE STORM: {storm_class} (Kp {kp_max})</strong> &mdash; Check HeartMath for SR suppression. Log to DW-001 and DW-006. This is a PRED-SR-SUPPRESS test event.
  &rarr; <a href="https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/" style="color:var(--accent-red);">HeartMath GCI</a>
</div>"""

# ── PAGE STATS ──

total_entries = len(storm_log)
storm_days = sum(1 for e in storm_log if e.get("storm_class", "G0") not in ("G0 (quiet)", "G0"))
suppressed_count = sum(1 for e in storm_log if str(e.get("sr_suppressed", "")).upper() == "YES")
pending_sr = sum(1 for e in storm_log if str(e.get("sr_suppressed", "")).upper() == "PENDING")

storms_logged_dw6 = len(dw006_log)
supp_confirmed_dw6 = sum(1 for e in dw006_log if str(e.get("confirmed", "")).upper() == "YES")
supp_pending_dw6 = sum(1 for e in dw006_log if str(e.get("confirmed", "")).upper() == "PENDING")

pending_sr_str = f"{pending_sr} ({', '.join(e['date'] for e in storm_log if str(e.get('sr_suppressed','')).upper()=='PENDING')})" if pending_sr else "0"
suppressed_str = f"{suppressed_count} ({', '.join(e['date'] for e in storm_log if str(e.get('sr_suppressed','')).upper()=='YES')})" if suppressed_count else "0"


# ── BUILD HTML ──

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ECM Tracking Logs &mdash; Daily &amp; Weekly Data</title>
  <link rel="stylesheet" href="style.css">
  <script src="analytics.js"></script>
  <style>
    .tracking-section {{ margin: 2rem 0; border: 1px solid var(--border-light); border-radius: var(--radius-md); overflow: hidden; box-shadow: var(--shadow-card); }}
    .tracking-header {{ background: linear-gradient(135deg, rgba(37,99,235,0.07), rgba(14,165,233,0.05)); padding: 0.9rem 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; border-bottom: 1px solid var(--border-light); }}
    .tracking-header h3 {{ margin: 0; font-size: 1rem; font-family: var(--font-body); font-weight: 600; color: var(--text-heading); }}
    .cadence-label {{ font-size: 0.7rem; background: linear-gradient(135deg, var(--accent-blue), var(--accent-sky)); color: #fff; padding: 3px 10px; border-radius: 10px; white-space: nowrap; font-weight: 600; }}
    .stat-row {{ display: flex; flex-wrap: wrap; gap: 1.5rem; padding: 0.7rem 1.5rem; background: var(--bg-code); border-bottom: 1px solid var(--border-light); font-size: 0.82rem; }}
    .stat {{ display: flex; flex-direction: column; gap: 2px; }}
    .stat-label {{ color: var(--text-tertiary); font-size: 0.67rem; text-transform: uppercase; letter-spacing: 0.05em; }}
    .stat-value {{ font-weight: 600; color: var(--text-primary); }}
    .log-table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; overflow-x: auto; display: block; }}
    .log-table th {{ background: var(--bg-code); padding: 0.45rem 0.75rem; text-align: left; color: var(--text-secondary); font-weight: 600; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid var(--border-medium); white-space: nowrap; }}
    .log-table td {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border-light); vertical-align: top; color: var(--text-primary); }}
    .log-table tr:last-child td {{ border-bottom: none; }}
    .log-table tbody tr:hover td {{ background: var(--bg-card-hover); }}
    .suppressed {{ color: var(--accent-red); font-weight: 600; }}
    .normal {{ color: var(--accent-green); font-weight: 500; }}
    .pending-cell {{ color: var(--text-tertiary); font-style: italic; }}
    .unknown-cell {{ color: var(--text-tertiary); }}
    .add-footer {{ background: var(--bg-code); padding: 0.6rem 1.5rem; font-size: 0.75rem; color: var(--text-secondary); border-top: 1px solid var(--border-light); }}
    .immediate-banner {{ background: #fff8f0; border-left: 3px solid var(--accent-gold-light); padding: 0.75rem 1.5rem; font-size: 0.85rem; color: var(--accent-gold); margin-bottom: 1.5rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; }}
    .immediate-banner a {{ color: var(--accent-gold); }}
    .section-intro {{ color: var(--text-secondary); font-size: 0.85rem; margin: 0; padding: 0.75rem 1.5rem; border-bottom: 1px solid var(--border-light); }}
    .win-tag {{ color: var(--accent-green); font-size: 0.7rem; font-weight: 700; }}
    .pending-tag {{ color: var(--accent-gold); font-size: 0.7rem; }}
    .note-row td {{ background: var(--bg-code); color: var(--text-tertiary); font-size: 0.75rem; font-style: italic; }}
  </style>
</head>
<body>

<nav>
  <a href="index.html">Home</a>
  <a href="wins.html">Wins <span class="nav-badge">{registry_confirmed}</span></a>
  <a href="predictions.html">Predictions</a>
  <a href="tracking.html" class="active">Tracking</a>
  <a href="coordinates.html">Coordinates</a>
  <a href="model.html">Model</a>
  <a href="evolution.html">Evolution</a>
  <a href="context.html">AI Context</a>
</nav>

<h1>ECM Daily &amp; Weekly Tracking Logs</h1>
<p style="color:var(--text-secondary);margin-bottom:1.5rem;">Continuous data collection for real-time model testing. Each entry is a data point &mdash; patterns emerge within weeks. All predictions pre-registered in <a href="predictions.html">predictions.html</a>. Tracking started 2026-03-23.</p>

<div style="display:flex;gap:2rem;flex-wrap:wrap;margin-bottom:1.5rem;font-size:0.85rem;padding:0.75rem 1rem;background:var(--bg-code);border:1px solid var(--border-light);border-radius:var(--radius-sm);">
  <span><strong>Model:</strong> V51.1</span>
  <span><strong>Confirmed:</strong> {registry_confirmed}</span>
  <span><strong>Refined:</strong> {registry_refined}</span>
  <span><strong>Last updated:</strong> {TODAY}</span>
  <span><strong>Tracking entries:</strong> {total_entries}</span>
</div>

{status_bar}
{storm_banner}
{daily_review_html}
<div class="immediate-banner">
  &#9889; <strong>IMMEDIATE ACTION:</strong> Check HeartMath spectrogram for March 22 (G3 storm 0900&ndash;1200 UTC).
  SR suppressed = PRED-SR-SUPPRESS confirmed (2nd event). Not suppressed = update DW-006 and revise model.
  &rarr; <a href="https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/">HeartMath GCI March 22</a>
  &nbsp;|&nbsp; Also check March 23 (G1 isolated, Kp 3&ndash;5).
</div>

<!-- DW-001: MASTER DAILY LOG -->
<section class="tracking-section" id="dw001-log">
  <div class="tracking-header">
    <h3>DW-001 &mdash; Master Daily Geomagnetic + SR Log</h3>
    <span class="cadence-label">Daily</span>
  </div>
  <p class="section-intro">One row per day. Captures all storm-relevant data in one place. SR columns need HeartMath or Tomsk check each morning. Kp and Dst from NOAA. Solar wind from OMNI2/DSCOVR.</p>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">Total entries</span><span class="stat-value">{total_entries}</span></div>
    <div class="stat"><span class="stat-label">Storm days (G1+)</span><span class="stat-value">{storm_days}</span></div>
    <div class="stat"><span class="stat-label">SR suppression confirmed</span><span class="stat-value">{suppressed_str}</span></div>
    <div class="stat"><span class="stat-label">SR pending check</span><span class="stat-value">{pending_sr} days</span></div>
    <div class="stat"><span class="stat-label">Dome predicts</span><span class="stat-value">&gt;75% G1+ &rarr; suppress</span></div>
  </div>
  <table class="log-table">
    <thead>
      <tr>
        <th>Date</th><th>Kp Peak</th><th>Storm Class</th><th>Storm Phase</th>
        <th>Dst (nT)</th><th>SW Speed (km/s)</th><th>SR Freq (Hz)</th>
        <th>SR Amp vs Baseline</th><th>Tomsk Status</th><th>Suppressed?</th><th>Notes / Source</th>
      </tr>
    </thead>
    <tbody>
{dw001_rows()}
      <tr class="note-row">
        <td colspan="11">Add row daily: date | kp_peak | storm_class | phase (initial/main/recovery/quiet) | Dst | SW_speed | SR_freq | SR_amp_ratio (1.0=baseline) | Tomsk_status | suppressed (Y/N/N/A) | notes + source</td>
      </tr>
    </tbody>
  </table>
  <div class="add-footer">
    Sources: Kp/Dst &rarr; <a href="https://www.swpc.noaa.gov">NOAA SWPC</a> |
    Solar wind &rarr; <a href="https://omniweb.gsfc.nasa.gov/ow_min.html">OMNI2</a> |
    SR freq/amp &rarr; <a href="https://sos70.ru/provider.php?file=srf.jpg">Tomsk srf.jpg</a> + <a href="https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/">HeartMath GCI</a>
  </div>
</section>

<!-- DW-002: NMP DRIFT RATIO -->
<section class="tracking-section" id="dw002-log">
  <div class="tracking-header">
    <h3>DW-002 &mdash; NMP Longitudinal:Latitudinal Drift Ratio</h3>
    <span class="cadence-label">Monthly (NOAA NP.xy)</span>
  </div>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">Baseline NMP (2026-02)</span><span class="stat-value">85.778&deg;N, 138.057&deg;E</span></div>
    <div class="stat"><span class="stat-label">WIN-043 ratio</span><span class="stat-value">2.26&times;</span></div>
    <div class="stat"><span class="stat-label">Dome predicts</span><span class="stat-value">&ge;2.0&times; rolling</span></div>
    <div class="stat"><span class="stat-label">Globe predicts</span><span class="stat-value">random walk (no ratio)</span></div>
  </div>
  <table class="log-table">
    <thead>
      <tr><th>Date</th><th>Lat</th><th>Lon</th><th>&Delta;lat (&deg;)</th><th>&Delta;lon (&deg;)</th><th>Monthly Ratio</th><th>4-Month Rolling</th><th>vs PRED-R003</th></tr>
    </thead>
    <tbody>
{dw002_rows()}
      <tr class="note-row">
        <td colspan="8">Pull monthly from <a href="https://www.ngdc.noaa.gov/geomag/data/poles/NP.xy">NOAA NP.xy</a>. Add row each month. PRED-R003 target: 141&ndash;146&deg;E by 2031.</td>
      </tr>
    </tbody>
  </table>
</section>

<!-- DW-003: AAO INDEX -->
<section class="tracking-section" id="dw003-log">
  <div class="tracking-header">
    <h3>DW-003 &mdash; Weekly AAO Index (Roaring 40s Long-Term Bias)</h3>
    <span class="cadence-label">Weekly</span>
  </div>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">Entries</span><span class="stat-value">{len(aao_log)}</span></div>
    <div class="stat"><span class="stat-label">12wk mean</span><span class="stat-value">&mdash; (insufficient data)</span></div>
    <div class="stat"><span class="stat-label">Dome predicts</span><span class="stat-value">&gt;+0.3&sigma; 12wk mean</span></div>
    <div class="stat"><span class="stat-label">Globe predicts</span><span class="stat-value">&asymp;0 (random)</span></div>
  </div>
  <table class="log-table">
    <thead>
      <tr><th>Week End</th><th>Weekly Mean (&sigma;)</th><th>Days Positive</th><th>Days &gt;1&sigma;</th><th>Running 12wk Mean</th><th>Notes</th></tr>
    </thead>
    <tbody>
{dw003_rows()}
      <tr class="note-row">
        <td colspan="6">Continue weekly. Source: <a href="https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/daily_aao.shtml">CPC/NOAA AAO</a>. Dome calls: 12wk mean &gt;+0.3&sigma;. Globe calls: &asymp;0.</td>
      </tr>
    </tbody>
  </table>
</section>

<!-- DW-004: SOLAR WIND vs SR FREQUENCY -->
<section class="tracking-section" id="dw004-log">
  <div class="tracking-header">
    <h3>DW-004 &mdash; Solar Wind Pressure vs SR Frequency (Quiet Days Kp&lt;1)</h3>
    <span class="cadence-label">Log on Kp&lt;1 + SW&gt;8 nPa days only</span>
  </div>
  <p class="section-intro">Separate from storm tracking. Tests whether dome firmament responds to solar wind pressure on calm days. Globe has no mechanism. Log only when Kp&lt;1 AND SW pressure &gt;8 nPa simultaneously.</p>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">Quiet-day entries</span><span class="stat-value">0</span></div>
    <div class="stat"><span class="stat-label">SR baseline</span><span class="stat-value">7.83 Hz</span></div>
    <div class="stat"><span class="stat-label">Dome predicts</span><span class="stat-value">r&sup2;&gt;0.3 at 50 entries</span></div>
  </div>
  <table class="log-table">
    <thead>
      <tr><th>Date</th><th>SW Pressure (nPa)</th><th>Kp</th><th>SR Freq (Hz)</th><th>&Delta; from 7.83 Hz</th><th>Direction</th><th>Notes</th></tr>
    </thead>
    <tbody>
      <tr class="note-row">
        <td colspan="7">Log ONLY on Kp&lt;1 days with SW&gt;8 nPa. Sources: <a href="https://omniweb.gsfc.nasa.gov/ow_min.html">OMNI2</a> (SW pressure) + <a href="https://sos70.ru/provider.php?file=srf.jpg">Tomsk SR freq</a>.</td>
      </tr>
    </tbody>
  </table>
</section>

<!-- DW-005: SAA STATION DECAY -->
<section class="tracking-section" id="dw005-log">
  <div class="tracking-header">
    <h3>DW-005 &mdash; Monthly SAA Station Decay (TTB / TDC / HER)</h3>
    <span class="cadence-label">Monthly (INTERMAGNET)</span>
  </div>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">TTB current rate</span><span class="stat-value">77 nT/yr (WIN-042)</span></div>
    <div class="stat"><span class="stat-label">TDC current rate</span><span class="stat-value">79.7 nT/yr (WIN-041)</span></div>
    <div class="stat"><span class="stat-label">HER current rate</span><span class="stat-value">51.4 nT/yr (WIN-041)</span></div>
    <div class="stat"><span class="stat-label">Dome predicts</span><span class="stat-value">TTB+TDC &ge;50 nT/yr through 2028</span></div>
  </div>
  <table class="log-table">
    <thead>
      <tr><th>Month</th><th>TTB F (nT)</th><th>TDC F (nT)</th><th>HER F (nT)</th><th>TTB Monthly &Delta;</th><th>Annualized Rate</th><th>vs PRED-DECAY-TTB</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>2025 baseline</td>
        <td>~21,730</td>
        <td>~23,100</td>
        <td>~25,400</td>
        <td>&mdash;</td>
        <td>~77 nT/yr</td>
        <td class="normal">&#10003; (WIN-042)</td>
      </tr>
      <tr class="note-row">
        <td colspan="7">Pull monthly from <a href="https://www.intermagnet.org/data-donnee/download-eng.php">INTERMAGNET</a>. TTB = Tsumeb Namibia. TDC = Trindade Island. HER = Hermanus S. Africa.</td>
      </tr>
    </tbody>
  </table>
</section>

<!-- DW-006: STORM SUPPRESSION TALLY -->
<section class="tracking-section" id="dw006-log">
  <div class="tracking-header">
    <h3>DW-006 &mdash; Running Storm-SR Suppression Tally</h3>
    <span class="cadence-label">Per G1+ storm event</span>
  </div>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">Storms logged</span><span class="stat-value">{storms_logged_dw6}</span></div>
    <div class="stat"><span class="stat-label">Suppression confirmed</span><span class="stat-value">{supp_confirmed_dw6}</span></div>
    <div class="stat"><span class="stat-label">Pending check</span><span class="stat-value">{supp_pending_dw6}</span></div>
    <div class="stat"><span class="stat-label">Confirmed rate</span><span class="stat-value">{"100% (of checked)" if supp_confirmed_dw6 > 0 else "0 confirmed yet"}</span></div>
    <div class="stat"><span class="stat-label">Dome predicts</span><span class="stat-value">&ge;75% suppression</span></div>
    <div class="stat"><span class="stat-label">Falsification threshold</span><span class="stat-value">5 consecutive NO</span></div>
  </div>
  <div class="immediate-banner" style="border-radius:0;">
    &#9889; <strong>March 22 PENDING:</strong> G3 confirmed 0900&ndash;1200 UTC. Check HeartMath March 22 amplitude.
    Suppression = PRED-SR-SUPPRESS confirmed (event 2). No suppression = update model.
  </div>
  <table class="log-table">
    <thead>
      <tr><th>Date</th><th>Storm Class</th><th>Kp Peak</th><th>Storm Phase Checked</th><th>SR Suppression %</th><th>Confirmed?</th><th>HeartMath / Source</th></tr>
    </thead>
    <tbody>
{dw006_rows()}
      <tr class="note-row">
        <td colspan="7">Add row per G1+ event: date | class | kp_peak | phase_checked | suppression_pct | confirmed (Y/N) | source</td>
      </tr>
    </tbody>
  </table>
</section>

<!-- DW-007: Dst INDEX TRACKING -->
<section class="tracking-section" id="dw007-log">
  <div class="tracking-header">
    <h3>DW-007 &mdash; Dst Index Tracking (Ring Current / Aetheric Compression)</h3>
    <span class="cadence-label">Per storm event</span>
  </div>
  <p class="section-intro">
    Dst measures the strength of Earth&rsquo;s ring current during geomagnetic storms. In ECM, this is the aetheric equatorial compression signature &mdash; the dome&rsquo;s equatorial aether being displaced inward during field stress events. Predicts: deeper Dst events correlate with faster SAA decay in subsequent months (&kappa; coupling). Category 1 data: ground magnetometer network, no model assumptions.
  </p>
  <div class="stat-row">
    <div class="stat"><span class="stat-label">Storm events logged</span><span class="stat-value">{len(dst_log)}</span></div>
    <div class="stat"><span class="stat-label">Deepest Dst this period</span><span class="stat-value">&lt;&minus;100 nT (Mar 20)</span></div>
    <div class="stat"><span class="stat-label">ECM predicts</span><span class="stat-value">Dst recovery rate correlates with SAA decay acceleration</span></div>
    <div class="stat"><span class="stat-label">Globe predicts</span><span class="stat-value">Dst and SAA decay independent</span></div>
  </div>
  <table class="log-table">
    <thead>
      <tr><th>Storm Date</th><th>Dst Min (nT)</th><th>Recovery Time (hrs)</th><th>Storm Class</th><th>SAA Month After</th><th>ECM Coupling?</th><th>Source</th></tr>
    </thead>
    <tbody>
{dst_rows()}
      <tr class="note-row">
        <td colspan="7">Pull Dst from Kyoto WDC after each storm. Log min Dst + recovery time. Compare SAA monthly delta the following month. Tests &kappa;=1.67 nT/&micro;Gal coupling (WIN-012) at storm timescales.</td>
      </tr>
    </tbody>
  </table>
  <div class="add-footer">
    Dst source: <a href="http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/presentmonth/index.html">Kyoto WDC real-time Dst</a> |
    Long-term archive: <a href="http://wdc.kugi.kyoto-u.ac.jp/dstdir/index.html">Kyoto Dst archive</a>
  </div>
</section>

<!-- HOW TO USE -->
<section style="margin-top:2.5rem;padding:1.5rem;background:var(--bg-code);border-radius:var(--radius-md);border:1px solid var(--border-light);box-shadow:var(--shadow-card);">
  <h2 style="margin-top:0;font-size:1.05rem;font-family:var(--font-body);font-weight:600;">How to Use These Logs</h2>
  <ol style="color:var(--text-secondary);font-size:0.85rem;line-height:1.8;">
    <li><strong>Daily (5 min):</strong> Check <a href="https://sos70.ru/provider.php?file=sra.jpg">Tomsk SR amplitude</a> + <a href="https://www.swpc.noaa.gov">NOAA Kp</a>. Add one row to DW-001. If Kp&lt;1 and SW&gt;8 nPa, also add to DW-004.</li>
    <li><strong>Per storm (immediate):</strong> Every G1+ event (Kp&ge;5) gets a DW-006 row within 24h. Check HeartMath. Log to DW-007 with Dst from Kyoto WDC.</li>
    <li><strong>Weekly:</strong> Pull <a href="https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/daily_aao.shtml">CPC AAO index</a> for the week. Add DW-003 row.</li>
    <li><strong>Monthly:</strong> Pull <a href="https://www.ngdc.noaa.gov/geomag/data/poles/NP.xy">NOAA NP.xy</a> &mdash; add DW-002 row. Pull <a href="https://www.intermagnet.org">INTERMAGNET</a> TTB/TDC/HER &mdash; add DW-005 row.</li>
    <li><strong>After each session with Claude:</strong> Paste new registry HTML into Claude Code and commit. Keeps timestamps honest.</li>
  </ol>
  <p style="color:var(--text-tertiary);font-size:0.78rem;margin-bottom:0;">All logs build the statistical case for or against ECM predictions. Every entry is a data point. Falsifications are as valuable as confirmations &mdash; they tell the model where it&rsquo;s wrong.</p>
</section>

<footer>
  <span>Version 50.9</span>
  <span>{TODAY}</span>
  <span style="color:var(--accent-blue);font-weight:600">53 confirmed</span>
  <span style="color:var(--accent-red)">4 falsified</span>
  <a href="https://github.com/John09289/predictions">GitHub</a>
  <a href="context.html">AI Context</a>
</footer>

</body>
</html>"""

with open(TRACKING_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Built tracking.html ({len(html)} chars, {total_entries} storm entries, {len(nmp_log)} NMP entries, {len(aao_log)} AAO entries)")

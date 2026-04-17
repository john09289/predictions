#!/usr/bin/env python3
"""
Build a daily prediction review artifact for the live site.

Outputs docs/data/daily_review.json using:
- ai_manifest.json for canonical registry counts
- status_history.json for live monitor state / trend
- optional Groq analysis when GROQ_API_KEY is present
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
DATA_DIR = DOCS_DIR / "data"
API_DIR = DOCS_DIR / "api" / "current"

AI_MANIFEST = DOCS_DIR / "ai_manifest.json"
STATUS_HISTORY = DATA_DIR / "status_history.json"
DAILY_REVIEW = DATA_DIR / "daily_review.json"

NOW = datetime.now(timezone.utc)
NOW_ISO = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
NOW_HUMAN = NOW.strftime("%Y-%m-%d %H:%M UTC")
TODAY = NOW.strftime("%Y-%m-%d")


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        print(f"Warning: failed to load {path.name}: {exc}")
        return default


def save_json(path: Path, payload):
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Saved {path}")


def pick_domain_groups(domains: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    passing = [d for d in domains if d.get("pass") is True]
    pending = [d for d in domains if d.get("pass") is None]
    failing = [d for d in domains if d.get("pass") is False]

    passing = sorted(
        passing,
        key=lambda d: (
            float("inf") if d.get("error_pct") is None else d.get("error_pct"),
            d.get("name", ""),
        ),
    )[:5]
    pending = pending[:5]
    failing = sorted(
        failing,
        key=lambda d: (
            -1 if d.get("error_pct") is None else -d.get("error_pct"),
            d.get("name", ""),
        ),
    )[:5]
    return passing, pending, failing


def simplify_domain(d: dict) -> dict:
    return {
        "name": d.get("name"),
        "predicted": d.get("predicted"),
        "observed": d.get("observed"),
        "unit": d.get("unit"),
        "error_pct": d.get("error_pct"),
        "status": (
            "pass" if d.get("pass") is True else
            "fail" if d.get("pass") is False else
            "pending"
        ),
        "source": d.get("source"),
    }


def build_local_brief(registry: dict, latest: dict, trend: dict, passing: list[dict], pending: list[dict], failing: list[dict]) -> dict:
    overview_parts = [
        f"Registry stands at {registry['confirmed']} confirmed, {registry['refined']} refined, and {registry['prospective']} prospective items.",
        f"Latest monitor snapshot is {latest.get('overall_score', '—')}% with {latest.get('passed', '—')} of {latest.get('total_scored', '—')} scored domains passing.",
    ]
    if trend.get("delta_score_7d") is not None:
        delta = trend["delta_score_7d"]
        direction = "up" if delta > 0 else "down" if delta < 0 else "flat"
        overview_parts.append(f"The 7-day score trend is {direction} by {abs(delta):.1f} points.")
    if latest.get("eclipse_days") is not None:
        overview_parts.append(f"{latest['eclipse_days']} days remain until the August 12, 2026 eclipse test.")

    next_actions = []
    if pending:
        next_actions.append(f"Check pending domains first: {', '.join(d.get('name', '?') for d in pending[:3])}.")
    if failing:
        next_actions.append(f"Audit the largest miss: {failing[0].get('name', '?')}.")
    next_actions.append("Keep WIN-058 marked pending until independent raw L1A or Tier 3 closure arrives.")

    prediction_focus = []
    if passing:
        prediction_focus.append(f"Strongest current live alignment: {passing[0].get('name', '?')}.")
    if latest.get("eclipse_days") is not None:
        prediction_focus.append("Primary forward discriminator remains the Tier 3 eclipse protocol.")

    caveats = [
        "Display ratio is bookkeeping, not a substitute for claim-by-claim audit.",
        "Supportive and pending items should not be collapsed into pure prospective wins.",
    ]

    return {
        "provider": "local",
        "model": "deterministic-summary",
        "summary": " ".join(overview_parts),
        "next_actions": next_actions,
        "prediction_focus": prediction_focus,
        "caveats": caveats,
    }


def call_groq(payload: dict) -> dict | None:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    system = (
        "You are generating a concise daily site brief for a live prediction registry. "
        "Use only the provided JSON facts. Do not invent data, citations, or claims. "
        "Return strict JSON with keys: summary, next_actions, prediction_focus, caveats. "
        "Each list should contain 2 to 4 short strings."
    )
    user = json.dumps(payload, indent=2)

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            },
            timeout=45,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return {
            "provider": "groq",
            "model": model,
            "summary": parsed.get("summary", ""),
            "next_actions": parsed.get("next_actions", []),
            "prediction_focus": parsed.get("prediction_focus", []),
            "caveats": parsed.get("caveats", []),
        }
    except Exception as exc:
        print(f"Groq generation failed, using local summary: {exc}")
        return None


def main():
    manifest = load_json(AI_MANIFEST, {})
    history = load_json(STATUS_HISTORY, [])

    latest = history[-1] if history else {}
    domains = latest.get("domains", [])
    passing, pending, failing = pick_domain_groups(domains)

    scores_7 = [h.get("overall_score") for h in history[-7:] if isinstance(h.get("overall_score"), (int, float))]
    latest_score = latest.get("overall_score")
    delta_score = None
    if len(scores_7) >= 2:
        delta_score = round(scores_7[-1] - scores_7[0], 2)

    registry = {
        "confirmed": manifest.get("counts", {}).get("confirmed", 69),
        "prospective": manifest.get("counts", {}).get("prospective_confirmed", 10),
        "refined": manifest.get("counts", {}).get("refined", 4),
        "registry_ratio_pct": manifest.get("counts", {}).get("registry_accuracy_pct", 94.5),
    }

    trend = {
        "samples_7d": len(scores_7),
        "avg_score_7d": round(mean(scores_7), 2) if scores_7 else None,
        "latest_score": latest_score,
        "delta_score_7d": delta_score,
    }

    review_payload = {
        "generated_at": NOW_ISO,
        "generated_human": NOW_HUMAN,
        "registry": registry,
        "live_monitor": {
            "timestamp": latest.get("timestamp"),
            "wins_confirmed_monitor": latest.get("wins_confirmed"),
            "overall_score": latest_score,
            "passed": latest.get("passed"),
            "total_scored": latest.get("total_scored"),
            "pending_domains": len([d for d in domains if d.get("pass") is None]),
            "eclipse_days": latest.get("eclipse_days"),
        },
        "trend": trend,
        "domain_review": {
            "top_passing": [simplify_domain(d) for d in passing],
            "pending_watchlist": [simplify_domain(d) for d in pending],
            "top_failing": [simplify_domain(d) for d in failing],
        },
        "accuracy_review": {
            "registry_ratio_pct": registry["registry_ratio_pct"],
            "monitor_score_pct": latest_score,
            "avg_monitor_score_7d": trend["avg_score_7d"],
            "passed_over_scored": (
                f"{latest.get('passed', 0)}/{latest.get('total_scored', 0)}"
                if latest else None
            ),
        },
    }

    llm_input = {
        "registry": review_payload["registry"],
        "live_monitor": review_payload["live_monitor"],
        "trend": review_payload["trend"],
        "domain_review": review_payload["domain_review"],
        "method_note": "Keep caveats visible. Do not convert supportive or pending items into pure prospective wins.",
    }
    ai_brief = call_groq(llm_input) or build_local_brief(
        registry, latest, trend, passing, pending, failing
    )
    review_payload["ai_brief"] = ai_brief

    save_json(DAILY_REVIEW, review_payload)


if __name__ == "__main__":
    main()

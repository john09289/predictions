#!/usr/bin/env python3
"""
Downloader for legitimately accessed L1A/L0-style datasets.

This script is intentionally designed around lawful access:
- no disposable email creation
- no CAPTCHA solving
- no account bypass

Supported workflows:
1. Selenium/manual-login mode:
   - opens a browser to the portal login page
   - you log in yourself
   - the script copies the authenticated browser cookies into a requests session
   - downloads continue automatically

2. Exported-cookie mode:
   - you log in with your normal browser
   - export cookies to Netscape or JSON format
   - the script imports those cookies and downloads files with requests

3. SFTP mode:
   - for portals that expose raw or high-rate files through SSH/SFTP
   - authenticate with your legitimate username/password or SSH key
   - download files directly without a browser

The job file is simple on purpose: one list of datasets, one authenticated URL
per download target. That keeps the downloader useful even when portal layouts
change but the final file URLs remain known.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import webbrowser
from dataclasses import dataclass
from http.cookiejar import MozillaCookieJar
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

try:
    import paramiko
except Exception:  # pragma: no cover - optional dependency
    paramiko = None

try:
    import tkinter as tk
    from tkinter import messagebox
except Exception:  # pragma: no cover - optional dependency
    tk = None
    messagebox = None

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
except Exception:  # pragma: no cover - optional dependency
    webdriver = None
    ChromeOptions = None
    ChromeService = None
    By = None
    WebDriverWait = None


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JOB_FILE = REPO_ROOT / "data" / "l1a_download_jobs.example.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "proofs" / "l1a_raw_downloads"
USER_AGENT = "predictions-repo-l1a-manual-downloader/1.0"


@dataclass
class DownloadJob:
    portal: str
    description: str
    login_url: str
    downloads: list[dict[str, Any]]
    transport: str = "http"
    requires_manual_login: bool = True
    notes: list[str] | None = None
    headers: dict[str, str] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=Path, default=DEFAULT_JOB_FILE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--portal",
        action="append",
        help="Restrict to one or more portal names from the job file.",
    )
    parser.add_argument(
        "--cookie-file",
        type=Path,
        help="Cookie export in Netscape or JSON list format.",
    )
    parser.add_argument(
        "--username",
        help="Username for SFTP jobs. If omitted, defaults to L1A_SFTP_USERNAME.",
    )
    parser.add_argument(
        "--password-env",
        default="L1A_SFTP_PASSWORD",
        help="Environment variable name holding the SFTP password. Default: L1A_SFTP_PASSWORD",
    )
    parser.add_argument(
        "--ssh-key",
        type=Path,
        help="Optional SSH private key file for SFTP jobs.",
    )
    parser.add_argument(
        "--allow-unknown-hosts",
        action="store_true",
        help="Allow connecting to SFTP hosts not present in known_hosts. Use only when you trust the host.",
    )
    parser.add_argument(
        "--selenium",
        action="store_true",
        help="Use Selenium for the manual login gate and import cookies from that session.",
    )
    parser.add_argument(
        "--browser",
        choices=("chrome",),
        default="chrome",
        help="Browser backend for Selenium mode.",
    )
    parser.add_argument(
        "--chrome-binary",
        help="Optional explicit path to the Chrome/Chromium binary.",
    )
    parser.add_argument(
        "--driver-path",
        help="Optional explicit path to chromedriver.",
    )
    parser.add_argument(
        "--login-check-css",
        help="Optional CSS selector that appears only after successful login.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Manual login timeout in seconds for Selenium mode.",
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the login URL in the default browser in non-Selenium mode.",
    )
    parser.add_argument(
        "--no-popup",
        action="store_true",
        help="Disable desktop popup guidance and use terminal prompts only.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be downloaded without making HTTP requests.",
    )
    return parser.parse_args()


def load_jobs(path: Path) -> list[DownloadJob]:
    payload = json.loads(path.read_text())
    jobs = []
    for entry in payload["jobs"]:
        jobs.append(
            DownloadJob(
                portal=entry["portal"],
                description=entry["description"],
                login_url=entry["login_url"],
                downloads=entry["downloads"],
                transport=entry.get("transport", "http"),
                requires_manual_login=entry.get("requires_manual_login", True),
                notes=entry.get("notes"),
                headers=entry.get("headers"),
            )
        )
    return jobs


def selected_jobs(jobs: list[DownloadJob], portals: list[str] | None) -> list[DownloadJob]:
    if not portals:
        return jobs
    wanted = set(portals)
    found = [job for job in jobs if job.portal in wanted]
    missing = wanted - {job.portal for job in found}
    if missing:
        joined = ", ".join(sorted(missing))
        raise SystemExit(f"Unknown portal names in --portal: {joined}")
    return found


def build_session(headers: dict[str, str] | None = None) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    if headers:
        session.headers.update(headers)
    return session


def import_cookie_file(session: requests.Session, cookie_file: Path) -> None:
    if cookie_file.suffix.lower() in {".txt", ".cookies", ".netscape"}:
        jar = MozillaCookieJar(str(cookie_file))
        jar.load(ignore_discard=True, ignore_expires=True)
        session.cookies.update(jar)
        return

    payload = json.loads(cookie_file.read_text())
    if isinstance(payload, dict) and "cookies" in payload:
        payload = payload["cookies"]

    if not isinstance(payload, list):
        raise ValueError("Cookie JSON must be a list of cookie objects or {\"cookies\": [...]} format.")

    for cookie in payload:
        name = cookie["name"]
        value = cookie["value"]
        domain = cookie.get("domain")
        path = cookie.get("path", "/")
        session.cookies.set(name, value, domain=domain, path=path)


def chrome_driver(args: argparse.Namespace):
    if webdriver is None:
        raise RuntimeError("Selenium is not installed. Install selenium to use --selenium.")
    options = ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    if args.chrome_binary:
        options.binary_location = args.chrome_binary
    service = ChromeService(executable_path=args.driver_path) if args.driver_path else None
    return webdriver.Chrome(service=service, options=options)


def popup_text(title: str, message: str, disable_popup: bool) -> None:
    if disable_popup or tk is None or messagebox is None:
        return
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showinfo(title, message, parent=root)
        root.destroy()
    except Exception:
        return


def render_login_steps(job: DownloadJob, selenium_mode: bool) -> str:
    steps = [
        f"Portal: {job.portal}",
        "",
        "What to do now:",
        "1. Log in with your real account.",
        "2. Complete any portal prompts in the opened browser window.",
        "3. Navigate to the page that confirms you are fully signed in.",
    ]
    if selenium_mode:
        steps.append("4. Return to the terminal and press Enter once login is complete.")
    else:
        steps.extend(
            [
                "4. Export the authenticated cookies from your browser.",
                "5. Return to the terminal and press Enter once the cookie file is ready.",
            ]
        )
    if job.notes:
        steps.extend(["", "Portal notes:"])
        steps.extend([f"- {note}" for note in job.notes])
    return "\n".join(steps)


def validate_download_targets(job: DownloadJob) -> None:
    placeholders = []
    for item in job.downloads:
        url = item["url"]
        if "REPLACE_WITH_REAL" in url or "example.com" in url:
            placeholders.append(item.get("label", url))
    if placeholders:
        joined = ", ".join(placeholders)
        raise SystemExit(
            f"Job file still contains placeholder download URLs for {job.portal}: {joined}. "
            "Replace them with your real authenticated export URLs first."
        )


def validate_sftp_args(args: argparse.Namespace, job: DownloadJob) -> None:
    if paramiko is None:
        raise RuntimeError("paramiko is not installed. Install requirements_l1a.txt to use SFTP jobs.")
    if not args.username and not os.environ.get("L1A_SFTP_USERNAME"):
        raise SystemExit(
            f"SFTP job for {job.portal} requires --username or L1A_SFTP_USERNAME in the environment."
        )
    if not args.ssh_key and not os.environ.get(args.password_env):
        raise SystemExit(
            f"SFTP job for {job.portal} requires either --ssh-key or password env {args.password_env}."
        )


def wait_for_manual_login(
    driver,
    job: DownloadJob,
    timeout: int,
    login_check_css: str | None,
    disable_popup: bool,
) -> None:
    login_url = job.login_url
    driver.get(login_url)
    message = render_login_steps(job, selenium_mode=True)
    print("\n" + message)
    popup_text(f"{job.portal} login needed", message, disable_popup)

    if login_check_css:
        print(f"Waiting up to {timeout}s for selector: {login_check_css}")
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, login_check_css)) > 0
        )
        return

    deadline = time.time() + timeout
    while time.time() < deadline:
        response = input("Press Enter after login is complete, or type 'abort' to stop: ").strip().lower()
        if response == "abort":
            raise SystemExit("Manual login aborted by user.")
        return
    raise TimeoutError("Timed out waiting for manual login.")


def selenium_cookies_to_session(driver, session: requests.Session) -> None:
    for cookie in driver.get_cookies():
        session.cookies.set(
            cookie["name"],
            cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path", "/"),
        )


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def download_with_session(session: requests.Session, url: str, output_path: Path, dry_run: bool) -> None:
    ensure_parent(output_path)
    if dry_run:
        print(f"DRY RUN  {url} -> {output_path}")
        return

    with session.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with output_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    handle.write(chunk)
    print(f"DOWNLOADED  {output_path}")


def build_sftp_client(args: argparse.Namespace, host: str, port: int):
    username = args.username or os.environ.get("L1A_SFTP_USERNAME")
    password = os.environ.get(args.password_env)

    client = paramiko.SSHClient()
    if args.allow_unknown_hosts:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    else:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())

    connect_kwargs: dict[str, Any] = {
        "hostname": host,
        "port": port,
        "username": username,
        "look_for_keys": False,
        "allow_agent": False,
        "timeout": 60,
    }
    if args.ssh_key:
        connect_kwargs["key_filename"] = str(args.ssh_key)
        if password:
            connect_kwargs["passphrase"] = password
    else:
        connect_kwargs["password"] = password

    client.connect(**connect_kwargs)
    return client


def download_with_sftp(args: argparse.Namespace, job: DownloadJob, output_dir: Path, dry_run: bool) -> None:
    validate_sftp_args(args, job)
    parsed = urlparse(job.downloads[0]["url"])
    host = parsed.hostname
    port = parsed.port or 22
    if not host:
        raise SystemExit(f"SFTP job for {job.portal} must use sftp://host/path URLs.")

    client = None
    sftp = None
    try:
        client = build_sftp_client(args, host, port)
        sftp = client.open_sftp()

        for item in job.downloads:
            parsed_item = urlparse(item["url"])
            if parsed_item.scheme != "sftp":
                raise SystemExit(f"SFTP job for {job.portal} contains non-sftp URL: {item['url']}")
            if parsed_item.hostname != host or (parsed_item.port or 22) != port:
                raise SystemExit(
                    f"All SFTP download URLs for {job.portal} must share the same host and port."
                )

            remote_path = parsed_item.path
            rel_path = Path(item["output"])
            output_path = output_dir / rel_path
            ensure_parent(output_path)

            if dry_run:
                print(f"DRY RUN  sftp://{host}{remote_path} -> {output_path}")
                continue

            sftp.get(remote_path, str(output_path))
            print(f"DOWNLOADED  {output_path}")
    finally:
        if sftp is not None:
            sftp.close()
        if client is not None:
            client.close()


def non_selenium_manual_gate(job: DownloadJob, open_browser: bool, disable_popup: bool) -> None:
    message = render_login_steps(job, selenium_mode=False)
    print("\n" + message)
    print(f"\nLogin URL: {job.login_url}")
    if open_browser:
        webbrowser.open(job.login_url)
    popup_text(f"{job.portal} cookie export needed", message, disable_popup)
    input("Press Enter to continue once the session is ready: ")


def main() -> int:
    args = parse_args()
    jobs = selected_jobs(load_jobs(args.jobs), args.portal)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if any(job.transport == "http" for job in jobs) and not args.selenium and not args.cookie_file:
        print(
            "HTTP portal jobs require either --selenium or --cookie-file for authenticated downloads.",
            file=sys.stderr,
        )
        return 2

    for job in jobs:
        validate_download_targets(job)
        if job.transport == "sftp":
            download_with_sftp(args, job, args.output_dir, args.dry_run)
            continue

        session = build_session(job.headers)
        driver = None

        try:
            if args.selenium:
                driver = chrome_driver(args)
                wait_for_manual_login(
                    driver=driver,
                    job=job,
                    timeout=args.timeout,
                    login_check_css=args.login_check_css,
                    disable_popup=args.no_popup,
                )
                selenium_cookies_to_session(driver, session)
            else:
                non_selenium_manual_gate(job, args.open_browser, args.no_popup)
                import_cookie_file(session, args.cookie_file)

            for item in job.downloads:
                url = item["url"]
                rel_path = Path(item["output"])
                output_path = args.output_dir / rel_path
                download_with_session(session, url, output_path, args.dry_run)

        finally:
            if driver is not None:
                driver.quit()

    print("\nAll selected download jobs completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

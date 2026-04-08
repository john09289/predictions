# L1A Manual Workflow

This workflow is designed for legitimate access only.

## 1. Prepare the environment

```bash
python3 -m pip install -r scripts/requirements_l1a.txt
```

If you want browser-assisted login reuse for web portals, also ensure:

- Chrome or Chromium is installed
- a matching `chromedriver` is available

## 2. Fill in the job file

Copy and edit:

- `data/l1a_download_jobs.example.json`

Replace each `REPLACE_WITH_REAL_*` URL with the actual authenticated export URL you are allowed to use.

## 3. Download with a manual login gate

### Option A — Selenium browser reuse

```bash
python3 scripts/download_l1a_manual.py \
  --jobs data/l1a_download_jobs.example.json \
  --portal igets_gfz \
  --selenium
```

The script will open a browser, show built-in step-by-step popup guidance, stop, and wait for you to log in manually. After you finish, it reuses that authenticated browser session for file downloads.

If you prefer terminal prompts only:

```bash
python3 scripts/download_l1a_manual.py \
  --jobs data/l1a_download_jobs.example.json \
  --portal igets_gfz \
  --selenium \
  --no-popup
```

### Option B — Exported cookies

Log in normally in your browser, export cookies, then run:

```bash
python3 scripts/download_l1a_manual.py \
  --jobs data/l1a_download_jobs.example.json \
  --portal intermagnet \
  --cookie-file /path/to/exported_cookies.txt
```

Supported cookie formats:

- Netscape/Mozilla cookie jar text
- JSON cookie list

### Option C — Official SFTP automation

Some raw/high-rate portals are not really browser workflows. If your portal provides SSH/SFTP access, you can download directly with your legitimate credentials:

```bash
export L1A_SFTP_USERNAME="your_username"
export L1A_SFTP_PASSWORD="your_password"

python3 scripts/download_l1a_manual.py \
  --jobs data/l1a_download_jobs.example.json \
  --portal igets_gfz_sftp \
  --allow-unknown-hosts
```

If you use a private key instead of a password:

```bash
export L1A_SFTP_USERNAME="your_username"

python3 scripts/download_l1a_manual.py \
  --jobs data/l1a_download_jobs.example.json \
  --portal igets_gfz_sftp \
  --ssh-key /path/to/private_key
```

Notes:

- `--allow-unknown-hosts` is only for hosts you trust and only if your `known_hosts` file does not already contain the portal host.
- For web portals like INTERMAGNET, keep using Selenium or cookie export.
- For SFTP portals, a browser tool like Lightpanda does not help much because the download path is not a browser session in the first place.

## 4. Analyze the files

```bash
python3 scripts/analyze_l1a_mask.py \
  --mag-file proofs/l1a_raw_downloads/intermagnet/her20240510vsec.sec \
  --grav-file proofs/l1a_raw_downloads/igets_gfz/serrahn_igrav033_2024_05_10.dat \
  --output-dir proofs/l1a_analysis_may10
```

Outputs include:

- PSD plots
- residual and spike plots
- optional ΔB/Δg ratio plot
- `l1a_analysis_report.md`

## 5. Honest interpretation

The analysis script can show:

- whether spikes survive baseline removal
- whether the PSD suggests low-pass filtering
- whether any coincident ΔB/Δg ratios cluster near a target

It cannot by itself prove deliberate suppression. If the public series is too smoothed, the strongest honest conclusion is that the dataset is not raw enough to test fast transients well.

"""
Upload NASA MODIS C6.1 Yearly ZIP Archives to GitHub Release Assets
"""

import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.error

PROJECT_DIR = r"D:\data\MODIS-C6.1"
RELEASE_ID = 425226852
REPO = "nisha200726/MODIS-C6.1"


def get_github_token():
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate('protocol=https\nhost=github.com\n')
    creds = dict(line.split('=', 1) for line in out.strip().splitlines() if '=' in line)
    return creds.get('password')


def get_existing_assets(token):
    url = f"https://api.github.com/repos/{REPO}/releases/{RELEASE_ID}/assets"
    req = urllib.request.Request(url, headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'MODIS-Uploader'
    })
    with urllib.request.urlopen(req) as resp:
        assets = json.loads(resp.read().decode())
    return {a['name']: a for a in assets}


def upload_asset(token, local_path, asset_name, max_retries=3):
    upload_url = f"https://uploads.github.com/repos/{REPO}/releases/{RELEASE_ID}/assets?name={asset_name}"
    file_size = os.path.getsize(local_path)
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Uploading {asset_name} ({file_size / (1024*1024):.2f} MB)... (attempt {attempt})")
            start_time = time.time()
            with open(local_path, "rb") as f:
                data = f.read()
                
            req = urllib.request.Request(upload_url, data=data, headers={
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/zip',
                'Content-Length': str(file_size),
                'User-Agent': 'MODIS-Uploader'
            })
            
            with urllib.request.urlopen(req, timeout=300) as resp:
                res = json.loads(resp.read().decode())
                elapsed = time.time() - start_time
                speed = (file_size / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                print(f"  -> Success! Uploaded in {elapsed:.1f}s ({speed:.2f} MB/s). Asset ID: {res.get('id')}")
                return res
        except Exception as e:
            print(f"  -> Error on attempt {attempt}: {e}")
            if attempt < max_retries:
                time.sleep(3 * attempt)
            else:
                raise


def get_file_map():
    mapping = []
    for year in range(2000, 2026):
        asset_name = f"modis_{year}_all_countries.zip"
        local_path = os.path.join(PROJECT_DIR, asset_name)
        if not os.path.exists(local_path):
            alt_path = os.path.join(PROJECT_DIR, f"modis_{year}_all_countries (1).zip")
            if os.path.exists(alt_path):
                local_path = alt_path
            else:
                raise FileNotFoundError(f"Missing local archive for {year}: {local_path}")
        mapping.append((year, local_path, asset_name))
    return mapping


def main():
    token = get_github_token()
    if not token:
        print("Error: Could not retrieve GitHub token from Git Credential Manager.")
        sys.exit(1)
        
    existing_assets = get_existing_assets(token)
    print(f"Existing assets in release: {len(existing_assets)}")
    
    file_map = get_file_map()
    print(f"Total files to process: {len(file_map)}")
    
    success_count = 0
    for idx, (year, local_path, asset_name) in enumerate(file_map, 1):
        print(f"\n[{idx}/{len(file_map)}] Year {year}: {asset_name}")
        if asset_name in existing_assets:
            remote_size = existing_assets[asset_name]['size']
            local_size = os.path.getsize(local_path)
            if remote_size == local_size:
                print(f"  -> Already uploaded and verified matching size ({remote_size} bytes). Skipping.")
                success_count += 1
                continue
            else:
                print(f"  -> Size mismatch (remote: {remote_size}, local: {local_size}). Needs re-upload.")
                
        upload_asset(token, local_path, asset_name)
        success_count += 1
        
    print(f"\nAll completed! Successfully uploaded and verified {success_count}/{len(file_map)} archives.")


if __name__ == "__main__":
    main()

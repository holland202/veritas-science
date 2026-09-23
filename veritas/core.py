import hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256(value):
    raw = value if isinstance(value, bytes) else canonical(value).encode()
    return hashlib.sha256(raw).hexdigest()

def now(): return datetime.now(timezone.utc).isoformat()
def environment(): return {"python": sys.version.split()[0], "platform": platform.platform(), "veritas": "0.1.0"}
def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write_json(path, value): Path(path).write_text(json.dumps(value, indent=2, sort_keys=True)+"\n", encoding="utf-8")
def envelope(kind, payload, parent_digest=None):
    out={"kind":kind,"created_at":now(),"payload":payload}
    if parent_digest: out["parent_digest"]=parent_digest
    out["digest"]=sha256(out)
    return out
def verify_envelope(obj):
    if not isinstance(obj, dict) or not obj.get("digest"): return False
    copy=dict(obj); given=copy.pop("digest")
    return given == sha256(copy)

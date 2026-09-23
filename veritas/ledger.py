import json
from pathlib import Path
from .core import now, sha256

class Ledger:
    def __init__(self, path): self.path=Path(path)
    def append(self, event, payload, previous=None):
        body={"event":event,"timestamp":now(),"payload":payload}
        if previous: body["previous_event_digest"]=previous
        record=dict(body, digest=sha256(body))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f: f.write(json.dumps(record, sort_keys=True)+"\n")
        return record
    def verify(self):
        if not self.path.exists(): return {"valid":True,"events":0}
        previous=None; count=0
        for line in self.path.read_text(encoding="utf-8").splitlines():
            record=json.loads(line); given=record.pop("digest",None)
            if given != sha256(record): return {"valid":False,"events":count,"reason":"digest mismatch"}
            if previous is not None and record.get("previous_event_digest") != previous:
                return {"valid":False,"events":count,"reason":"chain mismatch"}
            previous=given; count+=1
        return {"valid":True,"events":count}

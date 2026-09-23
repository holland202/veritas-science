from .core import envelope

STATUSES={"established","derived","conjectural","measured","exploratory"}
REQUIRED=("title","claim","epistemic_status","assumptions","prior_art","hypothesis","null","predictions","implementation","data_contract","analysis")


def validate_protocol(p):
    errors=["missing:"+k for k in REQUIRED if k not in p]
    if p.get("epistemic_status") not in STATUSES: errors.append("invalid epistemic_status")
    if not isinstance(p.get("assumptions"),list) or not p["assumptions"]: errors.append("assumptions must be non-empty")
    if not isinstance(p.get("prior_art"),list) or not p["prior_art"]: errors.append("prior_art must be non-empty")
    if not p.get("null"): errors.append("explicit null required")
    predictions=p.get("predictions",[])
    if not isinstance(predictions,list) or not predictions: errors.append("predictions must be non-empty")
    ids=set()
    for x in predictions:
        for k in ("id","metric","null","direction","threshold","alpha","n_min","anti_vacuity","refutes_claim"):
            if k not in x: errors.append(f"prediction missing:{k}")
        if x.get("id") in ids: errors.append("duplicate prediction:"+str(x.get("id")))
        ids.add(x.get("id"))
        if x.get("direction") not in {"greater","less","equal"}: errors.append("invalid prediction direction")
        if not isinstance(x.get("threshold"),(int,float)): errors.append("threshold must be numeric")
        if not 0 < x.get("alpha",0) < 1: errors.append("alpha must be in (0,1)")
        if x.get("n_min",0) < 2: errors.append("n_min must be >= 2")
        if not isinstance(x.get("anti_vacuity"),dict) or not x.get("anti_vacuity"): errors.append("anti-vacuity rule required")
        if "refutes_claim" not in x:
            continue
        if not isinstance(x["refutes_claim"], bool): errors.append("refutes_claim must be boolean")
    return errors


def freeze(p,parent_digest=None):
    errors=validate_protocol(p)
    if errors: raise ValueError("invalid protocol: "+"; ".join(errors))
    return envelope("preregistered_protocol",p,parent_digest)

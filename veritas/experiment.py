import math
from . import __version__
from .core import sha256, environment


def run(protocol, data, seed=None):
    threshold = protocol["implementation"].get("threshold", 0.5)
    if not data:
        raise ValueError("data must not be empty")
    y, x = [], []
    for i, row in enumerate(data):
        value, label = row.get("x"), row.get("y")
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            raise ValueError(f"row {i}: x must be finite")
        if label not in (0, 1):
            raise ValueError(f"row {i}: y must be 0 or 1")
        x.append(float(value)); y.append(int(label))
    predictions = [int(value >= threshold) for value in x]
    accuracy = sum(a == b for a, b in zip(y, predictions)) / len(y)
    baseline = max(sum(y), len(y) - sum(y)) / len(y)
    return {"n": len(y), "accuracy": accuracy, "majority_baseline": baseline,
            "effect": accuracy - baseline, "data_digest": sha256(data),
            "implementation_digest": sha256(protocol["implementation"]),
            "seed": seed, "environment": {**environment(), "veritas": __version__}}


def check_prediction(prediction, result):
    base = {"id": prediction["id"], "metric": prediction["metric"],
            "threshold": prediction["threshold"]}
    if result.get("n", 0) < prediction["n_min"]:
        return {**base, "status": "NOT_SUPPORTED", "reason": "n below minimum"}
    value = result.get(prediction["metric"])
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        return {**base, "status": "INDETERMINATE", "reason": "metric is missing or non-finite"}
    anti = prediction.get("anti_vacuity", {})
    if anti.get("reject_degenerate") and result.get("accuracy") in (0.0, 1.0):
        return {**base, "value": value, "status": "NOT_SUPPORTED", "reason": "degenerate accuracy rejected by anti-vacuity rule"}
    if prediction["direction"] == "greater": ok = value >= prediction["threshold"]
    elif prediction["direction"] == "less": ok = value <= prediction["threshold"]
    else: ok = abs(value - prediction["threshold"]) < 1e-12
    return {**base, "value": value, "status": "SUPPORTED" if ok else "NOT_SUPPORTED"}

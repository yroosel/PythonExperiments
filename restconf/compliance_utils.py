from typing import Optional, Any, Dict, List, Tuple
from copy import deepcopy
import json
from rich.table import Table
from rich.console import Console


# ---------- Merging & Baseline ----------

def deep_merge(a: Dict, b: Dict) -> Dict:
    """Return a deep merge of dict a with dict b (b overrides a)."""
    res = deepcopy(a)
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(res.get(k), dict):
            res[k] = deep_merge(res[k], v)
        else:
            res[k] = deepcopy(v)
    return res

def effective_baseline(baseline: Dict[str, Any], serial: str) -> Dict[str, Any]:
    """Compute effective baseline = global + per-device override by serial."""
    base = baseline.get("global", {}) or {}
    dev  = baseline.get("devices", {}).get(serial, {}) or {}
    return deep_merge(base, dev)


# ---------- Normalization helpers ----------

def canonical_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "yes", "on", "1", "enabled", "up")
    if isinstance(v, (int, float)):
        return bool(v)
    return v

def _norm_value(exp, act):
    """Normalize common types for fair comparison."""
    if isinstance(exp, bool):
        return canonical_bool(exp), canonical_bool(act)
    return exp, act


# ---------- List comparison (subset semantics) ----------

def _list_of_scalars_subset(exp_list, act_list):
    """True if every scalar in exp_list appears in act_list (order-insensitive)."""
    try:
        return set(exp_list).issubset(set(act_list or []))
    except Exception:
        return all(item in (act_list or []) for item in exp_list)

def _list_of_dicts_subset(exp_list, act_list):
    """True if every dict in exp_list appears in act_list (order-insensitive)."""
    exp_norm = [json.dumps(x, sort_keys=True) for x in exp_list]
    act_norm = [json.dumps(x, sort_keys=True) for x in (act_list or [])]
    return all(e in act_norm for e in exp_norm)

def _compare_lists_subset(exp_list, act_list):
    """Baseline-as-subset semantics for any list value."""
    if not isinstance(act_list, list):
        return False
    if all(not isinstance(x, (dict, list)) for x in exp_list):
        return _list_of_scalars_subset(exp_list, act_list)
    return _list_of_dicts_subset(exp_list, act_list)


# ---------- Diffing ----------

def compare_maps(baseline: Dict[str, Any], observed: Dict[str, Any]) -> List[Tuple[str, Any, Any]]:
    """
    Compare observed map to baseline. 
    Returns list of diffs: (keypath, expected, actual).
    Only keys present in baseline are enforced.
    """
    diffs: List[Tuple[str, Any, Any]] = []

    def walk(exp, act, prefix=""):
        if isinstance(exp, dict):
            if not isinstance(act, dict):
                diffs.append((prefix.rstrip("."), exp, act))
                return
            for k, v in exp.items():
                kp = f"{prefix}{k}"
                walk(v, act.get(k), kp + ".")
            return

        if isinstance(exp, list):
            if not _compare_lists_subset(exp, act):
                diffs.append((prefix.rstrip("."), exp, act))
            return

        exp_n, act_n = _norm_value(exp, act)
        if exp_n != act_n:
            diffs.append((prefix.rstrip("."), exp, act))

    walk(baseline, observed, "")
    return diffs


# ---------- Rendering ----------

def _short(val: Any, maxlen: int = 80) -> str:
    """Pretty/short string for table display."""
    try:
        if isinstance(val, (dict, list)):
            s = json.dumps(val, sort_keys=True)
        else:
            s = str(val)
    except Exception:
        s = repr(val)
    return (s if len(s) <= maxlen else s[: maxlen - 1] + "?")

def render_table(rows: List[Dict[str, str]], title: str = "Compliance Report"):
    """rows: dicts with keys Device, Serial, Protocol, Status, Drift Count, Drift Keys, Drift Values"""
    console = Console()
    table = Table(title=title)

    headers = ["Device", "Serial", "Protocol", "Status", "Drift Count", "Drift Keys", "Drift Values"]
    for h in headers:
        style = "cyan" if h in ("Device", "Serial", "Protocol") else ""
        no_wrap = False if h in ("Drift Keys", "Drift Values") else True
        table.add_column(h, style=style, no_wrap=no_wrap)

    for r in rows:
        table.add_row(
            r.get("Device", ""),
            r.get("Serial", ""),
            r.get("Protocol", ""),
            r.get("Status", ""),
            r.get("Drift Count", ""),
            r.get("Drift Keys", "-"),
            r.get("Drift Values", "-"),
        )

    console.print(table)


# ---------- Convenience formatter for collectors ----------

def diffs_to_columns(diffs: List[Tuple[str, Any, Any]]) -> Dict[str, str]:
    """Turn diff tuples into 'Drift Keys' and 'Drift Values' strings for the table."""
    if not diffs:
        return {"Drift Count": "0", "Drift Keys": "-", "Drift Values": "-"}

    keys = []
    vals = []
    for k, exp, act in diffs:
        keys.append(k)
        vals.append(f"{k} ? expected: {_short(exp)} / actual: {_short(act)}")

    return {
        "Drift Count": str(len(diffs)),
        "Drift Keys": ", ".join(keys),
        "Drift Values": "; ".join(vals),
    }
"""
extract_static_metrics.py — extract static code metrics for all 300 programs.

Metrics extracted:
  - LOC_Total, LOC_Code, LOC_Comment, Comment_Density
  - CC_Average, CC_Max, CC_Functions, Cognitive_CC
  - MI_Score, MI_Rank
  - H_Volume, H_Difficulty, H_Effort, H_Bugs
  - Max_Nesting, Avg_Func_Length
  - Code_Smells (basic anti-pattern counts), Duplicate_Pct

USAGE:
    python extract_static_metrics.py --manifest manifest.json \\
                                     --output static_metrics.csv
"""
import argparse
import ast
import json
import re
from pathlib import Path

import pandas as pd
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
from radon.raw import analyze


# ------------------------------------------------------------------
# Cognitive complexity (per Campbell 2018, simplified)
# ------------------------------------------------------------------

class CognitiveCC(ast.NodeVisitor):
    """Compute cognitive complexity. Adds nesting bonus for nested constructs."""

    NESTING_ADDERS = (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)
    FLAT_ADDERS = (ast.BoolOp,)  # logical-AND/OR counts as +1 each

    def __init__(self):
        self.cc = 0
        self.nesting = 0

    def visit(self, node):
        if isinstance(node, self.NESTING_ADDERS):
            self.cc += 1 + self.nesting
            self.nesting += 1
            for child in ast.iter_child_nodes(node):
                self.visit(child)
            self.nesting -= 1
        elif isinstance(node, ast.BoolOp):
            self.cc += max(0, len(node.values) - 1)
            for child in ast.iter_child_nodes(node):
                self.visit(child)
        else:
            self.generic_visit(node)


def cognitive_complexity_of(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return 0
    total = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            v = CognitiveCC()
            v.visit(node)
            total += v.cc
    return total


# ------------------------------------------------------------------
# Max nesting depth
# ------------------------------------------------------------------

class NestingDepth(ast.NodeVisitor):
    NESTING_NODES = (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.AsyncFor, ast.AsyncWith)

    def __init__(self):
        self.max_depth = 0
        self.cur_depth = 0

    def visit(self, node):
        if isinstance(node, self.NESTING_NODES):
            self.cur_depth += 1
            if self.cur_depth > self.max_depth:
                self.max_depth = self.cur_depth
            self.generic_visit(node)
            self.cur_depth -= 1
        else:
            self.generic_visit(node)


def max_nesting_of(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return 0
    v = NestingDepth()
    v.visit(tree)
    return v.max_depth


# ------------------------------------------------------------------
# Average function length
# ------------------------------------------------------------------

def avg_func_length(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return 0.0
    lengths = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body:
                first = node.body[0].lineno
                line_nums = []
                for n in ast.walk(node):
                    end = getattr(n, 'end_lineno', None)
                    line = getattr(n, 'lineno', None)
                    if end is not None:
                        line_nums.append(end)
                    elif line is not None:
                        line_nums.append(line)
                last = max(line_nums) if line_nums else first
                lengths.append(last - first + 1)
    return sum(lengths) / len(lengths) if lengths else 0.0


# ------------------------------------------------------------------
# Code smells: basic counters
# ------------------------------------------------------------------

SMELL_PATTERNS = [
    (r'\bglobal\s+\w', 'globals'),
    (r'\btry\s*:', 'try'),
    (r'\bexcept\s*:', 'bare_except'),
    (r'\bif\s+True\s*:', 'if_true'),
    (r'\b__main__\b', 'main_check'),
]
LONG_LINE_THRESHOLD = 100
MAGIC_NUM_THRESHOLD = 10  # numeric literals not in {-1,0,1,2,10,100,1000}
MAGIC_NUMBERS_OK = {-1, 0, 1, 2, 10, 100, 1000, 10000}


def count_smells(src):
    smells = 0
    # Pattern-based
    for pat, _ in SMELL_PATTERNS:
        smells += len(re.findall(pat, src))
    # Long lines
    for line in src.split('\n'):
        if len(line) > LONG_LINE_THRESHOLD:
            smells += 1
    # Magic numbers
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return smells
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value not in MAGIC_NUMBERS_OK:
                smells += 1
    return smells


# ------------------------------------------------------------------
# Duplicate code (very basic line-level)
# ------------------------------------------------------------------

def duplicate_pct(src):
    lines = [l.strip() for l in src.split('\n') if l.strip() and not l.strip().startswith('#')]
    if not lines:
        return 0.0
    counts = {}
    for l in lines:
        counts[l] = counts.get(l, 0) + 1
    dup = sum(c - 1 for c in counts.values() if c > 1)
    return 100.0 * dup / len(lines)


# ------------------------------------------------------------------
# Main extraction
# ------------------------------------------------------------------

def extract(src_path):
    src = src_path.read_text(encoding="utf-8")
    metrics = {}

    # Radon raw metrics
    raw = analyze(src)
    metrics["LOC_Total"] = raw.loc
    metrics["LOC_Code"] = raw.sloc
    metrics["LOC_Comment"] = raw.comments
    metrics["Comment_Density"] = (raw.comments / raw.loc * 100) if raw.loc else 0.0

    # Cyclomatic complexity
    try:
        cc_results = cc_visit(src)
        ccs = [b.complexity for b in cc_results]
        metrics["CC_Average"] = sum(ccs) / len(ccs) if ccs else 0.0
        metrics["CC_Max"] = max(ccs) if ccs else 0
        metrics["CC_Functions"] = len(ccs)
    except Exception:
        metrics["CC_Average"] = 0.0
        metrics["CC_Max"] = 0
        metrics["CC_Functions"] = 0

    # Maintainability Index
    try:
        mi = mi_visit(src, multi=True)
        metrics["MI_Score"] = float(mi)
    except Exception:
        metrics["MI_Score"] = 0.0
    mi_score = metrics["MI_Score"]
    metrics["MI_Rank"] = "A" if mi_score >= 20 else ("B" if mi_score >= 10 else "C")

    # Halstead metrics
    try:
        h = h_visit(src)
        # h.total is a HalsteadReport namedtuple
        metrics["H_Volume"] = float(h.total.volume)
        metrics["H_Difficulty"] = float(h.total.difficulty)
        metrics["H_Effort"] = float(h.total.effort)
        metrics["H_Bugs"] = float(h.total.bugs)
    except Exception:
        metrics["H_Volume"] = 0.0
        metrics["H_Difficulty"] = 0.0
        metrics["H_Effort"] = 0.0
        metrics["H_Bugs"] = 0.0

    metrics["Cognitive_CC"] = cognitive_complexity_of(src)
    metrics["Max_Nesting"] = max_nesting_of(src)
    metrics["Avg_Func_Length"] = avg_func_length(src)
    metrics["Code_Smells"] = count_smells(src)
    metrics["Duplicate_Pct"] = duplicate_pct(src)

    return metrics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="manifest.json")
    ap.add_argument("--tasks-dir", default="tasks")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)
    tasks_dir = Path(args.tasks_dir).resolve()

    rows = []
    for entry in manifest["tasks"]:
        tid = entry["id"]
        name = entry["name"]
        category = entry["category"]
        n_param = entry["n_param"]
        for ver in ("v1_clean", "v2_medium", "v3_bad"):
            path = tasks_dir / ver / f"p{tid:02d}_{name}.py"
            if not path.exists():
                continue
            m = extract(path)
            m.update({
                "task_id": tid,
                "name": name,
                "category": category,
                "version": ver,
                "n_param": n_param,
            })
            rows.append(m)

    df = pd.DataFrame(rows)
    # Reorder columns
    front = ["task_id", "name", "category", "version", "n_param"]
    other = [c for c in df.columns if c not in front]
    df = df[front + other]
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(df)} rows to {args.output}")
    # Sanity check: print per-version stats
    print("\nPer-version means:")
    print(df.groupby("version")[
        ["CC_Average", "Cognitive_CC", "Max_Nesting", "Code_Smells", "MI_Score", "H_Effort"]
    ].mean().round(2))


if __name__ == "__main__":
    main()

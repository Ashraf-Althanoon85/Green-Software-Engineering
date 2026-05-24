"""Quick test of first 20 tasks (and report on each)."""
import json, subprocess, time, sys
from pathlib import Path

ROOT = Path(__file__).parent
TASKS_DIR = ROOT / "tasks"

with open(ROOT / "manifest.json") as f:
    manifest = json.load(f)

# Test the first N tasks
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--from-id", type=int, default=1)
ap.add_argument("--to-id", type=int, default=20)
ap.add_argument("--timeout", type=int, default=60)
args = ap.parse_args()

results = []
for entry in manifest["tasks"]:
    if not (args.from_id <= entry["id"] <= args.to_id):
        continue
    task_id = entry["id"]
    name = entry["name"]
    outputs = {}
    times = {}
    failed = False
    for ver in ("v1_clean", "v2_medium", "v3_bad"):
        path = TASKS_DIR / ver / f"p{task_id:02d}_{name}.py"
        t0 = time.time()
        try:
            r = subprocess.run(
                ["python", str(path)],
                capture_output=True, text=True, timeout=args.timeout,
                cwd=str(TASKS_DIR),
            )
            dt = time.time() - t0
            if r.returncode != 0:
                outputs[ver] = f"ERR({r.returncode}):{r.stderr[:50]}"
                failed = True
            else:
                outputs[ver] = r.stdout.strip()
            times[ver] = dt
        except subprocess.TimeoutExpired:
            outputs[ver] = "TIMEOUT"
            times[ver] = args.timeout
            failed = True
    match = outputs["v1_clean"] == outputs["v2_medium"] == outputs["v3_bad"] and not failed
    sym = "OK" if match else "FAIL"
    print(f"{task_id:>3}  {name:<25}  [{sym}]  T={times.get('v1_clean',0):.1f}/{times.get('v2_medium',0):.1f}/{times.get('v3_bad',0):.1f}s   v1={outputs.get('v1_clean','')[:30]}")
    if not match:
        print(f"        v2={outputs.get('v2_medium','')[:60]}")
        print(f"        v3={outputs.get('v3_bad','')[:60]}")
    results.append({"id": task_id, "name": name, "match": match, "outputs": outputs, "times": times})
    sys.stdout.flush()

n_ok = sum(1 for r in results if r["match"])
print(f"\nPassed: {n_ok}/{len(results)}")

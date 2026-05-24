"""
measure_energy.py — measures CPU energy via Intel Power Gadget on Windows
for all 300 program variants in the benchmark.

USAGE (run in PowerShell as Administrator):
    cd C:\\path\\to\\benchmark_v2
    python measure_energy.py --runs 5 --output measured_energy.csv

Optional arguments:
    --runs N         repetitions per program (default 5)
    --from-id N      start at task id (default 1)
    --to-id N        end at task id (default 100)
    --cooldown S     seconds between runs (default 2)
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from io import StringIO
from pathlib import Path

import pandas as pd


# ------------------------------------------------------------------
# Locate PowerLog3.0.exe
# ------------------------------------------------------------------
def find_powerlog():
    env = os.environ.get("IPG_Dir")
    if env:
        p = Path(env) / "PowerLog3.0.exe"
        if p.exists():
            return str(p)
    candidates = [
        r"C:\Program Files\Intel\Power Gadget 3.6\PowerLog3.0.exe",
        r"C:\Program Files\Intel\Power Gadget 3.5\PowerLog3.0.exe",
        r"C:\Program Files (x86)\Intel\Power Gadget 3.6\PowerLog3.0.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    raise FileNotFoundError("PowerLog3.0.exe not found. Install Intel Power Gadget 3.6.")


# ------------------------------------------------------------------
# Parse PowerLog CSV output
# ------------------------------------------------------------------
def parse_log(csv_path):
    """Return (total_joules, duration_s, avg_cpu_pct, mean_freq_mhz)."""
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    header_idx = None
    for i, line in enumerate(lines):
        if "Elapsed Time" in line and "Cumulative" in line:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"PowerLog CSV unreadable: {csv_path}")
    data_lines = []
    for line in lines[header_idx:]:
        line = line.strip()
        if not line:
            break
        data_lines.append(line)
    df = pd.read_csv(StringIO("\n".join(data_lines)))
    df.columns = [c.strip() for c in df.columns]
    joule_col = next((c for c in df.columns if "Cumulative Processor Energy" in c and "Joules" in c), None)
    time_col = next((c for c in df.columns if "Elapsed Time" in c), None)
    cpu_col = next((c for c in df.columns if "CPU Utilization" in c), None)
    freq_col = next((c for c in df.columns if "CPU Frequency" in c), None)
    if joule_col is None or time_col is None:
        raise ValueError(f"Required columns missing in {csv_path}")
    total_j = float(df[joule_col].iloc[-1])
    duration = float(df[time_col].iloc[-1])
    avg_cpu = float(df[cpu_col].mean()) if cpu_col else 0.0
    mean_freq = float(df[freq_col].mean()) if freq_col else 0.0
    return total_j, duration, avg_cpu, mean_freq


# ------------------------------------------------------------------
# Single measurement
# ------------------------------------------------------------------
def measure_one(powerlog, program_path, working_dir, runs, cooldown, timeout):
    """Run program `runs` times under PowerLog. Return list of dicts."""
    results = []
    for r in range(runs):
        log_file = (Path.cwd() / f"_pwlog_{os.getpid()}_{r}.csv").absolute()
        if log_file.exists():
            log_file.unlink()
        cmd = [
            powerlog, "-resolution", "100",
            "-file", str(log_file),
            "-cmd", sys.executable, str(program_path),
        ]
        try:
            p = subprocess.run(
                cmd,
                capture_output=True, text=True,
                timeout=timeout, cwd=str(working_dir),
            )
            if p.returncode != 0:
                print(f"    run {r}: returncode={p.returncode}", file=sys.stderr)
                continue
        except subprocess.TimeoutExpired:
            print(f"    run {r}: TIMEOUT (>{timeout}s)", file=sys.stderr)
            continue
        except Exception as e:
            print(f"    run {r}: {e}", file=sys.stderr)
            continue
        try:
            j, dur, cpu, freq = parse_log(log_file)
            results.append({
                "run": r, "joules": j, "duration_s": dur,
                "cpu_pct": cpu, "freq_mhz": freq,
            })
        except Exception as e:
            print(f"    run {r}: parse error: {e}", file=sys.stderr)
        finally:
            if log_file.exists():
                log_file.unlink()
        time.sleep(cooldown)
    return results


# ------------------------------------------------------------------
# Driver
# ------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="manifest.json")
    ap.add_argument("--tasks-dir", default="tasks")
    ap.add_argument("--output", required=True)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--cooldown", type=float, default=2.0)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--from-id", type=int, default=1)
    ap.add_argument("--to-id", type=int, default=100)
    ap.add_argument("--versions", nargs="+",
                    default=["v1_clean", "v2_medium", "v3_bad"])
    args = ap.parse_args()

    powerlog = find_powerlog()
    print(f"[info] PowerLog: {powerlog}")

    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    tasks_dir = Path(args.tasks_dir).resolve()

    all_rows = []
    # Resume support: read existing rows if file exists
    output_path = Path(args.output)
    done_keys = set()
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_rows.append(row)
                done_keys.add((row["task_id"], row["version"]))
        print(f"[info] Found {len(all_rows)} existing rows; resuming.")

    n_total = sum(1 for t in manifest["tasks"] if args.from_id <= t["id"] <= args.to_id) * len(args.versions)
    done_count = 0
    for entry in manifest["tasks"]:
        tid = entry["id"]
        if not (args.from_id <= tid <= args.to_id):
            continue
        name = entry["name"]
        for ver in args.versions:
            done_count += 1
            key = (str(tid), ver)
            if key in done_keys:
                continue
            prog = tasks_dir / ver / f"p{tid:02d}_{name}.py"
            if not prog.exists():
                print(f"[skip] {prog} missing")
                continue
            print(f"[{done_count}/{n_total}] task {tid:>3} {name:<25} {ver}")
            runs = measure_one(powerlog, prog, tasks_dir, args.runs, args.cooldown, args.timeout)
            if not runs:
                print(f"    -> no successful runs")
                continue
            df = pd.DataFrame(runs)
            row = {
                "task_id": tid,
                "name": name,
                "category": entry["category"],
                "version": ver,
                "n_param": entry["n_param"],
                "runs_completed": len(runs),
                "joules_mean": df["joules"].mean(),
                "joules_std": df["joules"].std() if len(runs) > 1 else 0.0,
                "joules_min": df["joules"].min(),
                "joules_max": df["joules"].max(),
                "duration_s_mean": df["duration_s"].mean(),
                "duration_s_std": df["duration_s"].std() if len(runs) > 1 else 0.0,
                "cpu_pct_mean": df["cpu_pct"].mean(),
                "freq_mhz_mean": df["freq_mhz"].mean(),
            }
            all_rows.append(row)
            print(f"    -> {row['joules_mean']:.2f} J (±{row['joules_std']:.2f}), "
                  f"{row['duration_s_mean']:.2f}s")
            # Append-save after each measurement (in case of crash)
            df_all = pd.DataFrame(all_rows)
            df_all.to_csv(output_path, index=False)

    print(f"\n[done] Wrote {len(all_rows)} rows to {output_path}")


if __name__ == "__main__":
    main()

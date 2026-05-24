# Benchmark v2 — Green Software Engineering

A 100-task × 3-version benchmark for studying the relationship between static code quality metrics and CPU energy consumption.

## What is this?

- **100 computational tasks** distributed over 5 categories:
  - Sorting & searching (25)
  - Parsing & string processing (25)
  - Numerical computing (20)
  - String algorithms (15)
  - Data structures & graphs (15)
- **Each task has 3 quality variants** that produce **identical output** on **identical input**:
  - `v1_clean`: idiomatic Python with docstrings, type hints, low CC
  - `v2_medium`: same logic with smells (long names, magic numbers, no docs)
  - `v3_bad`: anti-patterns (deep nesting, globals, try/except in loops, dead branches)
- **All 300 programs verified for functional equivalence** (100/100 pass).

## Files

| File | Purpose |
|------|---------|
| `tasks/v1_clean/p*.py` | 100 clean implementations |
| `tasks/v2_medium/p*.py` | 100 medium-quality implementations |
| `tasks/v3_bad/p*.py` | 100 bad-quality implementations |
| `tasks/shared_input.py` | Deterministic input fixtures |
| `manifest.json` | Task ID → file mapping + metadata |
| `builder.py` | AST-based code transformer (V1 → V2 → V3) |
| `tasks_sorting.py`, `tasks_parsing.py`, `tasks_remaining.py` | Task definitions |
| `generate_all_tasks.py` | Re-generate all 300 files from definitions |
| `test_range.py` | Functional equivalence + runtime test |
| `extract_static_metrics.py` | Compute 16+ static metrics |
| `measure_energy.py` | Intel Power Gadget measurement (Windows) |
| `static_metrics.csv` | Pre-computed static metrics for 300 programs |
| `test_results.json` | Functional equivalence verification |

## How to use (on your Windows + Skylake machine)

### 1) Prerequisites

```powershell
# Ensure Python 3.9+ is available
python --version

# Install dependencies
pip install pandas numpy scipy matplotlib radon
```

Intel Power Gadget 3.6 must already be installed (you did this).

### 2) Verify functional equivalence (optional, ~10 minutes)

```powershell
# Test all 100 tasks
python test_range.py --from-id 1 --to-id 100 --timeout 60
```

Expected: `Passed: 100/100`.

### 3) Measure energy (~30-90 minutes depending on runtimes)

Open PowerShell **as Administrator**, then:

```powershell
cd C:\path\to\benchmark_v2
python measure_energy.py --runs 5 --output measured_energy.csv
```

The script:
- Runs each of the 300 programs 5 times under Intel Power Gadget
- Reads CPU energy in Joules from RAPL via the package-level MSR
- Saves results incrementally (resumes if interrupted)
- Records mean, std, min, max for joules and duration

### 4) Static metrics already extracted

`static_metrics.csv` is included. To regenerate:

```powershell
python extract_static_metrics.py --output static_metrics.csv
```

### 5) Send me back

Once measurement completes, send me:
- `measured_energy.csv`
- `static_metrics.csv`
- `test_results.json`

I will:
- Train GPR, MLP, NGBoost on the real measurements
- Add tabular baselines (Random Forest, XGBoost, LightGBM, Elastic Net, SVR)
- Generate all figures and tables
- Rewrite the paper end-to-end with the new, real data

## Design rationale

Each program does **real work** that runs for 0.5–15 seconds in pure Python on a modern CPU.
This is critical because:
1. Programs shorter than 100ms are dominated by Python interpreter startup
2. RAPL has 100ms sampling resolution; sub-100ms programs yield 1-2 samples
3. The original v1 benchmark consisted of stubs that ran in ~30 ms; meaningful energy correlations were impossible

## Authoring notes (for your records)

- Inputs are deterministic (seeded RNG) so different runs of the same program see identical work
- All three versions of a task call `shared_input.get_*()` with the same `TASK_ID`
- The `checksum()` function (and its `cs()` variants in v2, v3) deterministically hashes the output
- If any V1/V2/V3 trio disagrees on checksum, it's a bug; `test_range.py` catches this

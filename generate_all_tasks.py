"""Generate all 300 program files (100 tasks x 3 versions)."""

from pathlib import Path
import json
import sys
import traceback

from tasks_sorting import SORTING_TASKS
from tasks_parsing import PARSING_TASKS
from tasks_remaining import REMAINING_TASKS
from builder import write_task

ROOT = Path(__file__).parent
TASKS_DIR = ROOT / "tasks"

# Combine all tasks
ALL_TASKS = SORTING_TASKS + PARSING_TASKS + REMAINING_TASKS
assert len(ALL_TASKS) == 100, f"Expected 100 tasks, got {len(ALL_TASKS)}"

# Ensure clean state
for ver in ("v1_clean", "v2_medium", "v3_bad"):
    d = TASKS_DIR / ver
    d.mkdir(parents=True, exist_ok=True)
    for f in d.glob("p*.py"):
        f.unlink()

# Write each task
manifest = []
errors = []
for t in ALL_TASKS:
    try:
        write_task(t, TASKS_DIR)
        manifest.append({
            "id": t.task_id,
            "name": t.name,
            "category": t.category,
            "n_param": t.n,
            "files": [
                f"v1_clean/p{t.task_id:02d}_{t.name}.py",
                f"v2_medium/p{t.task_id:02d}_{t.name}.py",
                f"v3_bad/p{t.task_id:02d}_{t.name}.py",
            ],
        })
    except Exception as e:
        errors.append((t.task_id, t.name, str(e), traceback.format_exc()))
        print(f"ERROR task {t.task_id} ({t.name}): {e}", file=sys.stderr)

print(f"Generated {len(manifest)} task triplets ({len(manifest) * 3} files)")
if errors:
    print(f"Errors: {len(errors)}")
    for err in errors[:5]:
        print(f"  task {err[0]} ({err[1]}): {err[2]}")

(ROOT / "manifest.json").write_text(json.dumps({"tasks": manifest}, indent=2), encoding="utf-8")
print("Wrote manifest.json")

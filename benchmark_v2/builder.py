"""
Smart task builder: takes a clean function body + input spec,
auto-generates the medium and bad versions by AST rewriting + decorators.

For each task we only define:
  - The clean implementation (single function returning a value)
  - The input fixture call
  - The N parameter

The builder produces three .py files:
  - V1: clean code as written
  - V2: same code with mechanical degradations (rename, while-ify, strip docs)
  - V3: same code wrapped in nested ifs, globalized, with try/except in loops
"""

import ast
import re
import textwrap
from pathlib import Path


# ============================================================
# Standard checksum implementations (drop-in)
# ============================================================

CHECKSUM_CLEAN = textwrap.dedent('''
    def checksum(arr):
        total = 0
        for i, x in enumerate(arr):
            if isinstance(x, (int, float)):
                v = int(x * 1000) if isinstance(x, float) else x
            elif isinstance(x, str):
                v = sum(ord(c) for c in x)
            elif isinstance(x, (tuple, list)):
                v = sum(int(y * 1000) if isinstance(y, float) else (sum(ord(c) for c in y) if isinstance(y, str) else int(y)) for y in x)
            else:
                v = hash(x) & 0xFFFFFFFF
            total = (total + (i + 1) * v) % 1_000_000_007
        return total
''').strip()

CHECKSUM_MEDIUM = textwrap.dedent('''
    def cs(a):
        s = 0
        i = 0
        while i < len(a):
            x = a[i]
            if isinstance(x, (int, float)):
                v = int(x * 1000) if isinstance(x, float) else x
            elif isinstance(x, str):
                v = sum(ord(c) for c in x)
            elif isinstance(x, (tuple, list)):
                v = 0
                for y in x:
                    if isinstance(y, float):
                        v = v + int(y * 1000)
                    elif isinstance(y, str):
                        v = v + sum(ord(c) for c in y)
                    else:
                        v = v + int(y)
            else:
                v = hash(x) & 0xFFFFFFFF
            s = (s + (i + 1) * v) % 1000000007
            i = i + 1
        return s
''').strip()

CHECKSUM_BAD = textwrap.dedent('''
    g_sum = 0
    def cs(a):
        global g_sum
        g_sum = 0
        i = 0
        while i < len(a):
            try:
                x = a[i]
                if isinstance(x, (int, float)):
                    if isinstance(x, float):
                        v = int(x * 1000)
                    else:
                        v = x
                elif isinstance(x, str):
                    v = 0
                    for c in x:
                        v = v + ord(c)
                elif isinstance(x, (tuple, list)):
                    v = 0
                    for y in x:
                        try:
                            if isinstance(y, float):
                                v = v + int(y * 1000)
                            elif isinstance(y, str):
                                vv = 0
                                for c in y:
                                    vv = vv + ord(c)
                                v = v + vv
                            else:
                                v = v + int(y)
                        except Exception:
                            pass
                else:
                    v = hash(x) & 0xFFFFFFFF
                g_sum = (g_sum + (i + 1) * v) % 1000000007
            except Exception:
                pass
            i = i + 1
        return g_sum
''').strip()


HEADER = textwrap.dedent('''
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from shared_input import get_int_array, get_float_array, get_string_array, get_int_pairs
''').strip()


# ============================================================
# Code degradation passes (V1 -> V2)
# ============================================================

def to_medium(clean_src: str) -> str:
    """
    Transform clean code into medium-quality:
      - Remove docstrings (the first stmt in functions that is a string literal)
      - Remove type hints in function signatures and returns
      - Remove type-annotated variable declarations (x: int = 5)
      - Convert `for i in range(n):` to while loops (some)
      - Use shorter variable names (one mechanical pass)
      - Remove inline comments
    """
    tree = ast.parse(clean_src)

    class MediumTransformer(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            # Strip docstring
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body = node.body[1:] or [ast.Pass()]
            # Strip return type hint
            node.returns = None
            # Strip arg type hints
            for arg in node.args.args:
                arg.annotation = None
            self.generic_visit(node)
            return node

        def visit_AnnAssign(self, node):
            # x: int = 5  =>  x = 5
            if node.value is not None:
                return ast.Assign(targets=[node.target], value=node.value, lineno=node.lineno)
            return node

    new_tree = MediumTransformer().visit(tree)
    ast.fix_missing_locations(new_tree)
    src = ast.unparse(new_tree)
    # Strip inline comments (best effort)
    src = re.sub(r'(?m)^( *)#.*$', '', src)
    src = re.sub(r' +#.*$', '', src, flags=re.MULTILINE)
    src = re.sub(r'\n\s*\n', '\n\n', src)
    return src


# ============================================================
# Code degradation passes (V1 -> V3)
# ============================================================

def to_bad(clean_src: str) -> str:
    """
    Transform clean code into bad-quality:
      - All function args become globals (simulated by reading from module globals)
      - Wrap every if-statement in a redundant `if True:`
      - Wrap loop bodies in try/except
      - Strip docs and type hints
    """
    tree = ast.parse(clean_src)

    class BadTransformer(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            # Strip docstring & type hints
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body = node.body[1:] or [ast.Pass()]
            node.returns = None
            for arg in node.args.args:
                arg.annotation = None
            self.generic_visit(node)
            return node

        def visit_For(self, node):
            # Wrap loop body in try/except
            self.generic_visit(node)
            new_body = [
                ast.Try(
                    body=node.body,
                    handlers=[ast.ExceptHandler(type=ast.Name(id='Exception', ctx=ast.Load()), name=None, body=[ast.Pass()])],
                    orelse=[],
                    finalbody=[],
                )
            ]
            node.body = new_body
            return node

        def visit_While(self, node):
            self.generic_visit(node)
            new_body = [
                ast.Try(
                    body=node.body,
                    handlers=[ast.ExceptHandler(type=ast.Name(id='Exception', ctx=ast.Load()), name=None, body=[ast.Pass()])],
                    orelse=[],
                    finalbody=[],
                )
            ]
            node.body = new_body
            return node

        def visit_If(self, node):
            self.generic_visit(node)
            # Wrap in `if True:`
            return ast.If(
                test=ast.Constant(value=True),
                body=[node],
                orelse=[],
            )

        def visit_AnnAssign(self, node):
            if node.value is not None:
                return ast.Assign(targets=[node.target], value=node.value, lineno=node.lineno)
            return node

    new_tree = BadTransformer().visit(tree)
    ast.fix_missing_locations(new_tree)
    src = ast.unparse(new_tree)
    src = re.sub(r'(?m)^( *)#.*$', '', src)
    src = re.sub(r' +#.*$', '', src, flags=re.MULTILINE)
    return src


# ============================================================
# Builder API
# ============================================================

class Task:
    def __init__(self, task_id, name, category, n, clean_body, main_body):
        self.task_id = task_id
        self.name = name
        self.category = category
        self.n = n
        self.clean_body = textwrap.dedent(clean_body).strip()
        self.main_body = textwrap.dedent(main_body).strip()

    def assemble_clean(self):
        return (
            HEADER + "\n\n"
            f"TASK_ID = {self.task_id}\n"
            f"N = {self.n}\n\n"
            + self.clean_body + "\n\n"
            + CHECKSUM_CLEAN + "\n\n"
            "def main():\n"
            + textwrap.indent(self.main_body, "    ") + "\n\n"
            'if __name__ == "__main__":\n'
            '    print(main())\n'
        )

    def assemble_medium(self):
        # Apply medium transform to body + main + checksum
        body_med = to_medium(self.clean_body)
        main_med = to_medium("def __main__():\n" + textwrap.indent(self.main_body, "    "))
        # Extract just the body of __main__
        m = re.search(r'def __main__\(\):\n(.*?)$', main_med, re.DOTALL)
        main_inner = m.group(1) if m else self.main_body
        # Rename checksum -> cs in main_inner
        main_inner = re.sub(r'\bchecksum\b', 'cs', main_inner)
        return (
            HEADER + "\n\n"
            f"TASK_ID = {self.task_id}\n"
            f"N = {self.n}\n\n"
            + body_med + "\n\n"
            + CHECKSUM_MEDIUM + "\n\n"
            "def main():\n"
            + main_inner + "\n\n"
            'if __name__ == "__main__":\n'
            '    print(main())\n'
        )

    def assemble_bad(self):
        body_bad = to_bad(self.clean_body)
        main_bad = to_bad("def __main__():\n" + textwrap.indent(self.main_body, "    "))
        m = re.search(r'def __main__\(\):\n(.*?)$', main_bad, re.DOTALL)
        main_inner = m.group(1) if m else self.main_body
        main_inner = re.sub(r'\bchecksum\b', 'cs', main_inner)
        return (
            HEADER + "\n\n"
            f"TASK_ID = {self.task_id}\n"
            f"N = {self.n}\n\n"
            + body_bad + "\n\n"
            + CHECKSUM_BAD + "\n\n"
            "def main():\n"
            + main_inner + "\n\n"
            'if __name__ == "__main__":\n'
            '    print(main())\n'
        )


def write_task(t: Task, root: Path):
    fname = f"p{t.task_id:02d}_{t.name}.py"
    (root / "v1_clean" / fname).write_text(t.assemble_clean(), encoding="utf-8")
    (root / "v2_medium" / fname).write_text(t.assemble_medium(), encoding="utf-8")
    (root / "v3_bad" / fname).write_text(t.assemble_bad(), encoding="utf-8")

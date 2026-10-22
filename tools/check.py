# -*- coding: utf-8 -*-
"""把文中所有 ```python 代码块抽出来逐个执行，检查示例是否真的跑得通。

用法：
    python tools/check.py        # 逐个运行并汇总；有失败则返回码 1
    python tools/check.py -v     # 同时打印每个代码块的位置与首条输出

判定：
    ✓ 独立跑通            代码块自己就能跑
    ⊘ 依赖同文件前文      需要先执行同一文件里更早的代码块（章节式讲义常见）
    ⊘ 桩下通过            本机没装 matplotlib/scipy 等，用替身跑通；数值逻辑验证过，绘图效果未验证
    ⊘ 缺库跳过            真的需要那个库才能跑
    ✗ 失败                代码本身有错
"""
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^```(\w*)\s*$")
SKIP_LIBS = ("matplotlib", "mpl_toolkits", "scipy", "gudhi", "networkx", "torch",
             "pymc", "cvxpy", "sympy", "sklearn", "pandas")

# 只给"画图"类库装替身：它们不产出被断言比较的数值，替身不会掩盖数学错误
STUB = '''
import sys, types
class _Stub:
    def __getattr__(self, k): return _Stub()
    def __call__(self, *a, **k): return _Stub()
    def __getitem__(self, k): return _Stub()
    def __setitem__(self, k, v): None
    def __iter__(self): return iter((_Stub(), _Stub()))   # 兼容 fig, ax = plt.subplots(...)
for _name in ("matplotlib", "matplotlib.pyplot", "matplotlib.colors",
              "mpl_toolkits", "mpl_toolkits.mplot3d"):
    if _name not in sys.modules:
        _m = types.ModuleType(_name)
        _m.__getattr__ = lambda k: _Stub()
        sys.modules[_name] = _m
'''


def blocks():
    """→ [(相对路径, 起始行, 代码)]，按文件分组、文件内保持顺序。"""
    found = []
    for dirpath, dirnames, files in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in (".git", "tools"))
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            lines = open(path, encoding="utf-8").read().split("\n")
            lang, start, buf = None, 0, None
            for i, line in enumerate(lines, 1):
                m = FENCE.match(line)
                if m and buf is None:
                    lang, start, buf = m.group(1), i, []
                    continue
                if line.strip() == "```" and buf is not None:
                    if lang == "python":
                        found.append((rel, start, "\n".join(buf)))
                    lang, buf = None, None
                    continue
                if buf is not None:
                    buf.append(line)
    return found


def run(code, stub=False):
    """→ (status, message)；status ∈ ok / skip / fail。"""
    body = (STUB + "\n") if stub else ""
    body += code + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        script = os.path.join(tmp, "snippet.py")
        with open(script, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
                   MPLBACKEND="Agg")
        try:
            p = subprocess.run([sys.executable, script], cwd=tmp, env=env,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=120)
        except subprocess.TimeoutExpired:
            return "fail", "TimeOut: 超过 120 秒"
    if p.returncode == 0:
        return "ok", p.stdout.strip()
    for line in reversed((p.stderr or "").strip().split("\n")):
        if re.match(r"^\w*(Error|Exception)", line.strip()):
            if any(lib in line for lib in SKIP_LIBS):
                return "skip", line.strip()
            return "fail", line.strip()
    return "fail", "未知错误"


def judge(code, context):
    """依次尝试：独立 → 接前文 → 接前文+替身 → 仅替身。"""
    status, msg = run(code)
    if status == "ok":
        return "ok", msg
    if context:
        s2, m2 = run("\n\n".join(context + [code]))
        if s2 == "ok":
            return "context", "依赖同文件前文"
        if s2 == "skip" and not any(lib in m2 for lib in ("matplotlib", "mpl_toolkits")):
            return "skip", m2
    last = msg
    candidates = [context + [code], [code]] if context else [[code]]
    for i, parts in enumerate(candidates):
        s3, m3 = run("\n\n".join(parts), stub=True)
        if s3 == "ok":
            return "stub", "绘图用替身，数值逻辑已验证"
        if s3 == "skip" and not any(lib in m3 for lib in ("matplotlib", "mpl_toolkits")):
            return "skip", m3
        if i == 0:                      # 保留信息量最大的那次报错
            last = m3
    return ("skip" if status == "skip" else "fail"), last


def main():
    verbose = "-v" in sys.argv
    items = blocks()
    by_file = {}
    for rel, line, code in items:
        by_file.setdefault(rel, []).append((line, code))

    results, context = [], {}
    for rel, seq in by_file.items():
        acc = []
        for line, code in seq:
            status, msg = judge(code, acc)
            results.append((status, rel, line, msg))
            if verbose:
                tag = {"ok": "✓", "context": "⊘", "stub": "⊘", "skip": "⊘", "fail": "✗"}[status]
                print("%-4s %s:%d  %s" % (tag, rel, line, msg.split("\n")[0]))
            acc.append(code)

    def n(s):
        return sum(1 for r in results if r[0] == s)

    print("扫描到 %d 个 Python 代码块（%d 个文件）" % (len(items), len(by_file)))
    print("✓ 独立跑通 %d    ⊘ 依赖前文 %d    ⊘ 桩下通过 %d（绘图未验证）    ⊘ 缺库 %d    ✗ 失败 %d"
          % (n("ok"), n("context"), n("stub"), n("skip"), n("fail")))
    libs = sorted({r[3].split("'")[1] for r in results if r[0] == "skip" and "'" in r[3]})
    if libs:
        print("  缺的库：" + ", ".join(libs))
    for status, rel, line, msg in results:
        if status == "fail":
            print("✗ %s:%d  %s" % (rel, line, msg))
    return 1 if n("fail") else 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""把 math.md（唯一真相源）分发到目录树与根 README。

用法：
    python tools/build.py            # 重新生成 README.md 与各主题目录的 index.md
    python tools/build.py --check    # 只校验：链接是否可解析、编号是否与目录对齐

约定：
* math.md 里 `# 层级 N：X` 切分层级，`### N. 标题` 切分条目，`## 组名` 是组标签。
* 每个条目对应 `<层级目录>/<NN-标题>/index.md`，目录名由条目编号决定。
* level-2-concrete/05-线性代数 是手写的 12 章讲义，build.py 不覆盖它（见 EXPANDED）。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "math.md")

LEVELS = [
    ("0", "level-0-meta", "元框架"),
    ("0.5", "level-0.5-category-toolkit", "范畴论基础工具箱"),
    ("1", "level-1-abstract", "抽象结构层"),
    ("2", "level-2-concrete", "具体实例层"),
    ("3", "level-3-applied", "模型与计算层"),
]
LEVEL_TITLE = {"0": "层级 0：元框架", "0.5": "层级 0.5：范畴论基础工具箱",
               "1": "层级 1：抽象结构层", "2": "层级 2：具体结构层",
               "3": "层级 3：模型与计算层"}
EXPANDED = {"level-2-concrete/05-线性代数"}          # 手写模块，生成器跳过
BANNER = "<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->\n"


def read_source():
    with open(SOURCE, encoding="utf-8", newline="") as fh:
        return fh.read().replace("\r\n", "\n")


def parse(text):
    """→ [{level, num, title, group, body}]，body 是去掉 `### …` 标题后的正文行。"""
    lines = text.split("\n")
    sections, level, group = [], None, None
    intro, cur = {}, None

    for line in lines:
        m = re.match(r"^# 层级 ([\d.]+)：(.+)$", line)
        if m:
            level, group, cur = m.group(1), None, None
            intro[level] = []
            continue
        if level is None:
            continue
        if cur is None and not line.startswith("### "):
            if line.strip() and not line.startswith("#"):
                intro[level].append(line.strip())
            continue
        if line.startswith("## ") and not line.startswith("### "):
            group = line[3:].strip()
            cur = None
            continue
        m = re.match(r"^###\s+(?:(\d+)\.\s*)?(.+?)\s*$", line)
        if m:
            cur = {"level": level, "num": int(m.group(1)) if m.group(1) else None,
                   "title": m.group(2), "group": group, "body": []}
            sections.append(cur)
            continue
        if cur is not None:
            cur["body"].append(line)

    for s in sections:                      # 去掉正文尾部多余的分隔线与空行
        body = s["body"]
        while body and (body[-1].strip() == "" or body[-1].strip() == "---"):
            body.pop()
        s["body"] = body
    return sections, intro


def level_dirs(root_name):
    path = os.path.join(ROOT, root_name)
    return sorted(d for d in os.listdir(path)
                  if os.path.isdir(os.path.join(path, d)))


def resolve(sections):
    """给每个条目挂上目录名；编号必须与目录前缀一一对应。"""
    errors, plan = [], []
    for lvl, root_name, _ in LEVELS:
        items = [s for s in sections if s["level"] == lvl]
        dirs = level_dirs(root_name)
        if len(items) != len(dirs):
            errors.append("%s：math.md 有 %d 条，目录有 %d 个" % (root_name, len(items), len(dirs)))
            continue
        for s in items:
            if s["num"] is None:
                if len(dirs) != 1:
                    errors.append("%s：无编号条目无法定位目录" % root_name)
                    continue
                s["dir"] = dirs[0]
            else:
                prefix = "%02d-" % s["num"]
                hit = [d for d in dirs if d.startswith(prefix)]
                if len(hit) != 1:
                    errors.append("%s：编号 %d 找不到唯一目录（%s）" % (root_name, s["num"], hit))
                    continue
                s["dir"] = hit[0]
                base = hit[0][len(prefix):]
                norm = lambda t: re.sub(r"[^\w\u4e00-\u9fff]", "", t).lower()
                if norm(base) not in norm(s["title"]) and norm(s["title"]) not in norm(base):
                    errors.append("%s/%s：目录名与标题不符（%s）" % (root_name, hit[0], s["title"]))
            s["root"] = root_name
            s["path"] = "%s/%s" % (root_name, s["dir"])
            plan.append(s)
    return plan, errors


def page(s, index, total):
    level_label = LEVEL_TITLE[s["level"]]
    bits = [level_label]
    if s["group"]:
        bits.append("分组：" + s["group"])
    bits.append("第 %d/%d 条" % (index, total))
    nav = ["[总目录](../../README.md)"]
    if index > 1:
        prev = s["prev"]
        nav.insert(0, "[← %s](../%s/index.md)" % (prev["title"], prev["dir"]))
    if index < total:
        nxt = s["next"]
        nav.append("[%s →](../%s/index.md)" % (nxt["title"], nxt["dir"]))
    body = "\n".join(s["body"]).strip("\n")
    return "%s\n# %s\n\n> %s\n\n%s\n\n%s\n" % (
        BANNER, s["title"], " · ".join(bits), " · ".join(nav), body)


def build_readme(plan, intro):
    def fences(s):
        return "\n".join(s["body"]).count("```python")
    py = sum(fences(s) for s in plan)
    mma = sum("\n".join(s["body"]).count("```mathematica") for s in plan)
    out = ["# 数学范畴与应用实例", "",
           "用范畴论作统一语言，把数学拆成五个层级：**元框架 → 范畴论工具 → 抽象结构 → 具体实例 → 模型计算**。",
           "每个主题条目都给出同一套东西：`范畴` → `对象例子` → `态射例子` → `核心函子` → `Python` + `Mathematica` 双示例。", "",
           "**规模**：5 个层级 · %d 个主题条目 · %d 个 Python 示例 · %d 个 Mathematica 示例" % (len(plan), py, mma),
           "**两种读法**：通读看单文件 [math.md](math.md)；按主题跳转用下面的目录。", "",
           "## 怎么读", "",
           "| 目的 | 路径 |", "|---|---|",
           "| 建立元视角 | 层级 0：为什么用范畴论给数学分类 |",
           "| 学会语言 | 层级 0.5：范畴、函子、自然变换、米田、伴随、单子 |",
           "| 看结构 | 层级 1：代数 / 拓扑 / 几何 / 数论 / 逻辑的一般框架 |",
           "| 看实例 | 层级 2：分析、线性代数、概率统计等可以直接算的对象 |",
           "| 看算法 | 层级 3：优化、数值 PDE、机器学习、密码学等工程化模型 |",
           "| 想跑一遍 | `python tools/check.py`（逐个执行文中 Python 示例） |",
           "| 看全貌 | 三维知识地图 `map.html`：54 个条目按五个层级摆成立体结构 |", ""]

    for lvl, _, _ in LEVELS:
        items = [s for s in plan if s["level"] == lvl]
        if not items:
            continue
        out += ["## " + LEVEL_TITLE[lvl], ""]
        for line in intro.get(lvl, []):
            out += [line, ""]
        out += ["| # | 条目 | 范畴 | 代码 |", "|---|---|---|---|"]
        for s in items:
            cat = ""
            for line in s["body"]:
                if line.startswith("- 范畴："):
                    cat = line[len("- 范畴："):].strip()
                    break
            tags = []
            body = "\n".join(s["body"])
            if "```python" in body:
                tags.append("py")
            if "```mathematica" in body:
                tags.append("mma")
            if s["path"] in EXPANDED:
                tags.append("12 章讲义")
            label = s["title"] if s["num"] else s["title"]
            num = "%02d" % s["num"] if s["num"] else "—"
            out.append("| %s | [%s](%s/index.md) | %s | %s |"
                       % (num, label, s["path"], cat, " · ".join(tags)))
        out.append("")

    out += ["## 维护方式", "",
            "`math.md` 是唯一真相源；目录树与根 README 都是它的投影，不要手改生成物。", "",
            "```bash",
            "python tools/build.py           # 从 math.md 重新生成 README.md 与各主题 index.md",
            "python tools/build.py --check   # 只校验：编号↔目录是否对齐、相对链接是否都可解析",
            "python tools/check.py           # 逐个运行文中 Python 示例（-v 显示每个块的位置）",
            "python tools/site.py            # 生成静态站点 _site/（含三维交互页 /3d.html）",
            "python -m http.server 8765 --directory _site   # 打开 http://127.0.0.1:8765/",
            "```", "",
            "`check.py` 的判定分五档：独立跑通 / 依赖同文件前文 / 用 matplotlib 替身跑通"
            "（数值逻辑已验证、绘图未验证）/ 缺库跳过 / 失败。装了 `numpy` 就能跑通绝大多数示例，"
            "`scipy`、`matplotlib`、`networkx` 只影响个别条目。", "",
            "例外：`level-2-concrete/05-线性代数/` 是手写的 12 章讲义（含章节表与可视化），",
            "生成器不会覆盖它；改动请直接改该目录下的章节文件。", "",
            "> 需要 Python 3.9+。", ""]
    return "\n".join(out)


def check_links():
    bad = []
    for dirpath, _, files in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
                target = m.group(1).strip()
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = target.split("#")[0]
                if not target:
                    continue
                resolved = os.path.normpath(os.path.join(dirpath, target))
                if not os.path.exists(resolved):
                    bad.append((os.path.relpath(path, ROOT), target))
    return bad


def main():
    sections, intro = parse(read_source())
    plan, errors = resolve(sections)

    if "--check" in sys.argv:
        bad = check_links()
        for e in errors:
            print("✗ " + e)
        for path, target in bad:
            print("✗ 死链 %s → %s" % (path, target))
        if not errors and not bad:
            print("✓ 编号与链接全部通过（%d 个条目）" % len(plan))
        return 1 if (errors or bad) else 0

    if errors:
        for e in errors:
            print("✗ " + e)
        print("生成中止：先修好 math.md 的编号/标题。")
        return 1

    by_level = {}
    for s in plan:
        by_level.setdefault(s["level"], []).append(s)

    written = 0
    for lvl, _, _ in LEVELS:
        items = by_level.get(lvl, [])
        for i, s in enumerate(items, 1):
            s["prev"] = items[i - 2] if i > 1 else None
            s["next"] = items[i] if i < len(items) else None
            if s["path"] in EXPANDED:
                continue
            out_path = os.path.join(ROOT, s["path"], "index.md")
            with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(page(s, i, len(items)))
            written += 1

    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build_readme(plan, intro))

    bad = check_links()
    print("✓ 生成 %d 个 index.md + README.md（%d 个条目，跳过手写模块 %d 个）"
          % (written, len(plan), len(EXPANDED)))
    if bad:
        for path, target in bad:
            print("✗ 死链 %s → %s" % (path, target))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

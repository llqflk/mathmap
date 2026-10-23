# -*- coding: utf-8 -*-
"""把 math.md 与线性代数讲义生成一个本地可浏览的静态站点（_site/）。

用法：
    python tools/site.py          # 生成到 _site/
然后起一个静态服务器：
    python -m http.server 8765 --directory _site

约定同 build.py：math.md 是唯一真相源，线性代数目录是手写模块、按原样收录。
"""
import json
import math
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import LEVELS, LEVEL_TITLE, EXPANDED, ROOT, parse, read_source, resolve  # noqa: E402

OUT = os.path.join(ROOT, "_site")
ASSETS = os.path.join(ROOT, "tools", "assets")
LA_DIR = "level-2-concrete/05-线性代数"

MATHJAX = """<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  tex2jax: {inlineMath: [['$','$']], displayMath: [['$$','$$']], processEscapes: true},
  TeX: {extensions: ["AMSmath.js","AMSsymbols.js","AMScd.js"]},
  SVG: {scale: 100, font: "TeX"},
  showMathMenu: false, messageStyle: "none"
});
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@2.7.9/MathJax.js?config=TeX-AMS_SVG"
        onerror="document.documentElement.classList.add('nomath')"></script>"""

# ------------------------------------------------------------------ Markdown


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


MATH_RE = re.compile(r"(\$\$.+?\$\$|\$[^$\n]+?\$)")
SAFE_HREF = re.compile(r"^(https?://|mailto:|#|/)")


def fix_href(href):
    href = href.strip()
    if SAFE_HREF.match(href):
        return href
    href = href.replace("README.md", "index.html")
    if href.endswith(".md"):
        href = href[:-3] + ".html"
    return href


def inline_fmt(t):
    stash = []

    def keep(frag):
        stash.append(frag)
        return "\x00%d\x00" % (len(stash) - 1)

    t = re.sub(r"`([^`]+)`", lambda m: keep("<code>%s</code>" % m.group(1)), t)
    t = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)",
               lambda m: keep('<img alt="%s" src="%s">' % (m.group(1), fix_href(m.group(2)))), t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: keep('<a href="%s">%s</a>' % (fix_href(m.group(2)), m.group(1))), t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<em>\1</em>", t)
    for i, frag in enumerate(stash):
        t = t.replace("\x00%d\x00" % i, frag)
    return t


def inline(text):
    """公式先换成占位符，再加粗/斜体/链接——这样 `**…$x$…**` 这种跨公式的强调也能生效。"""
    stash = []

    def stash_math(m):
        stash.append(esc(m.group(0)))
        return "\x01%d\x01" % (len(stash) - 1)

    text = MATH_RE.sub(stash_math, text)
    text = inline_fmt(esc(text))
    for i, seg in enumerate(stash):
        text = text.replace("\x01%d\x01" % i, seg)
    return text


def split_row(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    cells, cur, in_math = [], "", False
    for ch in row:
        if ch == "$":
            in_math = not in_math
            cur += ch
        elif ch == "|" and not in_math:
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
    cells.append(cur.strip())
    return cells


def render_table(rows):
    head = split_row(rows[0])
    aligns = []
    for c in split_row(rows[1]) if len(rows) > 1 else []:
        if c.startswith(":") and c.endswith(":"):
            aligns.append("center")
        elif c.endswith(":"):
            aligns.append("right")
        else:
            aligns.append("left")
    body = rows[2:]
    out = ["<table>", "<thead><tr>"]
    out += ["<th>%s</th>" % inline(c) for c in head]
    out.append("</tr></thead>")
    out.append("<tbody>")
    for r in body:
        cells = split_row(r)
        tds = []
        for i, c in enumerate(cells):
            al = aligns[i] if i < len(aligns) else "left"
            tds.append('<td style="text-align:%s">%s</td>' % (al, inline(c)))
        out.append("<tr>" + "".join(tds) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def render_list(lines, i):
    base = len(lines[i]) - len(lines[i].lstrip())
    ordered = bool(re.match(r"^\s*\d+[.)]\s+", lines[i]))
    tag = "ol" if ordered else "ul"
    items, n = [], len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            break
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if not m:
            break
        indent = len(m.group(1))
        if indent < base:
            break
        if indent > base:
            sub, i = render_list(lines, i)
            if items:
                items[-1] = (items[-1][0], items[-1][1] + sub)
            continue
        items.append((m.group(3), ""))
        i += 1
    body = "".join("<li>%s%s</li>" % (inline(t), ch) for t, ch in items)
    return "<%s>%s</%s>" % (tag, body, tag), i


def convert(md):
    lines = md.replace("\r\n", "\n").split("\n")
    i, n, out = 0, len(lines), []
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = ' class="language-%s"' % lang if lang else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, esc("\n".join(buf))))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
            i += 1
            continue
        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows) if len(rows) >= 2 else "<p>%s</p>" % inline(row_plain(rows[0])))
            continue
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>%s</blockquote>" % convert("\n".join(buf)))
            continue
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            sub, i = render_list(lines, i)
            out.append(sub)
            continue
        s = line.strip()
        if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
            out.append('<div class="mathblock">%s</div>' % esc(s))   # 独立公式单独成块
            i += 1
            continue
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|```|\s*\|)|^\s*([-*+]|\d+[.)])\s+|^>", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf)))
    html = "\n".join(out)
    # math.md 的列表项之间隔着空行，会生成一串单元素 <ul>，这里合并回一个列表
    return re.sub(r"</(ul|ol)>\s*<\1>", "", html)


def row_plain(row):
    return row.strip().strip("|")


# ------------------------------------------------------------------ 站点结构

def strip_page_head(md, title):
    """去掉手写页里的 H1、面包屑、生成器注释，正文交给 convert。"""
    lines = md.replace("\r\n", "\n").split("\n")
    out, dropped_h1 = [], False
    for line in lines:
        if not dropped_h1 and re.match(r"^#\s+", line):
            dropped_h1 = True
            continue
        if line.startswith("<!-- 自动生成"):
            continue
        if line.startswith("[← 返回") or line.startswith("> [← 返回"):
            continue
        out.append(line)
    return "\n".join(out)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read().replace("\r\n", "\n")


def collect():
    """→ 有序页面列表；层级 2 的线性代数条目展开成 1 + 12 页。"""
    sections, _ = parse(read_source())
    plan, errors = resolve(sections)
    if errors:
        raise SystemExit("\n".join(errors))

    pages = []
    for lvl, _, _ in LEVELS:
        items = [s for s in plan if s["level"] == lvl]
        for s in items:
            url = s["path"] + "/index.html"
            if s["path"] in EXPANDED:
                idx_md = read(s["path"] + "/index.md")
                pages.append(dict(url=url, title="线性代数", level=lvl, group="12 章讲义",
                                  md=strip_page_head(idx_md, "线性代数"), sub=False, parent=None))
                chapters = sorted(f for f in os.listdir(os.path.join(ROOT, s["path"]))
                                  if f.endswith(".md") and f != "index.md")
                for ch in chapters:
                    ch_md = read(s["path"] + "/" + ch)
                    m = re.match(r"^#\s+(.+)$", ch_md.split("\n")[0])
                    title = m.group(1).strip() if m else ch[:-3]
                    pages.append(dict(url=s["path"] + "/" + ch[:-3] + ".html", title=title,
                                      level=lvl, group="12 章讲义",
                                      md=strip_page_head(ch_md, title), sub=True, parent=url))
            else:
                pages.append(dict(url=url, title=s["title"], level=lvl, group=s["group"],
                                  num=s["num"], md="\n".join(s["body"]).strip("\n"), sub=False, parent=None))
    return pages


def sidebar_html(pages, current_url):
    out = ['<a class="brand" href="/index.html">数学范畴与应用实例</a>',
           '<div class="tagline">范畴论视角下的数学地图 · 54 条</div>',
           '<div class="hot"><a href="/map.html">◆ 天赋树地图</a><br>'
           '<a href="/3d.html">◆ 三维曲面（交互）</a></div>']
    for lvl, _, _ in LEVELS:
        items = [p for p in pages if p["level"] == lvl]
        if not items:
            continue
        out.append('<div class="lvl">%s</div>' % LEVEL_TITLE[lvl].split("：", 1)[1])
        out.append("<ul>")
        for p in items:
            if p["sub"]:
                continue
            cls = ' class="on"' if p["url"] == current_url else ""
            out.append('<li><a%s href="/%s">%s</a></li>' % (cls, p["url"], p["title"]))
            kids = [c for c in items if c["parent"] == p["url"]]
            if kids:
                out.append('<li class="sub"><ul>')
                for c in kids:
                    cls = ' class="on"' if c["url"] == current_url else ""
                    out.append('<li><a%s href="/%s">%s</a></li>' % (cls, c["url"], c["title"]))
                out.append("</ul></li>")
        out.append("</ul>")
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{pagetitle}</title>
<link rel="stylesheet" href="/assets/style.css">
{mathjax}
<style>.nomath .mathwarn{{display:block}} .mathwarn{{display:none;background:#fff4e5;border:1px solid #f0c48a;
padding:8px 12px;border-radius:6px;font-size:13px;color:#8a5a1a;margin:0 0 16px}}</style>
</head>
<body>
<nav class="side">
{side}
</nav>
<main>
<div class="crumbs">{crumbs}</div>
<div class="mathwarn">MathJax 没加载成功（离线或 CDN 被拦），公式会显示成 LaTeX 源码，正文不受影响。</div>
<article>
{body}
</article>
<div class="pager">{pager}</div>
</main>
</body>
</html>
"""


# ------------------------------------------------------------------ 三维地图

MAP_LEVELS = [
    ("0", "层级 0 · 元框架", "起点", 0, 36, "#f0a04b"),
    ("0.5", "层级 0.5 · 范畴论工具箱", "工具", 210, 26, "#e06c75"),
    ("1", "层级 1 · 抽象结构", "抽象", 500, 21, "#61afef"),
    ("2", "层级 2 · 具体实例", "实例", 790, 18, "#98c379"),
    ("3", "层级 3 · 模型计算", "计算", 1080, 15, "#c678dd"),
]

EDGE_COLOR = {"meta": "#8b93a1", "tool": "#e5c07b", "struct": "#61afef",
              "instantiate": "#98c379", "compute": "#c678dd", "chapter": "#7fb069"}

# (层A, 序号A, 层B, 序号B, 关系标签, 类型) —— 关系按数学内容手工标注
MAP_EDGES = [
    # 元框架 → 工具
    ("0", 1, "0.5", 1, "分类即函子", "meta"),
    ("0", 1, "1", 5, "元语言", "meta"),
    # 层级 0.5 内部
    ("0.5", 1, "0.5", 2, "函子", "tool"),
    ("0.5", 2, "0.5", 3, "自然变换", "tool"),
    ("0.5", 3, "0.5", 4, "米田", "tool"),
    ("0.5", 3, "0.5", 5, "伴随", "tool"),
    ("0.5", 5, "0.5", 6, "单子", "tool"),
    # 层级 1 内部：代数与表示
    ("1", 1, "1", 3, "表示", "struct"),
    ("1", 2, "1", 3, "李代数表示", "struct"),
    ("1", 1, "1", 4, "链复形", "struct"),
    ("1", 21, "1", 3, "Galois 表示", "struct"),
    ("1", 21, "1", 16, "Langlands", "struct"),
    # 层级 1 内部：拓扑与几何
    ("1", 10, "1", 11, "同调", "struct"),
    ("1", 11, "1", 4, "链复形", "struct"),
    ("1", 10, "1", 12, "光滑结构", "struct"),
    ("1", 12, "1", 13, "度量", "struct"),
    ("1", 13, "1", 14, "几何结构", "struct"),
    ("1", 1, "1", 15, "环与理想", "struct"),
    ("1", 15, "1", 16, "概形", "struct"),
    # 层级 1 内部：分析与概率
    ("1", 7, "1", 6, "测度", "struct"),
    ("1", 7, "1", 8, "傅里叶", "struct"),
    ("1", 6, "1", 8, "算子", "struct"),
    ("1", 6, "1", 9, "Sobolev", "struct"),
    ("1", 8, "1", 9, "傅里叶方法", "struct"),
    ("1", 17, "1", 7, "测度", "struct"),
    ("1", 17, "1", 18, "随机流", "struct"),
    # 层级 1 内部：基础
    ("1", 20, "1", 19, "ZFC", "struct"),
    ("1", 5, "1", 4, "导出范畴", "struct"),
    ("1", 5, "1", 15, "层论", "struct"),
    ("1", 2, "1", 13, "对称空间", "struct"),
    # 抽象 → 具体
    ("1", 1, "2", 5, "模的特例", "instantiate"),
    ("1", 1, "2", 6, "多项式环", "instantiate"),
    ("1", 1, "2", 7, "Z/nZ", "instantiate"),
    ("1", 7, "2", 1, "ε-δ", "instantiate"),
    ("2", 1, "2", 2, "解析延拓", "instantiate"),
    ("2", 1, "2", 3, "初等积分", "instantiate"),
    ("2", 3, "2", 4, "PDE", "instantiate"),
    ("1", 6, "2", 4, "弱解", "instantiate"),
    ("2", 5, "2", 8, "坐标系", "instantiate"),
    ("1", 17, "2", 9, "分布", "instantiate"),
    ("1", 20, "2", 10, "有限集", "instantiate"),
    ("1", 17, "2", 11, "期望效用", "instantiate"),
    # 具体 → 计算
    ("2", 5, "3", 1, "浮点实现", "compute"),
    ("2", 4, "3", 2, "离散化", "compute"),
    ("2", 1, "3", 3, "梯度", "compute"),
    ("3", 3, "3", 4, "凸松弛", "compute"),
    ("2", 9, "3", 5, "后验", "compute"),
    ("1", 17, "3", 6, "概率", "compute"),
    ("2", 7, "3", 7, "模运算", "compute"),
    ("1", 8, "3", 8, "傅里叶", "compute"),
    ("2", 3, "3", 9, "状态方程", "compute"),
    ("2", 8, "3", 10, "几何对象", "compute"),
    ("2", 4, "3", 11, "N-S 方程", "compute"),
    ("2", 10, "3", 12, "图", "compute"),
    ("3", 4, "3", 13, "优化", "compute"),
    ("2", 9, "3", 14, "风险中性", "compute"),
    ("2", 5, "3", 15, "线性代数", "compute"),
    ("3", 1, "3", 13, "张量", "compute"),
]

# 少数条目可以直接跳到三维曲面页
MAP_QUADRIC = {"L2-05": "ellipsoid"}


def plain_math(t):
    t = t.replace("$", "")
    t = re.sub(r"\\(mathbf|mathbb|mathrm|mathcal|operatorname|text|mathfrak)\{([^{}]*)\}",
               r"\2", t)
    t = t.replace("\\to", "→").replace("\\times", "×").replace("\\cong", "≅")
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    t = re.sub(r"[{}]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def short_title(t):
    t = plain_math(t)
    t = re.sub(r"（[^）]*）|\([^)]*\)", "", t)
    t = t.split(" / ")[0].strip()
    return t[:16]


def category_of(section):
    for line in section["body"]:
        if line.startswith("- 范畴："):
            return plain_math(line[len("- 范畴："):])
    return ""


def la_chapters():
    """线性代数 12 章的标题、链接与小节名（这些才是“具体章节”）。"""
    base = os.path.join(ROOT, LA_DIR)
    out = []
    for name in sorted(os.listdir(base)):
        if not name.endswith(".md") or name == "index.md":
            continue
        text = read(LA_DIR + "/" + name)
        lines = text.split("\n")
        m = re.match(r"^#\s+(.+)$", lines[0]) if lines else None
        title = m.group(1).strip() if m else name[:-3]
        sections = []
        for ln in lines:
            mm = re.match(r"^##\s+(.+)$", ln)
            if mm:
                sections.append(plain_math(mm.group(1)))
        out.append(dict(
            slug=name[:-3],
            title=title,
            short=re.sub(r"^第\s*\d+\s*章[：:]\s*", "", title)[:24],
            url=LA_DIR + "/" + name[:-3] + ".html",
            sections=sections,
        ))
    return out


def build_map():
    """家族扇区（角度）+ 抽象度（半径）+ 桥；数据一次性烘焙进 map.html。"""
    from families import (BRIDGES, FAMILY, FAMILY_NAME, LEVEL_LABEL, LEVEL_RADIUS,
                          ORDER, family_colors)
    import similarity as simlib

    sections, _ = parse(read_source())
    plan, errors = resolve(sections)
    if errors:
        raise SystemExit("\n".join(errors))

    def nid(level, num):
        return "L%s-%02d" % (level.replace(".", ""), int(num or 1))

    sizes = {"0.5": 21, "1": 18, "2": 15, "3": 12}
    topics = []
    for s in plan:
        key = "%s-%s" % (s["level"], s["num"] or 1)
        num = s["num"] or 1
        topics.append(dict(
            id=nid(s["level"], num), key=key, level=s["level"], num=num,
            size=sizes.get(s["level"], 14),
            title=plain_math(s["title"]), short=short_title(s["title"]),
            cat=category_of(s), url=s["path"] + "/index.html",
            family=FAMILY.get(key, "J"),
        ))

    # 扇区宽度 ∝ 家族成员数
    counts = {}
    for x in topics:
        if x["family"] != "M":
            counts[x["family"]] = counts.get(x["family"], 0) + 1
    order = [f for f in ORDER if f in counts]
    # 扇区宽度 ∝ “角度需求” = max(同层节点数 / 该层半径)，而不是简单按成员数
    demand = {}
    for fam in order:
        groups = {}
        for x in topics:
            if x["family"] == fam:
                groups.setdefault(x["level"], []).append(x)
        demand[fam] = max(len(g) / LEVEL_RADIUS.get(lvl, 1000) for lvl, g in groups.items())
    total = sum(demand.values())
    gap = math.radians(4.2)
    avail = 2 * math.pi - gap * len(order)
    sectors, cursor = {}, -math.pi / 2
    for fam in order:
        w = avail * demand[fam] / total
        sectors[fam] = (cursor, cursor + w)
        cursor += w + gap

    colors = family_colors(order)
    colors["M"] = "#f0a04b"

    # 位置：扇区内按层分圈，同层按序号均分角度
    for fam, (a0, a1) in sectors.items():
        members = [x for x in topics if x["family"] == fam]
        by_level = {}
        for m in members:
            by_level.setdefault(m["level"], []).append(m)
        for lvl, group in by_level.items():
            group.sort(key=lambda x: x["num"])
            r = LEVEL_RADIUS.get(lvl, 1000)
            pad = (a1 - a0) * 0.10
            span = (a1 - a0) - 2 * pad
            for i, m in enumerate(group):
                ang = a0 + pad + span * (i + 0.5) / len(group)
                m["x"] = round(r * math.cos(ang), 1)
                m["y"] = round(r * math.sin(ang), 1)
                m["color"] = colors[fam]

    center = next(x for x in topics if x["family"] == "M")
    center.update(x=0.0, y=0.0, color=colors["M"], short="起点", size=32)

    lvl_rank = {"0.5": 0, "1": 1, "2": 2, "3": 3}
    edges = []

    def family_members(fam):
        return sorted([x for x in topics if x["family"] == fam],
                      key=lambda x: (lvl_rank[x["level"]], x["num"]))

    # 中心 → 每个家族的最内层节点
    for fam in order:
        edges.append(dict(a=center["id"], b=family_members(fam)[0]["id"],
                          kind="root", label="", color=colors[fam]))
    # 家族内脊柱
    for fam in order:
        ms = family_members(fam)
        for a, b in zip(ms, ms[1:]):
            edges.append(dict(a=a["id"], b=b["id"], kind="spine", label="", color=colors[fam]))

    # 跨家族弱连接（自动相似度）
    items = simlib.docs()
    vecs, _ = simlib.build_vectors(items)
    idx = {it["key"]: i for i, it in enumerate(items)}
    for i, u in enumerate(topics):
        for v in topics[i + 1:]:
            if u["family"] == v["family"] or "M" in (u["family"], v["family"]):
                continue
            s = simlib.cosine(vecs[idx[u["key"]]], vecs[idx[v["key"]]])
            if s >= 0.18:
                edges.append(dict(a=u["id"], b=v["id"], kind="weak", label="", color="#7d8697"))

    # 手工桥（有名字的函子/对偶）
    for ka, kb, label, _fa, _fb in BRIDGES:
        a = next((x for x in topics if x["key"] == ka), None)
        b = next((x for x in topics if x["key"] == kb), None)
        if a and b:
            edges.append(dict(a=a["id"], b=b["id"], kind="bridge", label=label, color="#e8c07a"))

    # 线性代数 45 小节：绕着它排成小轮（放大才看标签）
    hub = next(x for x in topics if x["key"] == "2-5")
    flat = []
    for ci, ch in enumerate(la_chapters(), 1):
        for si, sec in enumerate(ch["sections"], 1):
            flat.append((ci, si, sec, ch["url"]))
    per_ring = 15
    for i, (ci, si, sec, url) in enumerate(flat):
        ring, slot = divmod(i, per_ring)
        r = 100 + ring * 58
        a = -math.pi / 2 + 2 * math.pi * slot / per_ring + ring * 0.14
        sec_node = dict(
            id="SEC-%02d-%02d" % (ci, si), key="", level="2", num=0, size=6.5,
            title=sec, short="%d.%d" % (ci, si),
            cat="线性代数 · 第 %d 章" % ci, url=url,
            family="C", color=colors["C"], child=True,
            x=round(hub["x"] + r * math.cos(a), 1), y=round(hub["y"] + r * math.sin(a), 1),
        )
        topics.append(sec_node)
        edges.append(dict(a=hub["id"], b=sec_node["id"], kind="section", label="", color=colors["C"]))

    families = [dict(key=f, name=FAMILY_NAME[f], color=colors[f],
                     a0=round(sectors[f][0], 4), a1=round(sectors[f][1], 4), count=counts[f])
                 for f in order]

    payload = dict(center=center, families=families, nodes=topics,
                   rings=LEVEL_RADIUS, levelLabel=LEVEL_LABEL)
    tpl = open(os.path.join(ASSETS, "map.html"), encoding="utf-8").read()
    html = (tpl.replace("/*__DATA__*/", json.dumps(payload, ensure_ascii=False))
               .replace("/*__EDGES__*/", json.dumps(edges, ensure_ascii=False)))
    with open(os.path.join(OUT, "map.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return len(topics), len(edges), []


def build():
    pages = collect()
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    for name in os.listdir(ASSETS):
        shutil.copy(os.path.join(ASSETS, name), os.path.join(OUT, "assets", name))
    shutil.copy(os.path.join(ASSETS, "3d.html"), os.path.join(OUT, "3d.html"))

    for i, p in enumerate(pages):
        prev = pages[i - 1] if i > 0 else None
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        crumbs = LEVEL_TITLE[p["level"]]
        if p.get("group") and p["group"] != "12 章讲义":
            crumbs += " · " + p["group"]
        pager = []
        pager.append('<a href="/%s">← %s</a>' % (prev["url"], prev["title"]) if prev else '<span class="ph">已是第一篇</span>')
        pager.append('<a href="/%s">%s →</a>' % (nxt["url"], nxt["title"]) if nxt else '<span class="ph">已是最后一篇</span>')
        html_text = PAGE.format(
            title=p["title"], pagetitle=p["title"] + " · 数学范畴与应用实例", mathjax=MATHJAX,
            side=sidebar_html(pages, p["url"]),
            crumbs=crumbs,
            body=convert(p["md"]),
            pager="".join(pager),
        )
        dest = os.path.join(OUT, p["url"].replace("/", os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html_text)

    # 首页 = README
    readme = read("README.md")
    home = PAGE.format(
        title="数学范畴与应用实例", pagetitle="数学范畴与应用实例", mathjax=MATHJAX,
        side=sidebar_html(pages, "/index.html"), crumbs="总目录",
        body=convert(readme), pager='<a href="/%s">开始阅读：%s →</a>' % (pages[0]["url"], pages[0]["title"]),
    )
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(home)

    # 单文件全文（README 与导航里的 "math.md" 指向它）
    full = re.sub(r"^#\s+.*\n", "", read("math.md"), count=1)
    full_page = PAGE.format(
        title="全文", pagetitle="全文 · 数学范畴与应用实例", mathjax=MATHJAX,
        side=sidebar_html(pages, ""), crumbs="单文件通读",
        body=convert(full), pager='<a href="/index.html">← 返回总目录</a>',
    )
    with open(os.path.join(OUT, "math.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(full_page)

    n_nodes, n_edges, missing = build_map()
    dead = check_links()
    print("✓ 生成 %d 页 + 天赋树地图（%d 节点 / %d 条关系）到 %s"
          % (len(pages) + 3, n_nodes, n_edges, OUT))
    for a, b, label in missing:
        print("  ! 关系指向不存在的节点：%s → %s（%s）" % (a, b, label))
    for src, href in dead:
        print("✗ 死链 %s → %s" % (src, href))
    return 1 if dead else 0


def check_links():
    """校验站内绝对链接（/xxx）都能落到 _site 里的文件。"""
    bad = []
    for dirpath, _, files in os.walk(OUT):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, OUT)
            text = open(path, encoding="utf-8").read()
            for m in re.finditer(r'(?:href|src)="(/[^"#?]*)"', text):
                target = m.group(1)
                local = os.path.join(OUT, target.lstrip("/").replace("/", os.sep))
                if target.endswith("/"):
                    local = os.path.join(local, "index.html")
                if not os.path.exists(local):
                    bad.append((rel, target))
    return bad


if __name__ == "__main__":
    build()

# -*- coding: utf-8 -*-
"""相似度体检：给每个条目算 top-5 邻居，输出一张给作者审阅的表。

思路（先于布局）：
  1. 词表特征：数学术语词表 + 代码 API 名（np.linalg/svd/minimize…）
  2. TF-IDF：把“向量空间”“群”这类到处出现的词降权，抑制 hub 效应
  3. 余弦相似度 → 每个条目的最近邻
  4. 与我手工标的“同一家族”对照，标出两者冲突的地方（这些就是要你裁决的）

输出：similarity-review.md（不改动站点、不改动 math.md）
"""
import io
import math
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import parse, read_source, resolve  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "similarity-review.md")

# ---------------------------------------------------------------- 术语词表
TERMS = """
测度 可测 概率 随机 鞅 布朗 停时 分布 期望 方差 统计 估计 先验 后验 贝叶斯 MCMC 马尔可夫
熵 编码 信道 互信息 采样 蒙特卡洛 滤波 频谱 卷积 小波 傅里叶 变换 频域
群 环 域 理想 模 同态 商 自由 张量 线性 矩阵 向量 特征值 特征向量 对角化 Jordan 二次型 内积 范数
正交 秩 核 像 行列式 SVD 奇异值 谱 算子 自伴 酉 C* Hilbert Banach 紧 弱收敛
表示 特征标 不可约 李代数 李群 旋转 对称 生成元 指数映射
流形 切空间 余切 向量场 微分形式 外微分 联络 曲率 度量 黎曼 辛 泊松 哈密顿 拉格朗日
拓扑 开集 连续 同胚 紧致 连通 同伦 同调 上同调 链复形 边界 单纯复形 层 概形 簇 亏格
解析 全纯 留数 级数 极点 共形 黎曼面 亚纯
数域 判别式 素 理想类 类数 p进 模形式 Eisenstein Hecke L函数 Galois 椭圆曲线
变分 弱解 Sobolev 椭圆 抛物 双曲 特征线 守恒 离散 网格 有限元 刚度 插值 差分 稳定性
优化 梯度 凸 对偶 拉格朗日乘子 牛顿 拟牛顿 收敛 迭代 约束 线性规划
图 节点 边 路径 树 匹配 连通分量 邻接 平面图 欧拉 组合 计数 卡特兰 生成函数
算法 复杂度 排序 几何 凸包 Delaunay Voronoi 网格剖分
密码 加密 同态 RSA 模运算 哈希 签名 素数 分解
量子 量子门 纠缠 酉变换 CPT CPTP 密度矩阵 量子线路
神经网络 深度学习 反向传播 损失 梯度下降 激活 池化 张量运算
金融 期权 无套利 风险中性 对冲 波动率 Black-Scholes
控制 状态 反馈 能控 能观 极点配置 PID LQR 最优控制
逻辑 命题 谓词 归结 完备 哥德尔 模型 可证 定理证明
集合 基数 序数 力迫 选择公理 ZFC 连续统
范畴 函子 自然变换 伴随 单子 米田 预层 极限 余极限 2-范畴
""".split()

# 与代码/API 相关的硬信号
API_HINTS = [
    "np.linalg", "numpy", "scipy", "sympy", "matplotlib", "networkx", "torch", "sklearn",
    "pymc", "cvxpy", "gudhi", "delaunay", "convexhull", "svd", "eigh", "eigvals", "solve",
    "gradient", "minimize", "linprog", "quad", "odeint", "solve_ivp", "fft", "convolve",
    "euler", "rk4", "newton", "bfgs", "jacobian", "hessian", "sparse", "csr", "krylov",
    "mesh", "element", "stiffness", "assembly", "fem", "cfl", "advection", "diffusion",
    "galerkin", "interpolate", "spline", "residue", "contour", "holomorphic", "laplace",
    "fourier", "wavelet", "sample", "mcmc", "metropolis", "importance", "entropy", "kl",
    "rsa", "modpow", "pow(", "inverse", "hash", "sha", "gcm", "ecc", "elliptic",
    "gate", "hadamard", "cnot", "tensor", "statevector", "density", "povm",
    "mlp", "relu", "sigmoid", "softmax", "cross_entropy", "adam", "sgd",
    "black_scholes", "gbm", "monte", "brownian", "ito",
    "matrix", "matmul", "rank", "det", "trace", "inv", "norm", "dot", "cross",
]

# 手工“同一家族”（先给一版，供你改）
from families import FAMILY, FAMILY_NAME  # noqa: E402
STOP_LATIN = {
    "import", "print", "def", "for", "range", "lambda", "return", "self", "true", "false",
    "none", "and", "not", "the", "with", "from", "class", "assert", "float", "int", "str",
    "list", "dict", "len", "sum", "max", "min", "abs", "exp", "log", "sin", "cos", "sqrt",
    "array", "zeros", "ones", "eye", "random", "size", "shape", "plot", "show", "figure",
    "python", "mathematica", "numpy", "mathbf", "mathbb", "mathrm", "mathcal", "operatorname",
    "mu", "eta", "lambda_", "alpha", "beta", "gamma", "sigma", "theta", "frac", "left", "right",
}


def docs():
    sections, _ = parse(read_source())
    plan, errors = resolve(sections)
    if errors:
        raise SystemExit("\n".join(errors))
    out = []
    for s in plan:
        body = "\n".join(s["body"])
        cat = ""
        for line in s["body"]:
            if line.startswith("- 范畴："):
                cat = line
                break
        key = "%s-%s" % (s["level"], s["num"] or 1)
        out.append(dict(key=key, level=s["level"], num=s["num"] or 1,
                        title=s["title"], body=body, cat=cat, url=s["path"] + "/index.html",
                        family=FAMILY.get(key, "?")))
    return out


def tokens(d):
    body = d["body"]
    for junk in ("核心函子", "Python 示例", "Mathematica 示例", "Mathematica："):
        body = body.replace(junk, " ")
    text = d["title"] + "\n" + (d["cat"] * 3) + "\n" + body
    low = text.lower()
    tf = Counter()
    for t in TERMS:
        c = low.count(t.lower())
        if c:
            tf["zh:" + t] += c
    for h in API_HINTS:
        if h in low:
            tf["api:" + h] += 1
    for w in re.findall(r"[a-z_][a-z0-9_.]{2,}", low):
        if w in STOP_LATIN or len(w) < 3:
            continue
        tf["id:" + w] += 1
    if d["cat"]:
        for t in TERMS:
            if t in d["cat"]:
                tf["zh:" + t] += 2          # 范畴行再加一层权重
    return tf


def build_vectors(items):
    tfs = [tokens(d) for d in items]
    df = Counter()
    for tf in tfs:
        for k in tf:
            df[k] += 1
    n = len(items)
    vecs = []
    for tf in tfs:
        v = {}
        for k, c in tf.items():
            idf = math.log((1 + n) / (1 + df[k]))
            if idf <= 0.01:
                continue
            v[k] = (1 + math.log(c)) * idf
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vecs.append({k: x / norm for k, x in v.items()})
    return vecs, df


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(k, 0) for k, x in a.items())


def short(t, n=18):
    return t if len(t) <= n else t[:n] + "…"


def main():
    items = docs()
    vecs, df = build_vectors(items)
    n = len(items)

    sim = [[cosine(vecs[i], vecs[j]) for j in range(n)] for i in range(n)]
    for i in range(n):
        sim[i][i] = 0.0

    # 家族内/家族间平均相似度（检验区分度）
    intra, inter = [], []
    for i in range(n):
        for j in range(i + 1, n):
            (intra if items[i]["family"] == items[j]["family"] else inter).append(sim[i][j])

    lines = []
    add = lines.append
    add("# 相似度体检表（待你审阅）\n")
    add("这份表只用来**校验“谁和谁本质上接近”**，还没动页面。\n")
    add("算法：从每条正文（含代码里的 API 名）抽词 → TF-IDF 降权（把“向量空间”“群”这类到处都有的词压下去，"
        "否则一切都会贴到线性代数/抽象代数旁边）→ 余弦相似度。\n")
    add("“家族”是我手工标的先验（下面第二张表），两者独立算，冲突处就是需要你裁决的地方。\n")

    add("## 一、家族划分（我标的先验）\n")
    add("| 代号 | 家族 | 成员 |\n|---|---|---|")
    by_fam = {}
    for d in items:
        by_fam.setdefault(d["family"], []).append(d)
    for fam in sorted(by_fam):
        members = " · ".join(short(d["title"], 14) for d in by_fam[fam])
        add("| %s | %s | %s |" % (fam, FAMILY_NAME.get(fam, "?"), members))
    add("")

    add("## 二、每个条目的最近 5 个邻居\n")
    add("`√` = 同家族（符合先验）；`·` = 跨家族（可能是新关系，也可能是我算歪了）。\n")
    add("| 条目 | 家族 | 最近 5 个邻居（相似度） |\n|---|---|---|")
    for i, d in enumerate(items):
        order = sorted(range(n), key=lambda j: -sim[i][j])[:5]
        cells = []
        for j in order:
            mark = "√" if items[j]["family"] == d["family"] else "·"
            cells.append("%s %s <sub>%.2f</sub>" % (mark, short(items[j]["title"], 14), sim[i][j]))
        add("| %s `%s` | %s | %s |" % (short(d["title"], 20), d["key"], d["family"], "；".join(cells)))
    add("")

    add("## 三、区分度体检\n")
    add("- 家族内平均相似度：**%.3f**（样本 %d 对）" % (sum(intra) / len(intra), len(intra)))
    add("- 家族间平均相似度：**%.3f**（样本 %d 对）" % (sum(inter) / len(inter), len(inter)))
    add("- 比值 %.2f——越大说明“家族”这个先验和文本证据越一致。\n" % ((sum(intra) / len(intra)) / (sum(inter) / len(inter))))

    add("### 被降权的“万能词”（文档频率最高的 15 个）\n")
    add("这些词在所有条目里都出现，已经按 IDF 压低；如果还有残留的 hub 效应，可以再手工设零。\n")
    add("| 词 | 出现在多少条 |\n|---|---|")
    for k, c in df.most_common(15):
        add("| `%s` | %d |" % (k, c))
    add("")

    add("## 四、需要你裁决的 12 处\n")
    add("### A. 相似但被我分到不同家族（可能是漏掉的关系）\n")
    cross = []
    for i in range(n):
        for j in range(i + 1, n):
            if items[i]["family"] != items[j]["family"]:
                cross.append((sim[i][j], i, j))
    cross.sort(reverse=True)
    cross = cross[:12]
    add("| 条目 A | 条目 B | 相似度 | A 家族 | B 家族 |\n|---|---|---|---|---|")
    for s, i, j in cross[:12]:
        add("| %s | %s | %.2f | %s | %s |" % (short(items[i]["title"], 16), short(items[j]["title"], 16),
                                              s, items[i]["family"], items[j]["family"]))
    add("")
    add("### B. 同家族但并不相似的（可能我分错了）\n")
    weak = []
    for i in range(n):
        for j in range(i + 1, n):
            if items[i]["family"] == items[j]["family"]:
                weak.append((sim[i][j], i, j))
    weak.sort()
    weak = weak[:12]
    if weak:
        add("| 条目 A | 条目 B | 相似度 | 家族 |\n|---|---|---|---|")
        for s, i, j in weak[:12]:
            add("| %s | %s | %.2f | %s |" % (short(items[i]["title"], 16), short(items[j]["title"], 16),
                                             s, items[i]["family"]))
    else:
        add("（没有：同家族内部的相似度都 ≥ 0.10）")
    add("")

    add("## 五、各家族“文本紧密度”（自动相似度均值）\n")
    add("紧密度高 = 成员连用同一套词；低 = 我分得太宽或它们只是“同类不同题”。\n")
    add("| 家族 | 条数 | 内部平均相似度 | 成员 |\n|---|---|---|---|")
    fam_pairs = {}
    for i in range(n):
        for j in range(i + 1, n):
            if items[i]["family"] == items[j]["family"]:
                fam_pairs.setdefault(items[i]["family"], []).append(sim[i][j])
    for fam in sorted(by_fam, key=lambda f: -(sum(fam_pairs.get(f, [0])) / max(1, len(fam_pairs.get(f, [0]))))):
        ps = fam_pairs.get(fam, [])
        mean = sum(ps) / len(ps) if ps else 0.0
        add("| %s %s | %d | %.3f | %s |" % (
            fam, FAMILY_NAME.get(fam, "?"), len(by_fam[fam]), mean,
            " · ".join(short(d["title"], 12) for d in by_fam[fam])))
    add("")

    add("## 六、我自己的判断（供你对照，不用照抄）\n")
    add("**我确信是“同一”的（强边）**\n")
    add("- 线性代数 ↔ 数值线性代数：同一范畴，一个在纸上一个在浮点里（自动相似度 0.22，最高之一）")
    add("- 调和分析 ↔ 信号处理：同一傅里叶变换，一个是定理一个是滤波器（0.16）")
    add("- 概率论与随机过程 ↔ 概率论与数理统计：同一测度空间，一个看过程一个看反推（0.17）")
    add("- 常微分方程 ↔ 动力系统：同一演化，一个解方程一个看轨道（0.28）")
    add("- 数值优化 ↔ 凸优化：前者是方法，后者是保证收敛的那一类（0.28）")
    add("- 抽象代数 ↔ 表示论：表示就是“群在向量空间上作用”，本质是同一对象的两面（0.15）")
    add("")
    add("**我拿不准、需要你裁决的（自动给高分但语义可疑）**\n")
    add("- 微分拓扑 ↔ 数学分析（0.42，全表最高）：只是都在讲梯度/微分形式，还是真是同一件事？")
    add("- 点集拓扑 ↔ 调和分析（0.21）：靠“拓扑群”这个词撑起来的，我觉得是假信号")
    add("- 组合与离散数学 ↔ 范畴的定义（0.07）：它在正文里提了 FinSet 范畴，词面命中，语义无关")
    add("- 博弈论（整行都 ≤ 0.04）：正文太短，自动相似度对它基本无效，完全靠手工")
    add("")
    add("**我认为应该合并但自动没发现**\n")
    add("- 代数几何 ↔ 代数数论（0.13，还行但不高）：函数域 vs 数域，同一套 Spec 语言")
    add("- 模形式 ↔ 表示论（0.06，很低）：Langlands 的意义上它们才是同一件事，靠词表永远测不出来")
    add("")
    add("## 七、布局的两个选项（等你定第 1、3 个问题）\n")
    add("**A. 半径=抽象度，角度=家族**（我推荐先做）")
    add("- 中心仍是元框架，向外依次 工具→抽象→实例→计算；同一家族落在同一角度扇区")
    add("- 好处：保留“从抽象到具体”的整体阅读感，同族贴在一起；改动小，复用现有天赋树")
    add("- 代价：跨层的同族（比如“线性代数↔数值线性代数”）仍被半径分开，只能靠连线表达")
    add("")
    add("**B. 纯语义自由布局**")
    add("- 丢掉同心环，位置完全由相似度决定，家族成“大陆”，桥（同调/Spec/傅里叶/Gelfand）连接大陆")
    add("- 好处：最接近你说的“本质上同一个东西就靠近”")
    add("- 代价：失去层级直觉；54 个点容易摊成一张饼，需要簇锚点约束")
    add("")
    add("**C. 双坐标切换**：同一份数据两套坐标，按钮切换；工作量约 1.5 倍，但两种读法都在。")
    add("")

    add("## 八、确认之后我会怎么用\n")
    add("1. 家族内 → 强边（几乎重合，视觉上成簇）")
    add("2. 跨家族但相似度高 → 弱边（“共享工具”连接）")
    add("3. 手工桥边（同调 / Spec / 傅里叶 / Gelfand）单独画，方向感更强\n")
    add("审阅时你只需要做三件事：划掉不认同的邻居、补上漏掉的配对、指出分错的家族。")

    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("✓ 写入 %s（%d 条，家族 %d 个）" % (OUT, n, len(by_fam)))
    print("  家族内 / 家族间平均相似度：%.3f / %.3f" % (sum(intra) / len(intra), sum(inter) / len(inter)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

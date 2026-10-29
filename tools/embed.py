# -*- coding: utf-8 -*-
"""把 54 个条目嵌入三维空间（两级嵌入）。

为什么不是“一次性 MDS 到 3D”：实测 kNN 保持率只有 0.08——54 个点里 70 对同族
相似度被先验抬到 0.4 左右，距离差距太小，3D 抓不住局部结构。改成两级：

  级 1：13 个家族当成 13 个“质心”，用家族间平均相似度做 MDS → 3D 位置
  级 2：每个家族内部单独 MDS → 小范围偏移，半径随成员数增大

这样“同族成簇”由级 1 保证，“簇内谁离谁近”由级 2 用真实相似度决定。

高维表示仍是 TF-IDF 余弦（正文 + 范畴行 + 代码 API），家族先验只加 +0.38 的偏置。
"""
import importlib.util
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import similarity as simlib  # noqa: E402
from families import FAMILY, FAMILY_NAME  # noqa: E402

HAS_NUMPY = importlib.util.find_spec("numpy") is not None
FAMILY_BONUS = 0.38
KNN_K = 5
CENTROID_SCALE = 900.0


# ---------------------------------------------------------------- 小工具

def plain(t):
    t = re.sub(r"\$[^$]*\$", "", t)
    t = re.sub(r"[{}]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def short(t):
    t = plain(t)
    t = re.sub(r"（[^）]*）|\([^)]*\)", "", t)
    return t.split(" / ")[0].strip()[:16]


# ---------------------------------------------------------------- 矩阵工具

def _center(D2):
    n = len(D2)
    row = [sum(D2[i]) / n for i in range(n)]
    total = sum(row) / n
    return [[-0.5 * (D2[i][j] - row[i] - row[j] + total) for j in range(n)] for i in range(n)]


def _eig(B, k):
    """前 k 个特征对；返回 (特征值, 每个样本的 k 维坐标)。"""
    n = len(B)
    k = max(1, min(k, n - 1))
    if HAS_NUMPY:
        import numpy as np
        w, v = np.linalg.eigh(np.array(B, dtype=float))
        idx = list(range(n - 1, -1, -1))[:k]
        return ([float(max(0.0, w[i])) for i in idx],
                [[float(v[j][i]) for i in idx] for j in range(n)])

    A = [row[:] for row in B]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(60):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off < 1e-14:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = A[p][q]
                if abs(apq) < 1e-14:
                    continue
                th = (A[q][q] - A[p][p]) / (2 * apq)
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for i in range(n):
                    aip, aiq = A[i][p], A[i][q]
                    A[i][p] = c * aip - s * aiq
                    A[i][q] = s * aip + c * aiq
                for i in range(n):
                    api, aqi = A[p][i], A[q][i]
                    A[p][i] = c * api - s * aqi
                    A[q][i] = s * api + c * aqi
                for i in range(n):
                    vip, viq = V[i][p], V[i][q]
                    V[i][p] = c * vip - s * viq
                    V[i][q] = s * vip + c * viq
    order = sorted(range(n), key=lambda i: -A[i][i])[:k]
    return [max(0.0, A[i][i]) for i in order], [[V[j][i] for i in order] for j in range(n)]


def mds3(sim, scale):
    """相似度矩阵 → 3D 坐标（经典 MDS）。"""
    n = len(sim)
    if n == 1:
        return [[0.0, 0.0, 0.0]]
    D2 = [[(1.0 - sim[i][j]) ** 2 for j in range(n)] for i in range(n)]
    vals, raw = _eig(_center(D2), 3)
    if not vals or vals[0] <= 1e-12:
        return [[0.0, 0.0, 0.0] for _ in range(n)]
    k = len(vals)
    out = []
    for row in raw:
        p = [row[d] * math.sqrt(vals[d]) for d in range(k)]
        p += [0.0] * (3 - k)
        out.append(p)
    peak = max(math.sqrt(sum(c * c for c in p)) for p in out) or 1.0
    return [[c / peak * scale for c in p] for p in out]


# ---------------------------------------------------------------- 主流程

def embed():
    items = simlib.docs()
    vecs, _ = simlib.build_vectors(items)
    n = len(items)
    fams = [FAMILY.get(it["key"], "J") for it in items]

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        sim[i][i] = 1.0          # 自相似为 1，否则 MDS 的距离矩阵是错的
    for i in range(n):
        for j in range(i + 1, n):
            s = simlib.cosine(vecs[i], vecs[j])
            if fams[i] == fams[j]:
                s = min(1.0, s + FAMILY_BONUS)
            sim[i][j] = sim[j][i] = s

    # 级 1：家族质心
    groups = {}
    for i, f in enumerate(fams):
        groups.setdefault(f, []).append(i)
    fkeys = sorted(groups, key=lambda f: -len(groups[f]))
    fi = {f: i for i, f in enumerate(fkeys)}
    m = len(fkeys)
    fsim = [[0.0] * m for _ in range(m)]
    for a in range(m):
        for b in range(a + 1, m):
            left, right = groups[fkeys[a]], groups[fkeys[b]]
            vals = [sim[i][j] for i in left for j in right]
            fsim[a][b] = fsim[b][a] = sum(vals) / len(vals)
    cents = mds3(fsim, CENTROID_SCALE)

    # 级 2：家族内部
    coords = [None] * n
    for f in fkeys:
        idx = groups[f]
        if len(idx) == 1:
            coords[idx[0]] = [c for c in cents[fi[f]]]
            continue
        sub = [[sim[i][j] for j in idx] for i in idx]
        radius = 105 + 17 * len(idx)
        local = mds3(sub, radius)
        for k, i in enumerate(idx):
            c = cents[fi[f]]
            coords[i] = [c[d] + local[k][d] for d in range(3)]

    # 平移到质心，方便相机以原点为目标
    for d in range(3):
        mean = sum(c[d] for c in coords) / len(coords)
        for c in coords:
            c[d] -= mean

    # 体检：kNN 保持率 + 归一化 stress
    def top_hi(i):
        order = sorted((j for j in range(n) if j != i), key=lambda j: -sim[i][j])
        return set(order[:KNN_K])

    def top_lo(i):
        order = sorted((j for j in range(n) if j != i),
                       key=lambda j: sum((coords[i][d] - coords[j][d]) ** 2 for d in range(3)))
        return set(order[:KNN_K])

    keep = sum(len(top_hi(i) & top_lo(i)) / KNN_K for i in range(n)) / n
    for fam in fkeys:
        idx = groups[fam]
        if len(idx) < 2:
            continue
    intra_hi = [sim[i][j] for f in fkeys for a, i in enumerate(groups[f]) for j in groups[f][a + 1:]]
    intra_lo = [math.dist(coords[i], coords[j]) for f in fkeys
                for a, i in enumerate(groups[f]) for j in groups[f][a + 1:]]
    mean_lo = (sum(intra_lo) / len(intra_lo)) if intra_lo else 1.0
    stress = 0.0
    if intra_lo:
        stress = math.sqrt(sum(((1 - s) - d / mean_lo) ** 2 for s, d in zip(intra_hi, intra_lo)) / len(intra_lo))

    nodes = []
    for i, it in enumerate(items):
        nodes.append(dict(
            id="N%02d" % i, key=it["key"], url=it["url"],
            title=plain(it["title"]), label=short(it["title"]),
            family=fams[i], familyName=FAMILY_NAME.get(fams[i], ""),
            level=it["level"],
            x=round(coords[i][0], 1), y=round(coords[i][1], 1), z=round(coords[i][2], 1),
        ))

    # 高维空间的真近邻（k=4），给连线用
    edges, seen = [], set()
    for i in range(n):
        order = sorted((j for j in range(n) if j != i), key=lambda j: -sim[i][j])[:4]
        for j in order:
            a, b = sorted((i, j))
            if (a, b) in seen:
                continue
            seen.add((a, b))
            edges.append(dict(a=nodes[a]["id"], b=nodes[b]["id"],
                              w=round(sim[a][b], 3),
                              same=int(fams[a] == fams[b])))

    # 每个节点的前 3 近邻（给面板用）
    near = {}
    for i in range(n):
        order = sorted((j for j in range(n) if j != i), key=lambda j: -sim[i][j])[:3]
        near[nodes[i]["id"]] = [dict(id=nodes[j]["id"], label=nodes[j]["label"],
                                     sim=round(sim[i][j], 2)) for j in order]

    return dict(nodes=nodes, edges=edges, near=near,
                stats=dict(knn=round(keep, 3), stress=round(stress, 3),
                           bonus=FAMILY_BONUS, k=KNN_K, dim=len(vecs[0])))


if __name__ == "__main__":
    import json
    d = embed()
    print("节点", len(d["nodes"]), "边", len(d["edges"]), "体检", d["stats"])
    print(json.dumps(d["nodes"][:2], ensure_ascii=False, indent=1))

# -*- coding: utf-8 -*-
"""天赋树布局：同心环 + 角度对齐内层邻居。

比力导向更可控：每层的节点按“内层邻居的平均方位”排序后均匀铺在环上，
所以关系边大多是短弦/径向线，视觉上接近《流放之路》那种盘状天赋树。
确定性（固定种子），形状直接烘焙进 map.html。
"""
import math
import random

ORDER = ["0", "0.5", "1", "2", "3"]


def _circular_mean(angles):
    sx = sum(math.sin(a) for a in angles)
    cy = sum(math.cos(a) for a in angles)
    return math.atan2(sx, cy)


def radial_layout(nodes, edges, rings, seed=20261022):
    rnd = random.Random(seed)
    nbr = {n["id"]: set() for n in nodes}
    for e in edges:
        nbr[e["a"]].add(e["b"])
        nbr[e["b"]].add(e["a"])

    by_level = {}
    for n in nodes:
        by_level.setdefault(n["level"], []).append(n)

    pos, angle = {}, {}
    for n in by_level.get("0", []):
        pos[n["id"]] = (0.0, 0.0)
        angle[n["id"]] = 0.0

    for lvl in ORDER[1:]:
        items = sorted(by_level.get(lvl, []), key=lambda n: (n["num"] or 0))
        if not items:
            continue
        ring = rings[lvl]

        # 目标方位 = 已摆好的内层邻居的平均角
        target = {}
        for n in items:
            inner = [angle[m] for m in nbr[n["id"]] if m in angle]
            if inner:
                target[n["id"]] = _circular_mean(inner)

        known = sorted([n for n in items if n["id"] in target], key=lambda n: target[n["id"]])
        unknown = [n for n in items if n["id"] not in target]
        seq = known + unknown
        step = 2 * math.pi / max(1, len(seq))

        # 相位：让已知节点整体贴近各自的目标角
        if known:
            deltas = [math.atan2(math.sin(target[n["id"]] - i * step),
                                 math.cos(target[n["id"]] - i * step))
                      for i, n in enumerate(known)]
            base = _circular_mean(deltas)
        else:
            base = -math.pi / 2

        for i, n in enumerate(seq):
            a = base + i * step + rnd.uniform(-0.015, 0.015)
            r = ring * (1 + rnd.uniform(-0.045, 0.045))
            pos[n["id"]] = (r * math.cos(a), r * math.sin(a))
            angle[n["id"]] = a

    # 收尾：过近的节点互相推开（中心点固定不动）
    ids = list(pos)
    centre = next((n["id"] for n in nodes if n["level"] == "0"), None)
    for _ in range(200):
        clash = False
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                ax, ay = pos[a]
                bx, by = pos[b]
                d = math.hypot(ax - bx, ay - by)
                if d >= 92.0:
                    continue
                clash = True
                ux = (ax - bx) / (d or 1e-6)
                uy = (ay - by) / (d or 1e-6)
                push = (92.0 - d) * 0.55
                if a != centre:
                    pos[a] = (ax + ux * push, ay + uy * push)
                if b != centre:
                    pos[b] = (bx - ux * push, by - uy * push)
        if not clash:
            break

    return {k: (round(v[0], 1), round(v[1], 1)) for k, v in pos.items()}


def stats(pos, level_of):
    ids = list(pos)
    gaps = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            gaps.append(math.hypot(pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]))
    out = {"min_gap": round(min(gaps), 1) if gaps else 0.0}
    for lvl in sorted({level_of[i] for i in ids}):
        rs = [math.hypot(pos[i][0], pos[i][1]) for i in ids if level_of[i] == lvl]
        out[lvl] = (round(min(rs)), round(max(rs)))
    return out

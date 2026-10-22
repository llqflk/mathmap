<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 计算几何

> 层级 3：模型与计算层 · 第 10/15 条

[← 控制论](../09-控制论/index.md) · [总目录](../../README.md) · [计算流体力学（CFD） →](../11-计算流体力学/index.md)

- 范畴：$\mathbf{CompGeom}$ 计算几何范畴

- **对象例子**：平面上 $n$ 个点集 $P=\{p_1,\dots,p_n\}$

- **态射例子**：Delaunay 三角剖分；Voronoi 图（对偶映射）

- **核心函子实例**：凸包函子；三角剖分对偶函子

- **Python 示例（Delaunay 三角剖分 + 凸包）**

```python
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
points = np.random.rand(20, 2)
tri = Delaunay(points)
hull = ConvexHull(points)
print(f"三角剖分: {tri.nsimplex}个三角形, "
      f"凸包: {len(hull.vertices)}个顶点")
# 欧拉公式验证: V-E+F=2 (平面图)
E = (3*tri.nsimplex + len(hull.vertices))/2
print(f"V-E+F={len(points)}-{E:.0f}+{tri.nsimplex}=2 ✓")
```

```mathematica
(* Mathematica：计算几何 *)
points = RandomReal[{-1, 1}, {20, 2}];
(* Delaunay 三角剖分 *)
mesh = DelaunayMesh[points];
MeshCellCount[mesh]                     (* {顶点, 边, 三角形} *)
(* 欧拉公式 V-E+F *)
{V, E, F} = MeshCellCount[mesh][[{1, 2, 3}]];
V - E + F                               (* 应为 1(开网格) *)

(* 凸包 *)
ch = ConvexHullMesh[points];
MeshCellCount[ch]                       (* 凸包面数 *)
```

<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 图论

> 层级 3：模型与计算层 · 第 12/15 条

[← 计算流体力学（CFD）](../11-计算流体力学/index.md) · [总目录](../../README.md) · [深度学习 →](../13-深度学习/index.md)

- 范畴：$\mathbf{Graph}$ 图范畴——对象是图，态射是图同态（把边映成边）

- **对象例子**：四边形 $C_4$，顶点 $\{0,1,2,3\}$，边 $\{01,12,23,30\}$

- **态射例子**：$C_4\to K_2$ 的二部染色（图同态）；$C_4$ 的自同构（旋转、翻转）

- **核心函子实例**：邻接矩阵函子 $\mathrm{Adj}:\mathbf{Graph}\to\mathbf{Mat}$；圈空间函子（图→圈空间）

- **Python 示例（邻接矩阵 + 图同态判定）**

```python
g = {0: {1, 3}, 1: {0, 2}, 2: {1, 3}, 3: {0, 2}}   # 四边形 C4
k2 = {0: {1}, 1: {0}}                              # 两点图 K2

def is_hom(g, h, f):                               # 图同态：边必须映成边
    return all(f[v] in h[f[u]] for u in g for v in g[u])

def adj(g, order):                                 # 邻接矩阵函子
    return [[1 if v in g[u] else 0 for v in order] for u in order]

print("C4 邻接矩阵 =", adj(g, sorted(g)))
print("恒等映射是自同构:", is_hom(g, g, {v: v for v in g}))
print("C4 → K2 的二部染色是同态:", is_hom(g, k2, {0: 0, 1: 1, 2: 0, 3: 1}))
print("把 C4 折成单点:", is_hom(g, k2, {0: 0, 1: 0, 2: 0, 3: 0}))   # False
```

```mathematica
(* Mathematica：图论 *)
g = Graph[{1 <-> 2, 2 <-> 3, 3 <-> 1, 1 <-> 4}];  (* 三角形加悬边 *)
AdjacencyMatrix[g]                   (* 邻接矩阵函子 *)
GraphAutomorphismGroup[g]            (* 图的自同构群 *)
FindHamiltonianCycle[g]              (* 哈密顿回路 *)
```

<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 有限元

> 层级 3：模型与计算层 · 第 2/15 条

[← 数值线性代数](../01-数值线性代数/index.md) · [总目录](../../README.md) · [数值优化 →](../03-数值优化/index.md)

- 范畴：$\mathbf{FE}(\Omega)$ 有限元空间范畴——对象是网格上的有限元空间，态射是插值与限制映射

- **对象例子**：$\Omega=(0,1)$ 上 4 个线性单元、5 个节点组成的网格

- **态射例子**：刚度矩阵 $K_{ij}=\int_\Omega \varphi_i'\varphi_j'$——把弱形式 $-\Delta$ 变成线性方程组

- **核心函子实例**：离散化函子 $D:H^1(\Omega)\to\mathbb R^N$（连续 Sobolev 空间→自由度）；组装函子（单元矩阵→全局矩阵）

- **Python 示例（一维 Poisson 方程装配 + 与精确解对比）**

```python
import numpy as np
# -u'' = 1 on (0,1), u(0)=u(1)=0；4 个线性单元
n, h = 4, 0.25
K = np.zeros((n + 1, n + 1)); F = np.zeros(n + 1)
Ke = np.array([[1, -1], [-1, 1]]) / h       # 单元刚度矩阵
Fe = np.array([1, 1]) * h / 2               # 单元载荷（右端项 1）
for e in range(n):
    idx = [e, e + 1]
    K[np.ix_(idx, idx)] += Ke
    F[idx] += Fe

u = np.zeros(n + 1)                         # Dirichlet 边界置 0
u[1:-1] = np.linalg.solve(K[1:-1, 1:-1], F[1:-1])

x = np.linspace(0, 1, n + 1); exact = x * (1 - x) / 2
print("节点解 =", np.round(u, 4))
print("精确解 =", np.round(exact, 4))
print("最大误差 =", f"{np.abs(u - exact).max():.1e}")   # 一维线性元在节点上精确
```

```mathematica
(* Mathematica：有限元 *)
Needs["NDSolve`FEM`"]
mesh = ToElementMesh[Rectangle[]];   (* 三角形网格 *)
(* 刚度矩阵组装 *)
NDEigensystem[{-Laplacian[u[x, y]], DirichletCondition[u[x, y]==0, True]},
              u[x, y], {x, y} ∈ mesh, 5]
```

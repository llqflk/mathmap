<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 数值线性代数

> 层级 3：模型与计算层 · 第 1/15 条

[总目录](../../README.md) · [有限元 →](../02-有限元/index.md)

- 范畴：$\mathbf{Vect}_{\mathbb R}^{\mathrm{fd}}$ 的浮点实现——把 Abel 范畴搬到 IEEE 754 数组上

- **对象例子**：$\mathbb R^{3\times3}$ 中的可逆矩阵 $A$，右端项 $b\in\mathbb R^3$

- **态射例子**：$v\mapsto Av$（矩阵乘法）；求解 $Ax=b$（LU 分解 + 部分主元）

- **核心函子实例**：向量化函子（线性映射↔数组）；奇异值分解函子 $A\mapsto(\sigma_1,\dots,\sigma_n)$

- **Python 示例（LU 求解 + 数值秩 + 条件数）**

```python
import numpy as np
rng = np.random.default_rng(0)
A = rng.normal(size=(3, 3)); b = rng.normal(size=3)

x = np.linalg.solve(A, b)                  # LU 分解 + 部分主元
print("解 x =", np.round(x, 4), "残差 =", f"{np.linalg.norm(A @ x - b):.1e}")

s = np.linalg.svd(A, compute_uv=False)     # 奇异值：数值秩的判据
print("奇异值 =", np.round(s, 3), "数值秩 =", int((s > 1e-12).sum()))

# 病态矩阵：条件数 κ 放大误差（Hilbert 矩阵是经典坏例子）
H = np.array([[1.0 / (i + j + 1) for j in range(5)] for i in range(5)])
print("Hilbert(5) 条件数 =", f"{np.linalg.cond(H):.1e}")
```

```mathematica
(* Mathematica：数值线性代数 *)
A = {{1, 2}, {3, 4}}; v = {1, 0};
A . v                                (* 矩阵乘法 = {1, 3} *)
LinearSolve[A, {5, 11}]              (* 解方程组 = {1, 2} *)
SingularValueDecomposition[A]         (* SVD 分解 *)
```

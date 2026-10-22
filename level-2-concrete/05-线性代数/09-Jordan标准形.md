# 第 9 章：Jordan 标准形

> [← 返回《线性代数》目录](index.md) · [总目录](../../README.md)

> 不可对角化矩阵的最终分类。$\mathbb C[x]$-模结构定理 → Jordan 形。幂零部分的存在是 $\mathbf{Vect}_k$ 与 $\mathbf{Hilb}_{\text{fd}}$ 的根本区别。

---

## 9.1 不可对角化的本质

$J=\begin{pmatrix}0&1\\0&0\end{pmatrix}$：$m_a(0)=2$，$m_g(0)=\dim\ker J=1$。$J^2=0$，但 $J\neq0$。

**几何直觉**：Jordan 块代表一个"推移"作用——$e_2\mapsto e_1\mapsto 0$，形成一个长度为 2 的链。

**本章代码约定**（下文示例沿用这两个导入）

```python
import numpy as np
import matplotlib.pyplot as plt
```

```python
# 可视化：Jordan块的推移作用
J = np.array([[0, 1], [0, 0]])
v1 = np.array([1, 0]); v2 = np.array([0, 1])

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
axes[0].quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='b', width=0.06, label='e₁')
axes[0].quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color='r', width=0.06, label='e₂')
axes[0].set_xlim(-0.5, 2); axes[0].set_ylim(-0.5, 2); axes[0].set_aspect('equal')
axes[0].set_title('原始基'); axes[0].legend(); axes[0].grid(True)

Jv1, Jv2 = J @ v1, J @ v2
axes[1].quiver(0, 0, Jv1[0], Jv1[1], angles='xy', scale_units='xy', scale=1, color='b', width=0.06, label='Je₁=0')
axes[1].quiver(0, 0, Jv2[0], Jv2[1], angles='xy', scale_units='xy', scale=1, color='r', width=0.06, label='Je₂=e₁')
axes[1].set_xlim(-0.5, 2); axes[1].set_ylim(-0.5, 2); axes[1].set_aspect('equal')
axes[1].set_title('J 作用一次: e₂→e₁→0'); axes[1].legend(); axes[1].grid(True)

axes[2].text(0.3, 0.5, 'J² = 0\n所有向量归零\n(幂零指数=2)', fontsize=14, ha='center')
axes[2].set_xlim(0, 1); axes[2].set_ylim(0, 1); axes[2].axis('off')
plt.tight_layout(); plt.show()
```

```mathematica
(* Jordan块推移 *)
J = {{0, 1}, {0, 0}};
GraphicsRow[{Graphics[{Blue,Arrow[{{0,0},{1,0}}],Red,Arrow[{{0,0},{0,1}}]},Axes->True,PlotRange->2],
  Graphics[{Blue,Point[{0,0}],Red,Arrow[{{0,0},{1,0}}]},Axes->True,PlotRange->2]}]
```

---

## 9.2 Jordan 标准形定理

任意复方阵 $A$ 相似于唯一 Jordan 形 $A=PJP^{-1}$：
$$J=\bigoplus_{k=1}^r J_{n_k}(\lambda_k),\qquad J_n(\lambda)=\begin{pmatrix}\lambda&1&&\\&\ddots&\ddots&\\&&\lambda&1\\&&&\lambda\end{pmatrix}$$

- $\lambda$ 的代数重数 $=\sum n_k$（含 $\lambda$ 的块的阶数和）
- $\lambda$ 的几何重数 $=$ 含 $\lambda$ 的块的**个数**
- 最大块阶数 $=$ $(x-\lambda)$ 在极小多项式中的幂次

**广义特征空间**：$G_\lambda=\ker(A-\lambda I)^{m_a(\lambda)}$，$\dim G_\lambda=m_a(\lambda)$。

```python
# 3x3 Jordan块的空间变形
J3 = np.array([[2, 1, 0], [0, 2, 1], [0, 0, 2]])
np.random.seed(0); pts = np.random.randn(3, 100); pts /= np.linalg.norm(pts, axis=0)
pts_t = J3 @ pts

fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(*pts, c='blue', alpha=0.4, s=8)
ax1.set_title('原始 (单位球面)')
ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(*pts_t, c='red', alpha=0.4, s=8)
ax2.set_title('J₃(2) 作用后'); plt.tight_layout(); plt.show()
```

```mathematica
(* Jordan块3D *)
J = {{2,1,0},{0,2,1},{0,0,2}};
sphere = RandomPoint[Sphere[], 200];
GraphicsRow[{Graphics3D[Point[sphere]], Graphics3D[Point[J.#& /@ sphere]]}]
```

---

## 9.3 Jordan-Chevalley 分解

$A=S+N$：$S$ 半单（可对角化），$N$ 幂零，$SN=NS$。两者都是 $A$ 的多项式。

可对角化 $\iff N=0$。

```python
# e^{Jt} 的显式结构
from scipy.linalg import expm
J3 = np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
t_vals = np.linspace(0, 3, 100)
traj = np.array([expm(t*J3) @ [1, 0, 0] for t in t_vals])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(traj[:,0], traj[:,1], traj[:,2], 'b-', linewidth=2)
ax.scatter([1],[0],[0], s=60, c='red', zorder=5)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
ax.set_title('e^{tJ₃(1)}·e₁ = e^t(1, t, t²/2)'); plt.show()
```

```mathematica
(* e^{Jt} *)
J = {{1,1,0},{0,1,1},{0,0,1}};
ParametricPlot3D[MatrixExp[t J].{1,0,0}, {t,0,3}]
```

---
**范畴论**：$(V,T)$ 是 $\mathbb C[x]$-挠模。PID 上有限生成模的结构定理 → $V\cong\bigoplus\mathbb C[x]/(x-\lambda_j)^{n_j}$。每个循环模 = 一个 Jordan 块。Krull-Schmidt 保证唯一性。对比：$\mathbf{Hilb}_{\text{fd}}$ 自伴 → 总是可对角化；$\mathbf{Vect}_{\mathbb C}$ 任意自同态 → 可能含幂零部分。

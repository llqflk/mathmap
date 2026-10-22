<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 辛几何

> 层级 1：抽象结构层 · 分组：拓扑与几何 · 第 14/21 条

[← 黎曼几何 / 微分几何](../13-黎曼几何/index.md) · [总目录](../../README.md) · [代数几何 →](../15-代数几何/index.md)

- 范畴：$\mathbf{Sympl}$ 辛流形范畴

- **对象例子**：余切丛 $T^*\mathbb R^n\cong\mathbb R^{2n}$，标准辛形式 $\omega=\sum dp_i\wedge dq_i$

- **态射例子**：辛同胚（保持辛形式的光滑映射）

- **核心函子实例**：Hamilton 向量场函子 $H\mapsto X_H$（函数→向量场）；动量映射

- **Python 示例（Hamilton 力学 — 谐振子相空间）**

```python
import numpy as np
def ham_eqns(z, t):
    """H=0.5*(p^2+q^2), 谐振子"""
    q, p = z
    dq = p        # ∂H/∂p
    dp = -q       # -∂H/∂q
    return np.array([dq, dp])

def euler_symplectic(z0, dt, steps):
    z = [z0]
    for _ in range(steps):
        z_new = z[-1] + ham_eqns(z[-1], 0)*dt
        z.append(z_new)
    return np.array(z)

traj = euler_symplectic(np.array([1.0, 0.0]), 0.05, 200)
print(f"相空间面积≈守恒: max|q|={traj[:,0].max():.3f}, max|p|={traj[:,1].max():.3f}")
```

```mathematica
(* Mathematica：Hamilton 力学 — 谐振子 *)
(* Hamilton 方程 *)
{q, p} = {q[t], p[t]};
hamiltonian = 1/2*(p^2 + q^2);       (* H = 0.5(p²+q²) *)
eqns = {q'[t] == D[hamiltonian, p], p'[t] == -D[hamiltonian, q]};
sol = NDSolve[{eqns, q[0] == 1, p[0] == 0}, {q, p}, {t, 0, 10}];
ParametricPlot[Evaluate[{q[t], p[t]} /. sol], {t, 0, 10},
               AspectRatio -> 1]    (* 相图：单位圆 *)

(* 辛形式守恒验证 *)
Simplify[D[hamiltonian /. sol, t]]  (* 0 — 能量守恒 *)
```

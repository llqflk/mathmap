### 12. 计算流体力学（CFD）

- 范畴：$\mathbf{CFD}$ 连续介质离散化范畴

- **对象例子**：速度场 $\mathbf u(\mathbf x,t)$，控制体积 $\Omega$

- **态射例子**：对流-扩散算子；SIMPLE 压力修正步

- **核心函子实例**：有限体积离散函子（NS方程→代数方程组）

- **Python 示例（一维对流方程迎风格式）**

```python
import numpy as np
def advection_1d(u0, c=1.0, dx=0.02, dt=0.01, steps=200):
    u = u0.copy()
    C = c*dt/dx  # CFL数
    for _ in range(steps):
        u[1:] -= C*(u[1:]-u[:-1])  # 迎风差分
    return u

nx = 200; u0 = np.exp(-(np.linspace(0,2,nx)-0.5)**2/0.01)
u = advection_1d(u0, c=1.0)
print(f"质量守恒: sum(u0)={u0.sum():.3f}, sum(u)={u.sum():.3f}, "
      f"传播距离≈1.0")
```

```mathematica
(* Mathematica：计算流体力学 *)
(* 一维对流方程 ∂_t u + c ∂_x u = 0 *)
c = 1; dx = 0.02; dt = 0.01; nx = 200;
C = c*dt/dx;                          (* CFL数 *)
u0 = Table[Exp[-((i*dx - 0.5)^2/0.01)], {i, 1, nx}];

(* 迎风差分迭代 *)
u = u0;
Do[u[[2 ;;]] -= C*(u[[2 ;;]] - u[[1 ;; -2]]), {200}];
{Total[u0], Total[u]}                 (* 质量守恒验证 *)

(* 或用内置 PDE 求解器 *)
sol = NDSolve[{D[u[t, x], t] + D[u[t, x], x] == 0,
       u[0, x] == Exp[-((x - 0.5)^2/0.01)],
       u[t, 0] == 0},
      u, {t, 0, 2}, {x, 0, 4}];
Plot3D[u[t, x] /. sol, {t, 0, 2}, {x, 0, 4}]
```

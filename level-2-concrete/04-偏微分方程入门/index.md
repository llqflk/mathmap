### 5. 偏微分方程入门（PDE）

- 范畴：$\mathbf{DiffOp}$ 微分算子范畴

- **对象例子**：热方程 $\partial_t u=\alpha\nabla^2 u$ 的解空间

- **态射例子**：拉普拉斯算子 $\nabla^2$、传播子（Green 函数）

- **核心函子实例**：分离变量函子（PDE→ODE 组）；Fourier 变换将微分算子转为乘法

- **Python 示例（一维热方程显式差分）**

```python
import numpy as np
def heat_1d(u0, alpha=0.1, dx=0.1, dt=0.005, steps=500):
    u = u0.copy()
    r = alpha*dt/dx**2
    for _ in range(steps):
        u[1:-1] += r*(u[2:]-2*u[1:-1]+u[:-2])
    return u

u0 = np.zeros(100); u0[40:60] = 1.0  # 初始热脉冲
u = heat_1d(u0)
print(f"峰温从1衰减到{u.max():.3f}，两端绝热")
```

```mathematica
(* Mathematica：热方程解析+数值解 *)
(* 解析解（分离变量法） *)
DSolve[{D[u[t, x], t] == D[u[t, x], {x, 2}], u[0, x] == E^(-100*(x - 0.5)^2)},
       u[t, x], {t, x}]

(* 数值解 *)
sol = NDSolve[{D[u[t, x], t] == 0.1*D[u[t, x], {x, 2}],
       u[0, x] == Piecewise[{{1, 0.4 <= x <= 0.6}}], 
       u[t, 0] == 0, u[t, 1] == 0},
       u, {t, 0, 0.2}, {x, 0, 1}];
Plot3D[u[t, x] /. sol, {t, 0, 0.2}, {x, 0, 1}]
```

---

## 代数类

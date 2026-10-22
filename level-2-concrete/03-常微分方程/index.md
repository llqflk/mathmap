### 4. 常微分方程 ODE

- 范畴：$\mathbf{Dyn}$ 动力系统范畴

- **对象例子**：状态空间 $\mathbb R^2$（位置 + 速度）

- **态射例子**：单摆演化函数，$x(t+\Delta t)=F(x(t))$

- **核心函子实例**：时间演化自函子 $\Phi_t$，把初始状态映射为轨迹

- **Python 示例（欧拉法）**

```python
def euler(df, x0, t_end, dt=0.01):
    x = x0
    traj = [x]
    for _ in range(int(t_end/dt)):
        x += df(x)*dt
        traj.append(x)
    return traj

df = lambda x: -x  # dx/dt=-x
print(euler(df, 1, 2)[-1])
```

```mathematica
(* Mathematica：ODE 解析解 + 数值解 *)
sol = DSolve[{x'[t] == -x[t], x[0] == 1}, x[t], t]
(* 解析解：x[t] → E^-t *)

(* 数值解 *)
nsol = NDSolve[{x'[t] == -x[t], x[0] == 1}, x, {t, 0, 2}]
x[2] /. nsol           (* ≈ 0.135 *)
```

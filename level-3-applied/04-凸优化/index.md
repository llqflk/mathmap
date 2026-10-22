<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 凸优化

> 层级 3：模型与计算层 · 第 4/15 条

[← 数值优化](../03-数值优化/index.md) · [总目录](../../README.md) · [贝叶斯统计与MCMC →](../05-贝叶斯统计与MCMC/index.md)

- 范畴：$\mathbf{Conv}$ 凸集范畴——对象是凸集，态射是仿射映射（保持凸组合）

- **对象例子**：半空间 $C=\{(x,y)\in\mathbb R^2\mid x+y\le 2\}$

- **态射例子**：欧氏投影 $P_C$（把任意点压回凸集）；投影梯度步 $x\mapsto P_C(x-\eta\nabla f)$

- **核心函子实例**：共轭对偶函子 $f\mapsto f^*$（Legendre 变换）；支撑函数函子 $C\mapsto h_C$

- **Python 示例（投影梯度法 + KKT 乘子校验）**

```python
import numpy as np
f = lambda v: (v[0] - 3) ** 2 + (v[1] - 1) ** 2               # 目标函数
grad = lambda v: np.array([2 * (v[0] - 3), 2 * (v[1] - 1)])
proj = lambda v: v - max(0.0, v.sum() - 2) / 2 * np.ones(2)   # 投影到 x+y<=2

v, lr = np.zeros(2), 0.1
for _ in range(300):                                          # 投影梯度法
    v = proj(v - lr * grad(v))
print("最优解 =", np.round(v, 4), "最优值 =", round(f(v), 4))

lam = -grad(v).sum() / 2                                      # KKT 乘子
print("KKT 乘子 λ =", round(lam, 3), "≥ 0:", lam >= 0)
print("无约束极小是 (3,1)，但违反约束——约束确实起作用")
```

```mathematica
(* Mathematica：凸优化 *)
(* 无约束优化 *)
Minimize[x^2 + 2 Sin[x], x]         (* 全局最小 *)

(* 约束优化：min x^2 s.t. x >= 1 *)
Minimize[{x^2, x >= 1}, x]          (* x=1, 最小=1 *)

(* 线性规划 *)
LinearOptimization[2 x + y, {x + y >= 1, x >= 0, y >= 0}, {x, y}]
```

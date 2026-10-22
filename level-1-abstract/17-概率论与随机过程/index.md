### 17. 概率论与随机过程

- 范畴：带滤波概率空间范畴

- **对象例子**：布朗运动路径空间

- **态射例子**：伊藤积分

- **核心函子实例**：条件期望函子

- **Python 示例（简单条件期望）**

```python
import numpy as np
X = np.random.randn(1000)
Y = X + np.random.randn(1000)
# E[X|Y] 近似
```

```mathematica
(* Mathematica：条件期望 *)
dist = BinormalDistribution[{0, 0}, {1, Sqrt[2]}, 1/Sqrt[2]];
(* 理论 E[X|Y=y] *)
Expectation[x \[Conditioned] y == y0, {x, y} \[Distributed] dist]

(* 或数值模拟 *)
X = RandomVariate[NormalDistribution[], 1000];
Y = X + RandomVariate[NormalDistribution[], 1000];
lm = LinearModelFit[Transpose[{Y, X}], {1, y}, y];
lm["BestFit"]                        (* 回归线 ≈ E[X|Y] *)
```



- 范畴：$(\Omega,\mathcal F,\{\mathcal F_t\}_{t\ge0},\mathbb P)$ 带滤波概率空间

- **对象例子**：布朗运动 $(B_t)_{t\ge0}$（连续鞅）

- **态射例子**：停时 $\tau$（适应映射）；伊藤积分 $\int_0^t H_s dB_s$

- **核心函子实例**：鞅变换函子（鞅↔博弈）；条件期望函子

- **Python 示例（布朗运动路径模拟 + 鞅性验证）**

```python
import numpy as np
def brownian(n_steps=1000, dt=0.01):
    dB = np.random.randn(n_steps)*np.sqrt(dt)
    B = np.cumsum(dB)
    B = np.insert(B, 0, 0)
    return B

B = brownian()
# 鞅性: E[B_t|F_s]=B_s, 增量独立且零均值
increments = np.diff(B)
print(f"增量均值={increments.mean():.4f} (应为0), "
      f"增量方差≈{increments.var():.4f} (应为{0.01})")
# 停时模拟: 首次触达水平a的策略
```

```mathematica
(* Mathematica：布朗运动与随机过程 *)
(* 布朗运动模拟 *)
steps = 1000; dt = 0.01;
dB = RandomVariate[NormalDistribution[0, Sqrt[dt]], steps];
B = Accumulate[Prepend[dB, 0]];
(* 鞅性：增量零均值 *)
Mean[Differences[B]]              (* ≈ 0 *)
Variance[Differences[B]]          (* ≈ 0.01 *)

(* 内置随机过程 *)
proc = WienerProcess[];
ListLinePlot[RandomFunction[proc, {0, 10, 0.01}]["Values"]]

(* 停时：首达时间 *)
sim = RandomFunction[proc, {0, 10, 0.01}];
FirstPassageTimeDistribution[proc, 1.0]
```

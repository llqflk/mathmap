<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 概率论与数理统计

> 层级 2：具体结构层 · 分组：概率与统计类 · 第 9/11 条

[← 解析几何 / 微分几何入门](../08-解析几何/index.md) · [总目录](../../README.md) · [组合与离散数学 →](../10-组合与离散数学/index.md)

- 范畴：$\mathbf{FinProb}$ 有限概率空间范畴

- **对象例子**：样本空间 $\{\text{头},\text{尾}\}$，伯努利分布

- **态射例子**：随机变量 $X:\{\text{头},\text{尾}\}\to\{0,1\}$

- **核心函子实例**：期望函子 $\mathbb E$；分布 Monad

- **Python 示例（简单 Monad 思想）**

```python
import random
# 分布Monad：输入值，输出带概率的采样
def pure(x): return lambda: x
def bind(dist, f): return lambda: f(dist())()

coin = lambda: random.choice([0,1])
double = lambda x: pure(2*x)
res = bind(coin, double)
print(res())
```

```mathematica
(* Mathematica：分布与期望的 Monad 思想 *)
pure[x_] := x &
bind[dist_, f_] := f[dist[]] &

coin[] := RandomChoice[{0, 1}]
double[x_] := 2 x
bind[coin, double]

(* 更自然的方式：直接使用内置分布 *)
dist = BernoulliDistribution[0.5];
RandomVariate[dist, 10]  (* 10次采样 *)
```



- 范畴：$\mathbf{Stat}$ 统计模型范畴

- **对象例子**：参数空间 $\Theta=\{\theta\mid\theta>0\}$（如指数族参数）

- **态射例子**：估计量 $T:\mathcal X\to\Theta$（样本→参数估计）

- **核心函子实例**：充分统计量函子（样本→压缩信息）；Fisher 信息度规

- **Python 示例（MLE 估计 + 置信区间）**

```python
import numpy as np
from scipy import stats
data = np.random.normal(loc=5.0, scale=2.0, size=200)
mu_hat = np.mean(data)           # MLE of mean
sigma_hat = np.std(data, ddof=1) # MLE of std
ci = stats.t.interval(0.95, df=len(data)-1,
                      loc=mu_hat, scale=sigma_hat/np.sqrt(len(data)))
print(f"μ的MLE={mu_hat:.2f}, 95%CI=[{ci[0]:.2f},{ci[1]:.2f}]")
```

```mathematica
(* Mathematica：统计推断 *)
data = RandomVariate[NormalDistribution[5, 2], 200];
muHat = Mean[data];                  (* MLE *)
sigmaHat = StandardDeviation[data];  (* MLE *)
ci = MeanAround[data];               (* 置信区间 *)

(* 用内置符号分布 *)
dist = EstimatedDistribution[data, NormalDistribution[μ, σ]];
dist                                 (* NormalDistribution[5.03, 1.98] *)
```

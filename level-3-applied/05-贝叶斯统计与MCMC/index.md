### 5. 贝叶斯统计与MCMC

- 范畴：统计模型范畴

- 对象：正态先验

- 态射：后验更新

- 函子：条件概率 Monad bind

- 示例：PyMC3 采样

```mathematica
(* Mathematica：贝叶斯推断 *)
(* 正态-逆Gamma先验 → 后验更新 *)
data = RandomVariate[NormalDistribution[5, 2], 100];
(* 共轭先验 *)
prior = NormalDistribution[μ0, σ0/Sqrt[n0]];
posterior = NormalDistribution[
    (μ0*n0 + Total[data])/(n0 + Length[data]),
    2/Sqrt[n0 + Length[data]]];
posterior
```



- 范畴：$\mathbf{MC}$ 随机模拟范畴

- **对象例子**：目标分布 $\pi(x)$（如贝叶斯后验）

- **态射例子**：MCMC 转移核 $T(x\to y)$（保持 $\pi$ 不变）

- **核心函子实例**：重要性采样函子（分布变换）；Metropolis-Hastings 函子

- **Python 示例（Metropolis-Hastings 采样）**

```python
import numpy as np
def target(x):
    return np.exp(-0.5*x**2)  # 标准正态(unormalized)

def metropolis(n=5000, sigma=0.5):
    x = 0.0; samples = []
    for _ in range(n):
        x_prop = x + sigma*np.random.randn()
        alpha = min(1, target(x_prop)/target(x))
        if np.random.rand() < alpha:
            x = x_prop
        samples.append(x)
    return np.array(samples)

samples = metropolis()
print(f"采样均值={samples.mean():.3f}, 采样方差={samples.var():.3f}")
print(f"理论值: mean=0 std=1")
```

```mathematica
(* Mathematica：Metropolis-Hastings *)
targetPDF[x_] := Exp[-x^2/2]  (* 目标：标准正态(unormalized) *)

(* MCMC *)
samples = {};
x = 0; sigma = 0.5;
Do[
  xProp = x + RandomVariate[NormalDistribution[0, sigma]];
  alpha = Min[1, targetPDF[xProp]/targetPDF[x]];
  If[RandomReal[] < alpha, x = xProp];
  AppendTo[samples, x],
{10000}];
{Mean[samples], StandardDeviation[samples]}  (* ≈{0, 1} *)
```

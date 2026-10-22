<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 信息论

> 层级 3：模型与计算层 · 第 6/15 条

[← 贝叶斯统计与MCMC](../05-贝叶斯统计与MCMC/index.md) · [总目录](../../README.md) · [密码学 →](../07-密码学/index.md)

- 范畴：$\mathbf{Prob}$ 概率分布范畴（对象为分布，态射为信道）

- **对象例子**：离散分布 $p_X$（如公平硬币的 Bernoulli 分布）

- **态射例子**：信道 $W(Y|X)$（条件分布）；信源编码

- **核心函子实例**：熵函子 $H$（分布→实数）；互信息函子

- **Python 示例（熵与 KL 散度计算）**

```python
import numpy as np
def entropy(p):
    p = np.array(p) + 1e-12
    return -np.sum(p*np.log2(p))

def kl_div(p, q):
    p, q = np.array(p)+1e-12, np.array(q)+1e-12
    return np.sum(p*np.log2(p/q))

# 公平硬币 H=1 bit
print(f"H(fair)={entropy([0.5,0.5]):.3f}")
# 偏置硬币 H<1
print(f"H(biased)={entropy([0.9,0.1]):.3f}")
print(f"KL(p||q)={kl_div([0.5,0.5],[0.9,0.1]):.3f}")
```

```mathematica
(* Mathematica：信息论 *)
(* 熵 *)
entropy[p_] := -Total[p * Log2[p + $MachineEpsilon]]
entropy[{0.5, 0.5}]                          (* 1.0 bit *)
entropy[{0.9, 0.1}]                          (* 0.469 bit *)

(* KL 散度 *)
kl[p_, q_] := Total[p * Log2[p/(q + $MachineEpsilon) + $MachineEpsilon]]
kl[{0.5, 0.5}, {0.9, 0.1}]                  (* 0.531 bit *)
```

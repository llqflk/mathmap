### 15. 金融数学

- 范畴：$\mathbf{Mkt}$ 市场模型范畴——对象为概率空间上的资产与衍生品

- **对象例子**：几何布朗运动 $dS_t=\mu S_t dt+\sigma S_t dW_t$（Black-Scholes 标的资产）

- **态射例子**：自融资交易策略 $\phi_t=(\Delta_t,\Gamma_t)$；Girsanov 测度变换（物理测度→风险中性测度）

- **核心函子实例**：定价函子 $\Pi$（衍生品→无套利价格）；对冲函子（衍生品→复制组合）

- **Python 示例（Black-Scholes 定价 + Monte Carlo）**

```python
import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option='call'):
    """Black-Scholes 欧式期权定价"""
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option == 'call':
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

def monte_carlo_price(S0, K, T, r, sigma, paths=100000):
    """Monte Carlo 定价验证"""
    Z = np.random.randn(paths)
    ST = S0 * np.exp((r - sigma**2/2)*T + sigma*np.sqrt(T)*Z)
    payoff = np.maximum(ST - K, 0)
    return np.exp(-r*T) * payoff.mean()

# 定价
S, K, T, r, sigma = 100, 105, 1, 0.05, 0.2
bs_price = black_scholes(S, K, T, r, sigma)
mc_price = monte_carlo_price(S, K, T, r, sigma, paths=50000)
print(f"BS: {bs_price:.3f}, MC: {mc_price:.3f}")
```

```mathematica
(* Mathematica：金融数学 *)
(* Black-Scholes 公式 *)
FinancialDerivative[{"European", "Call"},
  {"StrikePrice" -> 105, "Expiration" -> 1},
  {"InterestRate" -> 0.05, "CurrentPrice" -> 100,
   "Volatility" -> 0.2}]

(* Girsanov 测度变换 *)
ItoProcess[\[DifferentialD]S[t] == \[Mu] S[t] \[DifferentialD]t +
   \[Sigma] S[t] \[DifferentialD]W[t], S[t], {S, S0}, t, W \[Distributed] WienerProcess[]]
```

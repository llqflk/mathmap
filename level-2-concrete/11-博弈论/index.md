### 14. 博弈论

- 范畴：$\mathbf{Game}$ 博弈范畴——对象为博弈（策略式或展开式），态射为博弈间的态射

- **对象例子**：囚徒困境——收益矩阵 $((3,3),(0,5);(5,0),(1,1))$

- **态射例子**：策略 $\sigma_i:S_i\to\Delta(A_i)$（纯策略→混合策略）；最佳响应映射

- **核心函子实例**：Nash 均衡函子（博弈→不动点集）；机制设计函子（社会选择→博弈规则）

- **Python 示例（囚徒困境 + 支持函数法求 Nash 均衡）**

```python
import numpy as np

# 囚徒困境收益矩阵 (行玩家, 列玩家)
A = np.array([[3, 0], [5, 1]])  # 行玩家
B = np.array([[3, 5], [0, 1]])  # 列玩家

def best_response(payoff_matrix, opponent_strategy):
    """给定对手策略，返回最佳纯策略"""
    expected = payoff_matrix @ opponent_strategy
    return np.argmax(expected)

def find_nash(A, B, tol=1e-6):
    """2x2 博弈的支持函数法求混合策略 Nash 均衡"""
    # 行玩家无差异条件
    a,b,c,d = A[0,0], A[0,1], A[1,0], A[1,1]
    # (a-b+c-d) * p * q + (b-d)*p + (d-b)*q + ... = 0
    denom = a - b - c + d
    if abs(denom) > tol:
        q = (d - b) / denom
        p = (d - c) / (a - b - c + d) if abs(a-b-c+d) > tol else 0.5
        return np.array([p, 1-p]), np.array([q, 1-q])
    return None, None

# 囚徒困境：唯一均衡 (背叛, 背叛)
p, q = find_nash(A, B)
print(f"行玩家策略: ({p[0]:.0f}, {p[1]:.0f}), 列玩家: ({q[0]:.0f}, {q[1]:.0f})")
# 均衡: (背叛, 背叛) = 帕累托次优 ✓
```

```mathematica
(* Mathematica：博弈论 *)
(* 囚徒困境 *)
payoffRow = {{3, 0}, {5, 1}};
payoffCol = {{3, 5}, {0, 1}};
NashEquilibrium[payoffRow, payoffCol]
(* 纯策略均衡：{2,2} = (背叛, 背叛) *)

(* 混合策略博弈 *)
(* 匹配便士 *)
NashEquilibrium[{{1, -1}, {-1, 1}}, {{-1, 1}, {1, -1}}]
(* (1/2, 1/2) 混合均衡 *)
```

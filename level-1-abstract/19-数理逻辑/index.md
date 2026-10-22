### 21. 数理逻辑

- 范畴：$\mathbf{Th}$ 理论范畴——对象是一阶理论 $T$，态射是理论间的解释（interpretation）

- **对象例子**：Peano 算术 $\mathrm{PA}$；ZFC 集合论；命题逻辑系统

- **态射例子**：语法解释 $I:T_1\to T_2$（将 $T_1$ 的公式翻译为 $T_2$ 的公式，保持可证性）；Gödel 编码

- **核心函子实例**：模型论函子 $M:\mathbf{Th}^{op}\to\mathbf{Set}$（理论→其模型的集合）；证明函子（命题→证物）

- **Python 示例（命题归结法——自动定理证明）**

```python
# 归结法 (Resolution): 自动定理证明核心算法
def resolve(clause1, clause2):
    """对两个子句做归结消解"""
    resolvents = []
    for lit1 in clause1:
        for lit2 in clause2:
            if lit1 == -lit2:  # 互补文字
                new_clause = (clause1 - {lit1}) | (clause2 - {lit2})
                resolvents.append(frozenset(new_clause))
    return resolvents

# 证明 (¬P ∨ Q) ∧ (P) ∧ (¬Q) 不可满足
clauses = [
    frozenset({-1, 2}),   # ¬P ∨ Q
    frozenset({1}),       # P
    frozenset({-2}),      # ¬Q
]
# 归结推导出空子句 □ = 矛盾
new = resolve(clauses[1], clauses[0])  # {Q}
final = resolve(new[0], clauses[2])    # {□}
print(f"归结到矛盾 {'✓ 不可满足' if frozenset() in final else '未完成'}")
```

```mathematica
(* Mathematica：逻辑与定理证明 *)
(* 命题逻辑真值表 *)
SatisfiableQ[(p || q) && (!p || r) && (!q || !r), {p, q, r}]

(* 一阶逻辑 *)
ForAll[x, Exists[y, x < y]]  (* 在实数中为真 *)

(* Gödel 不完备思想的编码示意 *)
(* 将语句编码为自然数 *)
EncodeFormula[formula_String] := Hash[formula, "SHA256"]
```

### 22. 集合论

- 范畴：$\mathbf{V}$ von Neumann 宇宙——以累积层级 $V_\alpha$ 为对象

- **对象例子**：序数 $\omega$（第一个无穷序数）；基数 $\aleph_1$（第一个不可数基数）

- **态射例子**：力迫扩张 $V\to V[G]$（加入通型滤子 $G$ 获得新模型）

- **核心函子实例**：幂集函子 $\mathcal P:V_\alpha\to V_{\alpha+1}$；连续统函子（基数→可能值域）

- **Python 示例（序数算术与基数运算）**

```python
# 模拟序数与基数运算
class Ordinal:
    """有限序数的 von Neumann 表示"""
    def __init__(self, n):
        self.n = n  # 0=∅, 1={∅}, 2={∅,{∅}}, ...

    def __repr__(self):
        return f"Ordinal({self.n})"

    def successor(self):
        return Ordinal(self.n + 1)

# 基数算术
def cardinal_add(kappa, _lambda):
    """|κ+λ| = max(κ,λ) 对无穷基数"""
    return max(kappa, _lambda)

def cardinal_mul(kappa, _lambda):
    """|κ×λ| = max(κ,λ) 对无穷基数"""
    return max(kappa, _lambda)

omega = Ordinal(float('inf'))  # 第一个无穷序数 ω
print(f"ω的后继 = {omega.successor()}")  # ω+1
print(f"ℵ₀ + ℵ₁ = ℵ{cardinal_add(0, 1)}")
```

```mathematica
(* Mathematica：集合论 *)
(* 序数 *)
OrdinalQ[ω]   (* 检查是否为序数 *)

(* 连续统假设独立于 ZFC *)
(* 不能从 ZFC 公理证明或反驳 *)

(* 力迫法的元数学性质 *)
(* 加法力迫：从 ZFC 一致性证明 ZFC+¬CH 一致性 *)
```

### 23. 模形式

- 范畴：$M_k(\Gamma)$ 权 $k$ 模形式空间（$\Gamma=\mathrm{SL}(2,\mathbb Z)$）

- **对象例子**：Eisenstein 级数 $E_4(\tau)=1+240\sum_{n=1}^\infty\sigma_3(n)q^n$

- **态射例子**：Hecke 算子 $T_n:M_k\to M_k$（模形式空间上的线性算子）

- **核心函子实例**：Mellin 变换函子（模形式→L-函数）；Galois 表示函子（模形式→2 维 Galois 表示）

- **Python 示例（Eisenstein 级数 q-展开）**

```python
def sigma(k, n):
    """除数函数 σ_k(n) = Σ_{d|n} d^k"""
    return sum(d**k for d in range(1, n+1) if n % d == 0)

def eisenstein_series(k, q_terms=10):
    """E_k = 1 + (2k/B_k) Σ σ_{k-1}(n) q^n"""
    from fractions import Fraction
    # Bernoulli numbers for normalization
    B = {4: Fraction(-1, 30), 6: Fraction(1, 42)}
    coeff = Fraction(2*k, B[k]) if k in B else 1
    series = [1]  # constant term
    for n in range(1, q_terms+1):
        series.append(int(coeff) * sigma(k-1, n))
    return series

E4 = eisenstein_series(4, 10)
print(f"E_4 = 1 + {E4[1]}q + {E4[2]}q^2 + {E4[3]}q^3 + ...")
# E_4 = 1 + 240q + 2160q^2 + 6720q^3 + ...
```

```mathematica
(* Mathematica：模形式 *)
(* Eisenstein 级数 *)
E4 = EisensteinE[4, q]
Series[E4, {q, 0, 10}]
(* 1 + 240q + 2160q^2 + 6720q^3 + ... *)

(* Hecke 算子特征值 *)
(* Ramanujan τ 函数 *)
RamanujanTau[1]  (* 1 *)
RamanujanTau[2]  (* -24 *)
RamanujanTau[3]  (* 252 *)

(* j-不变量 *)
KleinInvariantJ[I]  (* 1728 *)
```

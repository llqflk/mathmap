<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 模形式

> 层级 1：抽象结构层 · 分组：概率结构 · 第 21/21 条

[← 集合论](../20-集合论/index.md) · [总目录](../../README.md)

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

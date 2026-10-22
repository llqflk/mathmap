<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 代数数论

> 层级 1：抽象结构层 · 分组：代数几何与数论 · 第 16/21 条

[← 代数几何](../15-代数几何/index.md) · [总目录](../../README.md) · [概率论与随机过程 →](../17-概率论与随机过程/index.md)

- 范畴：$\mathbf{NumFld}$ 数域范畴

- **对象例子**：数域 $K=\mathbb Q(\sqrt{-5})$，整数环 $\mathcal O_K$

- **态射例子**：嵌入 $K\hookrightarrow\mathbb C$；Galois 群作用

- **核心函子实例**：理想类群函子 $\mathrm{Cl}(K)$；Dedekind $\zeta$ 函子

- **Python 示例（数域判别式与分裂）**

```python
import math
def disc_quad(d):
    """二次域Q(√d)的判别式"""
    if d%4==1: return d
    return 4*d

def kronecker(a, n):
    """Kronecker符号，判断p在Q(√d)中分裂"""
    if n==2:
        if a%2==0: return 0
        return 1 if a%8 in (1,7) else -1
    return pow(a, (n-1)//2, n) - n + 1

print(f"Q(√-5)判别式={disc_quad(-5)}")
# 判别式为-20，分裂信息可据此计算
```

```mathematica
(* Mathematica：数域 *)
(* 二次域 Q(√-5) *)
d = -5;
discriminant = If[Mod[d, 4] == 1, d, 4 d]  (* -20 *)

(* Kronecker 符号 *)
KroneckerSymbol[-20, 7]                   (* 判断分裂 *)

(* 数域整数环 *)
ToNumberField[Sqrt[-5]]                    (* AlgebraicNumber *)
```

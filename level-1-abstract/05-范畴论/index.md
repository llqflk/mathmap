<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 范畴论（作为独立学科：高阶结构）

> 层级 1：抽象结构层 · 第 5/21 条

[← 同调代数](../04-同调代数/index.md) · [总目录](../../README.md) · [泛函分析与算子代数 →](../06-泛函分析与算子代数/index.md)

- 范畴：$\mathbf{2Cat}$ 2-范畴的范畴——对象是 2-范畴，态射是 2-函子

- **对象例子**：$\mathbf{Cat}$ 本身是一个 2-范畴——对象 = 小范畴，1-态射 = 函子，2-态射 = 自然变换

- **态射例子**：
  - 垂直合成：$\begin{CD}F\\@VV\alpha V\\G\\@VV\beta V\\H\end{CD}$ = $\beta\cdot\alpha:F\Rightarrow H$（自然变换的自然变换）
  - 水平合成（Whiskering）：$F\circ\alpha:G\circ F\Rightarrow G\circ F'$

- **核心函子实例**：同伦 2-函子 $\Pi_2:\mathbf{Top}\to\mathbf{2Grpd}$（空间→基本 2-群胚）；$\infty$-范畴是 $\mathbf{Cat}$ 的弱化版本，允许结合律只在"同伦意义下"成立

- **Python 示例（Cat 作为 2-范畴：自然变换的垂直与水平合成）**

```python
# Cat 是一个 2-范畴：对象=范畴，1-态射=函子，2-态射=自然变换
# 垂直合成：两个自然变换首尾相接
def vertical_compose(eta, mu):
    """η: F⇒G, μ: G⇒H → μ·η: F⇒H"""
    return lambda x: mu(eta(x))

# 水平合成：函子 × 自然变换
def horizontal_compose(F, eta, G):
    """F: C→D, η: G⇒H (in D), 得 F∘η∘G: F∘G∘G ⇒ F∘H∘G"""
    return lambda x: F(eta(G(x)))

# 实例：在 Set 中
F = lambda x: x + 1       # 函子 F: ℕ→ℕ
G = lambda x: x * 2       # 函子 G: ℕ→ℕ
# η: F ⇒ G 定义为 η_x(x) = x+1 → 2x
eta = lambda x: 2*x       # 自然变换在 x 处的分量 F(x)↦G(x)

# 交换律验证（2-范畴的核心公理）
print(f"η_3: F(3)={F(3)} → G(3)={eta(F(3))}")
# 垂直 + 水平合成满足中间互换律
```

```mathematica
(* Mathematica：2-范畴 Cat *)
(* Cat 是一个 2-范畴 *)
(* 对象 = 范畴 *)
(* 1-态射 = 函子: F: C → D *)
(* 2-态射 = 自然变换: η: F ⇒ G *)

(* 垂直合成：η: F⇒G 与 μ: G⇒H → μ∘η: F⇒H *)
vertical[η_, μ_][x_] := μ[η[x]]

(* 水平合成（Whiskering） *)
whisker[F_, η_, G_][x_] := F[η[G[x]]]

(* 2-范畴公理：中间互换律 *)
(* (μ' ∘ μ) * (η' ∘ η) = (μ' * η') ∘ (μ * η) *)
(* 在 Cat 中，这意味着自然变换的两种合成方式结果一致 *)
```

> **与层级 0.5 的分工**：0.5 是"语法手册"（范畴、函子、自然变换的定义），层级 1 本条是**将这些定义本身作为研究对象**——2-范畴、导出范畴、模型范畴、$\infty$-范畴——它们构成现代数学的"元语言基础设施"。

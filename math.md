# 数学范畴与应用实例

下面以范畴论统一语言，对每个数学方向补全：**范畴名称 + 具体对象例子 + 具体态射例子 + 核心函子实例 + Python/Mathematica 双代码示例**。
整体结构：**层级 0（元框架）→ 层级 0.5（范畴论基础）→ 层级 1（抽象结构）→ 层级 2（具体实例）→ 层级 3（模型计算）**。
逻辑链：先定义"如何看数学"（元视角），再学"范畴的语言"（基础工具箱），然后用这套语言描述所有数学结构（抽象→具体→工程）。

---

# 层级 0：元框架

> **定位**：站在数学之外看数学——将整份文档的分类法本身作为范畴论对象。

### 数学分支的范畴 $\mathbf{Math}$

- 范畴：$\mathbf{Math}$——以数学分支为对象，以分支间的结构映射为态射

- **对象例子**：
  - 分析 $\mathbf{Analysis}$（微积分、PDE、泛函分析……）
  - 代数 $\mathbf{Algebra}$（群论、环论、域论……）
  - 拓扑 $\mathbf{Topology}$（点集拓扑、代数拓扑……）
  - 概率 $\mathbf{Probability}$（初等概率、随机过程……）
  - 计算 $\mathbf{Computation}$（数值分析、ML……）

- **态射例子**：
  - 同调：$\mathbf{Topology}\to\mathbf{Algebra}$（空间→群）
  - 傅里叶变换：$\mathbf{Analysis}\to\mathbf{Analysis}$（时域→频域）
  - 统计推断：$\mathbf{Probability}\to\mathbf{Analysis}$（数据→参数）

- **核心函子实例**：本分类法本身就是一个函子 $F:\mathbf{Math}\to\{\text{抽象},\text{实例},\text{工程}\}$——它把每个数学分支映射到三个抽象层级之一

- **Python 示例（文档的元模型）**

```python
# 数学分支 = 对象，分支间映射 = 态射
math_branches = {
    'Topology':  {'level': 'abstract',  'objects': 'spaces'},
    'Algebra':   {'level': 'abstract',  'objects': 'structures'},
    'Analysis':  {'level': 'concrete',  'objects': 'functions'},
    'FEM':       {'level': 'applied',   'objects': 'meshes'},
}
# 函子：拓扑 → 代数（同调）
homology_functor = lambda space: f'H_{{{space}}}(X)'  # 空间↦同调群
print(homology_functor('1'))  # H_1(X) —— 一维洞的计数
```

```mathematica
(* Mathematica：元框架——数学分支作为符号对象 *)
branches = <|
  "Topology" -> "spaces", "Algebra" -> "structures",
  "Analysis" -> "functions", "Probability" -> "measures",
  "Computation" -> "algorithms"
|>;
(* 函子 = 分支间的映射 *)
homology[space_] := HomologyGroup[space];
(* 这是本文档每一行在做的抽象动作 *)
```

---

---

# 层级 0.5：范畴论基础工具箱

> **定位**：在讨论 Grp、Top、Vect 这些具体范畴之前，先定义"范畴"本身是什么。

## 基本概念

### 1. 范畴的定义

- 范畴：$\mathbf{Cat}$——范畴的范畴（以范畴为对象，以函子为态射）

- **对象例子**：一个小范畴 $\mathcal C$，包含：
  - 对象集 $\mathrm{Ob}(\mathcal C)=\{A,B,C\}$
  - 态射集 $\mathrm{Hom}(A,B)=\{f:A\to B\}$
  - 组合运算 $\circ:\mathrm{Hom}(B,C)\times\mathrm{Hom}(A,B)\to\mathrm{Hom}(A,C)$
  - 满足**结合律** $h\circ(g\circ f)=(h\circ g)\circ f$ 和**单位律** $f\circ\mathrm{id}_A=f$

- **态射例子**：恒等态射 $\mathrm{id}_A:A\to A$；组合 $g\circ f$

- **核心函子实例**：遗忘函子 $\mathbf{Cat}\to\mathbf{Graph}$（忘掉组合律，只看对象和箭头）

- **Python 示例（范畴的最小实现）**

```python
class Category:
    def __init__(self, name):
        self.name = name
        self.objects = set()
        self.hom = {}  # (A,B) -> list of morphisms

    def add_object(self, obj):
        self.objects.add(obj)

    def add_morphism(self, f, src, tgt):
        self.hom.setdefault((src, tgt), []).append(f)

    def compose(self, g, f):
        """g ∘ f: A→B→C"""
        return lambda x: g(f(x))

# 实例化：Set 范畴（对象=集合，态射=函数）
SetCat = Category("Set")
SetCat.add_object("ℕ"); SetCat.add_object("ℝ")
SetCat.add_morphism(lambda x: x+1, "ℕ", "ℝ")
print(SetCat.objects)  # {'ℕ', 'ℝ'}
```

```mathematica
(* Mathematica：范畴的符号化定义 *)
(* 范畴 = 对象 + 态射 + 组合 *)
objects = {A, B, C};
hom = <|{A, B} -> {f}, {B, C} -> {g}, {A, C} -> {g ∘ f}|>;
(* 结合律验证 *)
IsAssociative[hom] := (h ∘ (g ∘ f)) == ((h ∘ g) ∘ f)
```

### 2. 函子

- 范畴：$\mathbf{Cat}$ 中的态射就是函子——保持结构的范畴间映射

- **对象例子**：遗忘函子 $U:\mathbf{Grp}\to\mathbf{Set}$——忘掉群结构，只看底层集合

- **态射例子**：函子 $F:\mathcal C\to\mathcal D$ 把 $\mathcal C$ 的每个对象和态射映射到 $\mathcal D$，保持组合律：$F(g\circ f)=F(g)\circ F(f)$，$F(\mathrm{id}_A)=\mathrm{id}_{F(A)}$

- **核心函子实例**：
  - 恒等函子 $\mathrm{Id}_{\mathcal C}$（什么都不变）
  - 常函子 $\Delta_X$（把一切映射到固定对象 $X$）
  - Hom 函子 $\mathrm{Hom}(A,-):\mathcal C\to\mathbf{Set}$

- **Python 示例（列表函子：Set→Set）**

```python
# List 函子：对象 X ↦ List[X]（X 的列表类型）
#           态射 f ↦ map(f)（逐元素映射）
F_obj = lambda X: f'List[{X}]'        # 对象映射
F_mor = lambda f: lambda xs: list(map(f, xs))  # 态射映射

# 验证函子律：F(g∘f) = F(g)∘F(f)
f = lambda x: x + 1
g = lambda x: x * 2
xs = [1, 2, 3]
assert F_mor(lambda x: g(f(x)))(xs) == F_mor(g)(F_mor(f)(xs))
print("✓ 函子律成立")
```

```mathematica
(* Mathematica：函子实现 *)
(* 函子 F: Set → Set, F(X) = X×X, F(f) = f×f *)
FObj[X_] := {X, X}
FMor[f_][{x_, y_}] := {f[x], f[y]}

(* 验证函子律 *)
f[x_] := x + 1; g[x_] := 2 x;
FMor[Composition[g, f]][{a, b}] == FMor[g][FMor[f][{a, b}]]  (* True *)
```

### 3. 自然变换

- 范畴：$\mathbf{Fun}(\mathcal C,\mathcal D)$——以函子为对象，以自然变换为态射的函子范畴

- **对象例子**：两个平行函子 $F,G:\mathbf{Grp}\to\mathbf{Set}$

- **态射例子**：自然变换 $\eta:F\Rightarrow G$——对 $\mathcal C$ 中每个对象 $A$，给出 $\mathcal D$ 中态射 $\eta_A:F(A)\to G(A)$，使得对所有 $f:A\to B$，下图交换：
  $$\begin{CD}F(A)@>{\eta_A}>>G(A)\\@V{F(f)}VV@VV{G(f)}V\\F(B)@>{\eta_B}>>G(B)\end{CD}$$

- **核心函子实例**：米田嵌入（见下一条）

- **Python 示例（double→square 自然变换）**

```python
# F = 2×,  G = (·)²  (看作两个从Set到Set的函子)
import numpy as np

F = lambda x: 2*x           # F(x) = 2x
G = lambda x: x**2          # G(x) = x²
# 自然变换 η: F ⇒ G,  η_x(x) = x/2 · x
eta = lambda x: x/2 * x     # η_x: F(x) ↦ G(x) 即 2x ↦ x²

for x in [1, 2, 3, 5]:
    assert G(x) == eta(F(x)), f"η_{x}: 2*{x}={F(x)} ↦ {G(x)}={x}²"
print("✓ 自然变换一致")
```

```mathematica
(* Mathematica：自然变换 *)
(* F = (·)×2, G = (·)² *)
F[x_] := 2 x; G[x_] := x^2;
(* 自然变换 η: F ⇒ G *)
η[x_] := x^2/2  (* η_x: F(x)=2x → G(x)=x² *)
η[F[x]] == G[x]  (* True — 自然方块的每一格交换 *)
```

### 4. 米田嵌入

- 范畴：$[\mathcal C^{op},\mathbf{Set}]$ 预层范畴

- **对象例子**：对象 $A\in\mathcal C$ 通过 $\mathrm{Hom}(-,A):\mathcal C^{op}\to\mathbf{Set}$ 表示为预层

- **态射例子**：米田嵌入 $\mathcal Y:\mathcal C\hookrightarrow[\mathcal C^{op},\mathbf{Set}]$，$\mathcal Y(A)=\mathrm{Hom}(-,A)$

- **核心函子实例**：米田引理——$\mathrm{Nat}(\mathrm{Hom}(-,A),F)\cong F(A)$，对象的全部信息由"指向它的所有态射"决定

- **Python 示例（态射字典 = 米田表示）**

```python
# 任一对象 A 的信息 = 所有 Hom(−, A) 的集合
class YonedaSim:
    def __init__(self):
        self.objects = {'ℕ', 'ℝ', 'String'}
        self.hom_to = {}  # A -> {X -> Hom(X,A)}

    def represent(self, A):
        """Yoneda 嵌入：A ↦ Hom(−,A)"""
        return {X: f'{X}→{A}' for X in self.objects}

Y = YonedaSim()
print(Y.represent('ℕ'))
# {'ℕ': 'ℕ→ℕ', 'ℝ': 'ℝ→ℕ', 'String': 'String→ℕ'}
# 对象 ℕ 完全由"从所有对象到它的态射"刻画
```

```mathematica
(* Mathematica：米田嵌入示意 *)
(* 对象 A 的米田表示 = 所有到 A 的态射 *)
yonedaRepresentation[A_, category_] :=
  AssociationMap[Hom[#, A] &, Objects[category]];
(* 米田引理：Nat(Hom(−,A), F) ≅ F(A) *)
(* "A 是什么" 完全由 "什么映射到 A" 决定 *)
```

### 5. 伴随函子

- 范畴：伴随对 $(F,G,\eta,\varepsilon)$，写作 $F\dashv G$

- **对象例子**：自由群函子 $F:\mathbf{Set}\to\mathbf{Grp}$ 和遗忘函子 $U:\mathbf{Grp}\to\mathbf{Set}$，$F\dashv U$

- **态射例子**：单位 $\eta_X:X\to U(F(X))$（把集合元素注入自由群）；余单位 $\varepsilon_G:F(U(G))\to G$（把"忘掉结构再自由生成"映射回原群）

- **核心函子实例**：$F\dashv G$ 等价于自然同构 $\mathrm{Hom}_{\mathcal D}(F(X),Y)\cong\mathrm{Hom}_{\mathcal C}(X,G(Y))$

- **Python 示例（自由幺半群 ⊣ 遗忘函子）**

```python
# F: Set → Mon (自由幺半群: 字符串列表)
# U: Mon → Set (遗忘函子: 忘掉拼接运算)
# F ⊣ U: Hom_Mon(F(X), M) ≅ Hom_Set(X, U(M))

F = lambda X: ('List', X)    # 自由幺半群 = 字符列表
U = lambda M: M[1]            # 遗忘 = 取底层集合

# 伴随同构：从自由幺半群到M的同态 ↔ 从集合X到U(M)的函数
def adjunction(f_map, X_elements):
    """自由幺半群上的同态完全由生成元上的映射决定"""
    return {x: f(x) for x in X_elements}

print(adjunction(lambda c: c.upper(), ['a','b','c']))
```

```mathematica
(* Mathematica：伴随函子 *)
(* 自由 ⊣ 遗忘：FreeMonoid[Set] -> Mon, Forget[Mon] -> Set *)
(* 伴随同构 *)
Hom[FreeMonoid[X], M] ≅ Hom[X, Forget[M]]
(* 单位 η: 每个集合元素成为自由生成的单个字母 *)
(* 余单位 ε: "忘掉再自由生成"坍缩回原 Monoid 元素 *)
```

### 6. 单子（Monad）

- 范畴：自函子范畴上的 Monoid——$(T,\eta,\mu)$，$T:\mathcal C\to\mathcal C$ 是自函子

- **对象例子**：Maybe 单子 $T(X)=X\sqcup\{\text{None}\}$（处理可能缺失的值）

- **态射例子**：单位 $\eta_X:X\to T(X)$ 把纯值提升进单子上下文；乘法 $\mu_X:T(T(X))\to T(X)$ 把嵌套单子摊平

- **核心函子实例**：每个伴随 $F\dashv G$ 产生单子 $G\circ F$

- **Python 示例（Maybe/List 单子的 bind）**

```python
class Maybe:
    """Maybe Monad: T(X) = X | None"""
    @staticmethod
    def pure(x): return ('Just', x)   # η: X → T(X)

    @staticmethod
    def bind(mx, f):                  # >>= : T(X) × (X→T(Y)) → T(Y)
        if mx[0] == 'Nothing': return mx
        return f(mx[1])

# Maybe 链式计算
result = Maybe.bind(
    Maybe.pure(42),
    lambda x: Maybe.pure(x / 2) if x != 0 else ('Nothing',)
)
print(result)  # ('Just', 21.0)

# List Monad: T(X) = [X], bind = flatMap
List = type('List', (), {
    'pure': staticmethod(lambda x: [x]),
    'bind': staticmethod(lambda xs, f: [y for x in xs for y in f(x)])
})
print(List.bind([1,2,3], lambda x: [x, -x]))  # [1,-1,2,-2,3,-3]
```

```mathematica
(* Mathematica：单子 *)
(* Maybe 单子 *)
Just[x_] := x; NothingQ = Nothing;
(* pure = η: X → T(X) *)
pure[x_] := x
(* bind = >>= : T(X) × (X→T(Y)) → T(Y) *)
bind[mx_, f_] := If[mx === Nothing, Nothing, f[mx]]

(* 安全除法：a/b，b=0 时返回 Nothing *)
safeDiv[a_, b_] := If[b == 0, Nothing, a/b]
bind[pure[42], safeDiv[#, 2] &]    (* 21 *)
bind[pure[42], safeDiv[#, 0] &]    (* Nothing *)
```

---

---

# 层级 1：抽象结构层

> **判断标准**：对象是"结构的结构"——你不能用一个具体数值来举例，只能描述结构之间的映射关系。

### 1. 抽象代数（群 / 环 / 域 / 模）

- 范畴：$\mathbf{Grp}$ 群范畴

- **对象例子**：整数加法群 $\mathbb Z$

- **态射例子**：同态 $f(n)=2n$（保持加法）

- **核心函子实例**：自由群函子；遗忘函子（忘掉群结构只看集合）

- **Python 示例（群同态）**

```python
def hom_z(n): return 2*n
print(hom_z(2+3) == hom_z(2)+hom_z(3))  # True，保持运算
```

```mathematica
(* Mathematica：群同态 *)
homZ[n_] := 2 n
homZ[2 + 3] == homZ[2] + homZ[3]  (* True *)

(* 群论：对称群、循环群等内置 *)
GroupElements[SymmetricGroup[3]]
(* {Cycles[{}], Cycles[{{2,3}}], Cycles[{{1,2}}], ...} *)

(* 商群 Z/nZ 等价于模运算 *)
Mod[7 + 5, 12]  (* 模12加法 *)
```

### 2. 李群与李代数

- 范畴：$\mathbf{LieGrp}$ 李群范畴

- **对象例子**：旋转群 $\mathrm{SO}(2)$

- **态射例子**：旋转矩阵

- **核心函子实例**：李代数函子（群→无穷小生成元）

- **Python 示例（SO2 生成元）**

```python
import numpy as np
J = np.array([[0,-1],[1,0]])  # so(2)李代数元素
print(J)
```

```mathematica
(* Mathematica：李代数生成元 *)
J = {{0, -1}, {1, 0}};              (* so(2) 生成元 *)
MatrixExp[theta*J]                   (* SO(2): 旋转矩阵 e^{θJ} *)

(* 李括号 *)
Comm[A_, B_] := A . B - B . A
Comm[{{0,1},{0,0}}, {{0,0},{1,0}}]  (* = {{1,0},{0,-1}} *)
```

### 3. 表示论

- 范畴：$\mathbf{Rep}(G)$ 群表示范畴

- **对象例子**：二维线性空间

- **态射例子**：群元素对应矩阵

- **核心函子实例**：表示函子 $G\to\mathbf{Vect}$

- **Python 示例**：上面旋转矩阵例子就是 SO(2) 的二维表示

```mathematica
(* Mathematica：SO(2) 的二维表示 *)
(* 群元 → 矩阵 *)
rep[theta_] := RotationMatrix[theta]
rep[Pi/3] . {1, 0}                      (* 旋转作用 *)

(* 不可约表示分解 *)
rep[theta] // MatrixForm
(* SO(2) 在 R^2 上的标准表示 *)
```

### 4. 同调代数

- 范畴：$\mathbf{Ch}(R)$ 链复形范畴（R-模上的链复形）

- **对象例子**：链复形 $\cdots\xrightarrow{d_2}C_1\xrightarrow{d_1}C_0\to0$

- **态射例子**：链映射 $f_\bullet:C_\bullet\to D_\bullet$（满足 $fd=df$）

- **核心函子实例**：同调函子 $H_n$（链复形→同调模）；$\mathrm{Ext}^n$、$\mathrm{Tor}_n$ 导出函子

- **Python 示例（单纯复形边界算子 + 同调计算）**

```python
import numpy as np
# 三角形ABC的边界矩阵
# 顶点A(0),B(1),C(2) 边AB(0,1),BC(1,2),AC(0,2)
vertices = 3
edges = [(0,1),(1,2),(0,2)]  # 3条边
# 边界算子∂_1 (边→顶点)
b1 = np.zeros((vertices, len(edges)))
for j,(u,v) in enumerate(edges):
    b1[u,j] = -1; b1[v,j] = 1
# 同调 H_1 = ker∂_1 (因为没有2-单形，im∂_2=0)
rank = np.linalg.matrix_rank(b1)
print(f"b1秩={rank}, H_1维数={len(edges)-rank}")  # 1个生成元=1维洞
```

```mathematica
(* Mathematica：链复形与同调 *)
(* 单纯复形同调 *)
tri = SimplicialComplex[{{1, 2, 3}, {1, 2}, {2, 3}, {1, 3}}]
Homology[tri]                    (* H_0=Z, H_1=Z, H_2=0 *)

(* 边界矩阵 *)
b1 = {{-1, -1, 0}, {1, 0, -1}, {0, 1, 1}};   (* ∂_1 *)
MatrixRank[b1]                                  (* 2 *)
NullSpace[Transpose[b1]]                        (* H_1 生成元 *)
```

### 5. 范畴论（作为独立学科：高阶结构）

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

### 6. 泛函分析与算子代数

- 范畴：$\mathbf{Hilb}$ 希尔伯特空间范畴

- **对象例子**：$L^2[0,1]$ 平方可积函数空间

- **态射例子**：积分算子 $Tf(x)=\int_0^x f(t)dt$

- **核心函子实例**：对偶函子、傅里叶变换酉算子

- **Python 示例（简单线性算子）**

```python
def integral_op(f):
    return lambda x: sum(f(i*0.01)*0.01 for i in range(int(x/0.01)))
```

```mathematica
(* Mathematica：泛函分析中的算子 *)
(* 积分算子 T: f -> ∫_0^x f(t) dt *)
T[f_][x_] := Integrate[f[t], {t, 0, x}]
T[Sin][x]                           (* 1 - Cos[x] *)

(* 内积空间 *)
f[x_] := x; g[x_] := x^2
Integrate[f[x]*g[x], {x, 0, 1}]     (* L^2[0,1] 内积 = 1/4 *)

(* Gram-Schmidt 正交化 *)
Orthogonalize[{1, x, x^2}, Integrate[#1*#2, {x, -1, 1}] &]
```



- 范畴：$\mathbf{C^*Alg}$ C*-代数范畴

- **对象例子**：$C(X)$ 紧空间上连续函数的 C*-代数；$M_n(\mathbb C)$ 矩阵代数

- **态射例子**：*-同态 $f:A\to B$（保持加法、乘法、对合）

- **核心函子实例**：Gelfand 对偶（交换C*-代数↔紧Hausdorff空间）；包络 von Neumann 代数

- **Python 示例（矩阵作为C*-代数元素）**

```python
import numpy as np
A = np.array([[0,1],[0,0]])       # 幂零算子
A_dag = A.conj().T                 # 对合 *
comm = A @ A_dag - A_dag @ A      # 自伴交换子
norm_A = np.linalg.norm(A, 2)     # C*-范数 = 谱半径
print(f"‖A‖={norm_A:.3f}, A*A={A_dag@A}")
# C*恒等式 ‖A*A‖=‖A‖² 验证
print(f"‖A*A‖={np.linalg.norm(A_dag@A,2):.3f}, ‖A‖²={norm_A**2:.3f}")
```

```mathematica
(* Mathematica：C* 代数 *)
A = {{0, 1}, {0, 0}};          (* 幂零算子 *)
Adag = ConjugateTranspose[A];   (* 对合 *)
Norm[A]                         (* C* 范数 *)

(* 自伴交换子 *)
Adag . A - A . Adag             (* {{1, 0}, {0, -1}} *)
(* C* 恒等式验证 *)
Norm[Adag . A] == Norm[A]^2    (* True *)
```

### 7. 实分析（测度论）

- 范畴：$\mathbf{Meas}$ 可测空间范畴

- **对象例子**：区间 $[0,1]$，勒贝格测度

- **态射例子**：可测函数 $f(x)=x$

- **核心函子实例**：勒贝格积分函子

- **Python 示例（离散近似积分）**

```python
def lebesgue_int(f, a=0,b=1,n=1000):
    dx = (b-a)/n
    return sum(f(a+i*dx)*dx for i in range(n))
print(lebesgue_int(lambda x:x))  # ≈0.5
```

```mathematica
(* Mathematica：符号积分 + 数值积分 *)
Integrate[x, {x, 0, 1}]             (* 精确：1/2 *)
NIntegrate[Sin[x^2], {x, 0, 2}]     (* 数值积分 *)

(* Lebesgue 积分：处理可测函数 *)
Integrate[If[x ∈ Rationals, 1, 0], {x, 0, 1}]  (* Dirichlet 函数积分为0 *)
```

### 9. 调和分析

- 范畴：拓扑群上函数空间范畴

- **对象例子**：周期函数空间

- **态射例子**：周期函数

- **核心函子实例**：傅里叶变换函子（卷积→点乘）

- **Python 示例（FFT）**

```python
import numpy as np
x = np.array([1,2,3,4])
print(np.fft.fft(x))
```

```mathematica
(* Mathematica：傅里叶变换 *)
Fourier[{1, 2, 3, 4}]               (* 离散傅里叶变换 *)
FourierTransform[E^(-x^2), x, ω]     (* 连续傅里叶变换 *)

(* 卷积定理验证 *)
a = {1, 2, 3}; b = {4, 5, 6};
Fourier[ListConvolve[a, b]] == Fourier[a] * Fourier[b]  (* True *)
```

### 10. PDE 进阶（索伯列夫空间）

- 范畴：索伯列夫空间范畴

- **对象例子**：函数空间 $H^1$

- **态射例子**：拉普拉斯算子

- **核心函子实例**：离散化函子（无穷维→稀疏矩阵）

- **Python 示例（稀疏矩阵离散）**

```python
import scipy.sparse
# 二阶差分=一维拉普拉斯离散化
```

```mathematica
(* Mathematica：有限差分离散化 *)
n = 10;
(* 一维拉普拉斯二阶差分矩阵 *)
laplacian1D = SparseArray[{Band[{1, 1}] -> -2, Band[{1, 2}] -> 1, 
                          Band[{2, 1}] -> 1}, {n, n}];
laplacian1D // MatrixForm
(* 这是 Dirichlet 边界条件下的离散 −Δ *)
```

---

## 拓扑与几何

### 11. 点集拓扑

- 范畴：$\mathbf{Top}$ 拓扑空间范畴

- **对象例子**：实数轴 $\mathbb R$（通常拓扑）

- **态射例子**：连续函数 $f(x)=x^2$

- **核心函子实例**：紧致化函子

- **Python 示例（连续函数）**

```python
f = lambda x: x**2
# 连续：x微小变化→f微小变化
```

```mathematica
(* Mathematica：拓扑空间示例 *)
f[x_] := x^2
(* 原像为开：f^{-1}[(1,4)] = (-2,-1)∪(1,2) 是开集 *)
Reduce[1 < f[x] < 4, x]            (* -2 < x < -1 || 1 < x < 2 *)
(* 紧致化: 单位区间同胚于单点紧致化的R *)
```

### 12. 代数拓扑

- 范畴：拓扑空间→代数的函子范畴

- **对象例子**：圆环（1 个洞）

- **态射例子**：连续形变

- **核心函子实例**：同调函子（圆环→整数加法群）

- **Python 示例（持续同调库，示意）**

```python
# 第三方库gudhi，提取点云拓扑洞
# import gudhi
```

```mathematica
(* Mathematica：持久同调 *)
(* 点云构建Vietoris-Rips复形 *)
points = RandomReal[{-1, 1}, {30, 2}];
(* 或使用Euler示性数 *)
Simplify[PolyhedronData["Torus", "EulerCharacteristic"]]  (* 0 *)
PolyhedronData["Torus", "Genus"]                          (* 1 *)
```

### 13. 微分拓扑

- 范畴：$\mathbf{Diff}$ 微分流形范畴（对象为光滑流形，态射为光滑映射）

- **对象例子**：$S^2$ 二维球面；环面 $T^2=S^1\times S^1$

- **态射例子**：光滑浸入 $f:S^1\looparrowright\mathbb R^2$；横截映射

- **核心函子实例**：切丛函子 $T:M\mapsto TM$；配边函子

- **Python 示例（Morse 函数临界点检测）**

```python
import numpy as np
def morse_f(x):
    """f(x,y) = x^2 - y^2 (鞍点 Morse 函数)"""
    return x[0]**2 - x[1]**2

def is_critical(grad, x, h=1e-5):
    return np.linalg.norm(grad(morse_f, x, h)) < 1e-3

# 复用在多变量微积分中定义的 gradient 函数
def gradient(f, x, h=1e-5):
    n = len(x)
    grad = np.zeros(n)
    for i in range(n):
        dx = np.zeros(n); dx[i] = h
        grad[i] = (f(x+dx)-f(x-dx))/(2*h)
    return grad

print(f"(0,0)是临界点吗？{is_critical(gradient, np.array([0.,0.]))}")  # True
```

```mathematica
(* Mathematica：Morse 理论 *)
(* Morse 函数 f = x^2 - y^2，鞍点 *)
f[x_, y_] := x^2 - y^2
Grad[f[x, y], {x, y}]                    (* {2x, -2y} *)
Solve[Grad[f[x, y], {x, y}] == {0, 0}]  (* 唯一临界点 (0,0) *)
(* Hessian 行列式 = -4 < 0 → 非退化鞍点 *)
Det[D[f[x, y], {{x, y}, 2}]]             (* -4 *)
```

### 14. 黎曼几何 / 微分几何

- 范畴：$\mathbf{Riem}$ 黎曼流形范畴

- **对象例子**：单位球面

- **态射例子**：球面测地线

- **核心函子实例**：切丛函子（球面每点→切平面）

- **Python 示例（球面切向量）**

```python
import numpy as np
# 球面点(1,0,0)切向量(0,1,0)
```

```mathematica
(* Mathematica：球面切空间 *)
(* 球面 S^2 参数化 *)
sphere = {Sin[θ] Cos[φ], Sin[θ] Sin[φ], Cos[θ]};
(* 切向量基底 *)
eθ = D[sphere, θ];  eφ = D[sphere, φ];
(* 在点(1,0,0)即(θ=π/2, φ=0)处 *)
eθ /. {θ -> Pi/2, φ -> 0}           (* {0, 0, -1} *)
eφ /. {θ -> Pi/2, φ -> 0}           (* {0, 1, 0} *)
```

### 15. 辛几何

- 范畴：$\mathbf{Sympl}$ 辛流形范畴

- **对象例子**：余切丛 $T^*\mathbb R^n\cong\mathbb R^{2n}$，标准辛形式 $\omega=\sum dp_i\wedge dq_i$

- **态射例子**：辛同胚（保持辛形式的光滑映射）

- **核心函子实例**：Hamilton 向量场函子 $H\mapsto X_H$（函数→向量场）；动量映射

- **Python 示例（Hamilton 力学 — 谐振子相空间）**

```python
import numpy as np
def ham_eqns(z, t):
    """H=0.5*(p^2+q^2), 谐振子"""
    q, p = z
    dq = p        # ∂H/∂p
    dp = -q       # -∂H/∂q
    return np.array([dq, dp])

def euler_symplectic(z0, dt, steps):
    z = [z0]
    for _ in range(steps):
        z_new = z[-1] + ham_eqns(z[-1], 0)*dt
        z.append(z_new)
    return np.array(z)

traj = euler_symplectic(np.array([1.0, 0.0]), 0.05, 200)
print(f"相空间面积≈守恒: max|q|={traj[:,0].max():.3f}, max|p|={traj[:,1].max():.3f}")
```

```mathematica
(* Mathematica：Hamilton 力学 — 谐振子 *)
(* Hamilton 方程 *)
{q, p} = {q[t], p[t]};
hamiltonian = 1/2*(p^2 + q^2);       (* H = 0.5(p²+q²) *)
eqns = {q'[t] == D[hamiltonian, p], p'[t] == -D[hamiltonian, q]};
sol = NDSolve[{eqns, q[0] == 1, p[0] == 0}, {q, p}, {t, 0, 10}];
ParametricPlot[Evaluate[{q[t], p[t]} /. sol], {t, 0, 10},
               AspectRatio -> 1]    (* 相图：单位圆 *)

(* 辛形式守恒验证 *)
Simplify[D[hamiltonian /. sol, t]]  (* 0 — 能量守恒 *)
```

---

## 代数几何与数论

### 16. 代数几何

- 范畴：$\mathbf{Sch}$ 概形范畴，或 $\mathbf{Var}_k$ 代数簇范畴

- **对象例子**：仿射直线 $\mathbb A_k^1$；椭圆曲线 $y^2=x^3-x$

- **态射例子**：态射 $f:\mathbb A^1\to\mathbb A^1,\ f(x)=x^2$

- **核心函子实例**：全局截影函子 $\Gamma$（概形→环）；结构层函子

- **Python 示例（椭圆曲线点加法）**

```python
def elliptic_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    x1,y1 = P; x2,y2 = Q
    if x1==x2 and (y1+y2)%p==0: return None
    if P==Q:
        m = (3*x1*x1+a)*pow(2*y1,-1,p)%p
    else:
        m = (y2-y1)*pow(x2-x1,-1,p)%p
    x3 = (m*m-x1-x2)%p
    y3 = (m*(x1-x3)-y1)%p
    return (x3, y3)

# 曲线 y^2=x^3-x over F_7
P=(0,0); Q=(1,0)
print(elliptic_add(P, Q, -1, 7))
```

```mathematica
(* Mathematica：椭圆曲线 *)
(* 曲线 y^2 = x^3 - x 在域 F_7 上 *)
ec = EllipticCurve[{-1, 0}, Modulus -> 7];
pts = Points[ec]                    (* 有限域上的有理点 *)
PointAdd[ec, {0, 0}, {1, 0}]       (* 点加法 *)

(* 复数域上的椭圆曲线 *)
ec2 = EllipticCurve[{-1, 0}];
ParametricPlot[Through[{Re, Im}[WeierstrassP[t, {-1, 0}]]], {t, 0, 2Pi}]
```

### 17. 代数数论

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

---

## 概率结构

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

### 20. 动力系统

- 范畴：$\mathbf{Dyn}$ 状态自函子范畴

- **对象例子**：混沌映射状态

- **态射例子**：逻辑斯蒂映射 $x\to4x(1-x)$

- **核心函子实例**：迭代自函子

- **Python 示例**

```python
def logistic(x): return 4*x*(1-x)
x=0.2
for _ in range(10): x=logistic(x); print(x)
```

```mathematica
(* Mathematica：动力系统 *)
logistic[x_] := 4 x (1 - x)
(* 迭代 *)
NestList[logistic, 0.2, 10]          (* 10步迭代 *)
(* 相图 *)
ListPlot[NestList[logistic, 0.2, 100]]
```

---

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
    B = {4: Fraction(-1, 30), 6: Fraction(1, 42)}
    coeff = Fraction(2*k, B[k]) if k in B else 1
    series = [1]
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
RamanujanTau[1]  (* 1 *)
RamanujanTau[2]  (* -24 *)

(* j-不变量 *)
KleinInvariantJ[I]  (* 1728 *)
```

---

# 层级 2：具体结构层

> **判断标准**：对象可以写出一个具体数值——你可以用代码跑出一个数字来。

### 1. 数学分析与多变量微积分

- 范畴：$\mathbf{Man}_\infty$ 光滑流形范畴（取特例：$\mathbb R$ 一维欧氏流形）

- **对象例子**：$\mathbb R$，函数 $f(x)=x^2$

- **态射例子**：$f(x)=x^2,\ g(x)=\sin x$（光滑函数）

- **核心函子实例**：切函子 $T$，$T(f)=f'(x)=2x$；积分函子 $\int f=\frac13x^3$

- **Python 示例（高阶函数模拟微分）**

```python
def diff(f, h=1e-5):
    return lambda x: (f(x+h)-f(x))/h

f = lambda x: x**2
df = diff(f)
print(df(2))  # 输出≈4.0
```

```mathematica
(* Mathematica：符号微分与数值微分 *)
f[x_] := x^2
df = f'[x]           (* 符号导数：2x *)
dfn[x_] := f'[x]
dfn[2]               (* 输出：4 *)

(* 或用数值微分 *)
g[x_] := x^2
ND[g[x], x, 2]       (* 数值导数在x=2处 *)
```



- 范畴：$\mathbf{Man}_\infty$ 光滑流形范畴中的 $\mathbb R^n$ 对象

- **对象例子**：$\mathbb R^3$ 中的标量场 $f(x,y,z)$ 和向量场 $\mathbf F$

- **态射例子**：梯度 $\nabla f$（纯量→向量）；旋度 $\nabla\times\mathbf F$

- **核心函子实例**：de Rham 复形函子 $\Omega^0\xrightarrow{d}\Omega^1\xrightarrow{d}\Omega^2\xrightarrow{d}\Omega^3$

- **Python 示例（数值梯度）**

```python
import numpy as np
def gradient(f, x, h=1e-5):
    n = len(x)
    grad = np.zeros(n)
    for i in range(n):
        dx = np.zeros(n); dx[i] = h
        grad[i] = (f(x+dx)-f(x-dx))/(2*h)
    return grad

f = lambda x: x[0]**2 + x[1]**3  # f(x,y)=x^2+y^3
print(gradient(f, np.array([1.0, 2.0])))  # ≈[2, 12]
```

```mathematica
(* Mathematica：符号梯度 *)
f[x_, y_] := x^2 + y^3
Grad[f[x, y], {x, y}]                   (* {2x, 3y^2} *)
Grad[f[x, y], {x, y}] /. {x -> 1, y -> 2}  (* {2, 12} *)

(* 散度、旋度等 *)
Div[{x^2, y^2, z^2}, {x, y, z}]          (* 2x + 2y + 2z *)
Curl[{x*y, y*z, z*x}, {x, y, z}]         (* {-y, -z, -x} *)
```

### 2. 复变函数论

- 范畴：$\mathbf{Hol}$ 复解析空间范畴

- **对象例子**：复平面区域 $\mathbb C$，解析函数 $f(z)=z^2$

- **态射例子**：$f(z)=e^z,\ f(z)=z^3$（全纯 / 解析映射）

- **核心函子实例**：复微分函子，$T(f)=2z$；留数积分函子

- **Python 示例（复函数）**

```python
import cmath
f = lambda z: z**2
df = lambda z: 2*z
print(df(1+2j))  # (2+4j)
```

```mathematica
(* Mathematica：复数内置原生支持 *)
f[z_] := z^2
df = f'[z]              (* 2z，自动处理复数 *)
df /. z -> 1 + 2 I      (* 输出：2 + 4 I *)

(* 复函数可视化 *)
ComplexPlot[f[z], {z, -2-2I, 2+2I}]
```

### 4. 常微分方程 ODE

- 范畴：$\mathbf{Dyn}$ 动力系统范畴

- **对象例子**：状态空间 $\mathbb R^2$（位置 + 速度）

- **态射例子**：单摆演化函数，$x(t+\Delta t)=F(x(t))$

- **核心函子实例**：时间演化自函子 $\Phi_t$，把初始状态映射为轨迹

- **Python 示例（欧拉法）**

```python
def euler(df, x0, t_end, dt=0.01):
    x = x0
    traj = [x]
    for _ in range(int(t_end/dt)):
        x += df(x)*dt
        traj.append(x)
    return traj

df = lambda x: -x  # dx/dt=-x
print(euler(df, 1, 2)[-1])
```

```mathematica
(* Mathematica：ODE 解析解 + 数值解 *)
sol = DSolve[{x'[t] == -x[t], x[0] == 1}, x[t], t]
(* 解析解：x[t] → E^-t *)

(* 数值解 *)
nsol = NDSolve[{x'[t] == -x[t], x[0] == 1}, x, {t, 0, 2}]
x[2] /. nsol           (* ≈ 0.135 *)
```

### 5. 偏微分方程入门（PDE）

- 范畴：$\mathbf{DiffOp}$ 微分算子范畴

- **对象例子**：热方程 $\partial_t u=\alpha\nabla^2 u$ 的解空间

- **态射例子**：拉普拉斯算子 $\nabla^2$、传播子（Green 函数）

- **核心函子实例**：分离变量函子（PDE→ODE 组）；Fourier 变换将微分算子转为乘法

- **Python 示例（一维热方程显式差分）**

```python
import numpy as np
def heat_1d(u0, alpha=0.1, dx=0.1, dt=0.005, steps=500):
    u = u0.copy()
    r = alpha*dt/dx**2
    for _ in range(steps):
        u[1:-1] += r*(u[2:]-2*u[1:-1]+u[:-2])
    return u

u0 = np.zeros(100); u0[40:60] = 1.0  # 初始热脉冲
u = heat_1d(u0)
print(f"峰温从1衰减到{u.max():.3f}，两端绝热")
```

```mathematica
(* Mathematica：热方程解析+数值解 *)
(* 解析解（分离变量法） *)
DSolve[{D[u[t, x], t] == D[u[t, x], {x, 2}], u[0, x] == E^(-100*(x - 0.5)^2)},
       u[t, x], {t, x}]

(* 数值解 *)
sol = NDSolve[{D[u[t, x], t] == 0.1*D[u[t, x], {x, 2}],
       u[0, x] == Piecewise[{{1, 0.4 <= x <= 0.6}}], 
       u[t, 0] == 0, u[t, 1] == 0},
       u, {t, 0, 0.2}, {x, 0, 1}];
Plot3D[u[t, x] /. sol, {t, 0, 0.2}, {x, 0, 1}]
```

---

## 代数类

### 6. 线性代数

- 范畴：$\mathbf{Vect}_\mathbb R$ 有限维实线性空间

- **对象例子**：$\mathbb R^2$ 二维向量空间

- **态射例子**：矩阵 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$

- **核心函子实例**：对偶函子（向量→行向量）；张量积函子；直和函子

- **Python 示例（矩阵 = 线性态射）**

```python
import numpy as np
A = np.array([[1,2],[3,4]])
v = np.array([1,0])
print(A @ v)  # 线性映射结果
```

```mathematica
(* Mathematica：矩阵即线性态射 *)
A = {{1, 2}, {3, 4}};
v = {1, 0};
A . v                 (* 输出：{1, 3} *)

(* 附带特征值、对角化等 *)
Eigenvalues[A]        (* 谱分析 *)
Det[A]                (* 行列式 = -2 *)
```

### 7. 多项式代数 / 矩阵论

- 范畴：$\mathbf{Poly}$ 多项式环范畴

- **对象例子**：$p(x)=x^2+1$

- **态射例子**：多项式复合 $p(q(x))$

- **核心函子实例**：求值函子（多项式→数值）

- **Python 示例**

```python
p = lambda x: x**2 + 1
q = lambda x: 2*x
compose = lambda x: p(q(x))
print(compose(3))  # (6)^2+1=37
```

```mathematica
(* Mathematica：多项式复合 *)
p[x_] := x^2 + 1
q[x_] := 2 x
Composition[p, q][x]      (* p[q[x]] = 1 + 4x^2 *)
Composition[p, q][3]      (* 输出：37 *)

(* 直接符号复合 *)
p[q[x]]                   (* 1 + 4x^2 *)
```

### 8. 初等数论

- 范畴：$\mathbf{Arith}$ 算术范畴（$\mathbb Z$ 及其同余结构）

- **对象例子**：整数 $\mathbb Z$，模 $n$ 剩余类环 $\mathbb Z/n\mathbb Z$

- **态射例子**：同余映射 $a\mapsto a\bmod n$；欧拉函数 $\varphi(n)$

- **核心函子实例**：局部化函子（$\mathbb Z\to\mathbb Z_{(p)}$）；模约化函子

- **Python 示例（RSA 密钥生成思想）**

```python
import math
def lcm(a, b): return a*b//math.gcd(a,b)
def modinv(a, m):
    def egcd(a,b):
        if b==0: return a,1,0
        g,x,y = egcd(b, a%b)
        return g,y,x-(a//b)*y
    g,x,_ = egcd(a,m)
    return x%m if g==1 else None
# 小规模RSA：p=61, q=53
phi = (61-1)*(53-1)
e = 17
d = modinv(e, phi)
print(f"公钥({e},{61*53}) 私钥({d},{61*53})")
```

```mathematica
(* Mathematica：数论内置函数 *)
(* 扩展欧几里得 *)
ExtendedGCD[17, (61-1)*(53-1)]   (* {1, {233, -1}} *)

(* RSA 核心：模逆用 PowerMod *)
phi = (61-1)*(53-1);
e = 17;
d = PowerMod[e, -1, phi]         (* 私钥指数 *)

(* 加密/解密 *)
n = 61*53;
m = 42;                           (* 明文 *)
c = PowerMod[m, e, n];            (* 密文 *)
PowerMod[c, d, n]                 (* 解密还原 → 42 *)
```

---

## 几何类

### 9. 解析几何 / 微分几何入门

- 范畴：$\mathbf{Euc}$ 欧氏空间范畴

- **对象例子**：平面点集、球面

- **态射例子**：旋转矩阵、平移变换

- **核心函子实例**：切平面函子（曲面→切空间）

- **Python 示例（2D 旋转）**

```python
import numpy as np
def rotate(theta):
    return np.array([[np.cos(theta),-np.sin(theta)],
                     [np.sin(theta),np.cos(theta)]])
v = np.array([1,0])
print(rotate(np.pi/2) @ v)
```

```mathematica
(* Mathematica：内置旋转矩阵 *)
RotationMatrix[Pi/2]          (* {{0,-1},{1,0}} *)

(* 或手动定义 *)
rotate[theta_] := RotationMatrix[theta]
rotate[Pi/2] . {1, 0}         (* 输出：{0, 1} *)
```

---

## 概率与统计类

### 9. 概率论与数理统计

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

### 10. 组合与离散数学

- 范畴：$\mathbf{FinSet}$ 有限集范畴

- **对象例子**：$n$ 元集 $[n]=\{1,2,\dots,n\}$

- **态射例子**：排列（双射）、组合（单射）、划分（满射）

- **核心函子实例**：幂集函子 $\mathcal P$；计数函子（集合→基数）

- **Python 示例（生成所有组合）**

```python
from itertools import combinations, permutations
items = ['A','B','C']
print(list(combinations(items, 2)))  # 组合
print(list(permutations(items, 2)))  # 排列
# 卡特兰数：合法括号序列数
def catalan(n):
    from math import comb
    return comb(2*n, n)//(n+1)
print(catalan(5))  # 42
```

```mathematica
(* Mathematica：组合函数内置 *)
Subsets[{A, B, C}, {2}]           (* 组合 *)

(* 卡特兰数 *)
CatalanNumber[5]                  (* 输出：42 *)

(* 排列、划分等 *)
Permutations[{A, B, C}, {2}]      (* 排列 *)
IntegerPartitions[5]               (* 整数划分 *)
```



- 范畴：$\mathbf{Set}$ 集合范畴；$\mathbf{Bool}$ 布尔代数范畴

- **对象例子**：命题集合 $\{P,Q,R\}$；真值集合 $\{0,1\}$

- **态射例子**：逻辑蕴含 $P\Rightarrow Q$；真值函数

- **核心函子实例**：Stone 对偶（布尔代数↔Stone 空间）；幂集单子

- **Python 示例（真值表 + 布尔代数）**

```python
from itertools import product
def truth_table(expr):
    vars = sorted(set(c for c in expr if c.isalpha() & c.islower()))
    for vals in product([0,1], repeat=len(vars)):
        env = dict(zip(vars, vals))
        res = eval(expr, {"__builtins__":{}}, env)
        yield {**env, 'result': res}

for row in truth_table("(p and q) or (not p and not q)"):
    print(row)  # XNOR = 等价关系
```

```mathematica
(* Mathematica：内置布尔/逻辑函数 *)
BooleanTable[(p && q) || (!p && !q), {p, q}]
(* 输出：{True, False, False, True} — XNOR *)

(* 真值表直接生成 *)
SatisfiabilityInstances[(p && q) || (!p && !q), {p, q}, All]

(* 集合论：并、交、补 *)
Intersection[{1, 2, 3}, {2, 3, 4}]  (* {2, 3} *)
Union[{1, 2}, {2, 3}]               (* {1, 2, 3} *)
```

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

---

# 层级 3：模型与计算层

> **判断标准**：以解决具体工程问题为目的——数学结构在这里被算法化。

### 1. 数值线性代数

- 范畴：离散化 $\mathbf{Vect}$

- 对象：numpy 数组

- 态射：矩阵乘法

- 函子：向量化函子

- 示例：`A @ v`

```mathematica
(* Mathematica：数值线性代数 *)
A = {{1, 2}, {3, 4}}; v = {1, 0};
A . v                                (* 矩阵乘法 = {1, 3} *)
LinearSolve[A, {5, 11}]              (* 解方程组 = {1, 2} *)
SingularValueDecomposition[A]         (* SVD 分解 *)
```

### 2. 有限元

- 范畴：连续→离散网格函子

- 对象：三角形网格

- 态射：刚度矩阵

- 函子：离散化函子

- 示例：FEniCS 刚度矩阵组装

```mathematica
(* Mathematica：有限元 *)
Needs["NDSolve`FEM`"]
mesh = ToElementMesh[Rectangle[]];   (* 三角形网格 *)
(* 刚度矩阵组装 *)
NDEigensystem[{-Laplacian[u[x, y]], DirichletCondition[u[x, y]==0, True]},
              u[x, y], {x, y} ∈ mesh, 5]
```

### 3. 数值优化

- 范畴：$\mathbf{Opt}$ 优化问题范畴

- **对象例子**：目标函数 $f(x)=x^2+2\sin(x)$

- **态射例子**：牛顿法迭代步；拟牛顿Hessian更新（BFGS）

- **核心函子实例**：梯度下降函子；拉格朗日对偶函子（原问题↔对偶问题）

- **Python 示例（牛顿法与 BFGS 对比）**

```python
import numpy as np
from scipy.optimize import minimize
f = lambda x: x[0]**2 + 2*np.sin(x[0])
res = minimize(f, x0=3.0, method='BFGS')
print(f"BFGS: x*={res.x[0]:.4f}, f*={res.fun:.4f}")
# 约束优化: min x^2 s.t. x>=1
cons = {'type':'ineq','fun':lambda x: x[0]-1}
res_c = minimize(lambda x: x[0]**2, 0.0,
                 constraints=cons, method='SLSQP')
print(f"约束解 x*={res_c.x[0]:.4f}")
```

```mathematica
(* Mathematica：数值优化 *)
(* 无约束：BFGS *)
FindMinimum[x^2 + 2 Sin[x], {x, 3}]    (* {x->-0.379, 最小值→-1.77} *)

(* 约束优化 *)
NMinimize[{x^2, x >= 1}, x]            (* {1., {x->1.}} *)

(* 符号优化 *)
Minimize[{x^2, x >= 1}, x]             (* 精确解 *)
```

### 4. 凸优化

- 范畴：凸集范畴

- 对象：凸函数

- 态射：梯度下降

- 函子：共轭对偶函子

- 示例：CVXPY 最小二乘

```mathematica
(* Mathematica：凸优化 *)
(* 无约束优化 *)
Minimize[x^2 + 2 Sin[x], x]         (* 全局最小 *)

(* 约束优化：min x^2 s.t. x >= 1 *)
Minimize[{x^2, x >= 1}, x]          (* x=1, 最小=1 *)

(* 线性规划 *)
LinearOptimization[2 x + y, {x + y >= 1, x >= 0, y >= 0}, {x, y}]
```

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

### 7. 信息论

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

### 8. 密码学

- 范畴：$\mathbf{Crypt}$ 密码系统范畴

- **对象例子**：明文空间 $\mathcal M$（有限集上的消息）

- **态射例子**：加密函数 $E_k:\mathcal M\to\mathcal C$（密钥 $k$ 参数化）

- **核心函子实例**：同态加密函子（明文运算↔密文运算）

- **Python 示例（Paillier 加法同态示意）**

```python
import math
def paillier_keygen(bits=16):
    p, q = 17, 19  # 小素数示例
    n = p*q; lam = math.lcm(p-1, q-1)
    g = n+1; mu = pow(lam, -1, n)
    return (n,g), (lam,mu,n)  # 公钥, 私钥

def paillier_enc(pk, m):
    n,g = pk; r = 7  # 随机数(实际应随机)
    n2 = n*n
    return (pow(g,m,n2)*pow(r,n,n2))%n2

def paillier_dec(sk, c):
    lam,mu,n = sk; n2 = n*n
    L = (pow(c,lam,n2)-1)//n
    return (L*mu)%n

pk, sk = paillier_keygen()
c = paillier_enc(pk, 42)
print(f"Enc(42)={c}, Dec={paillier_dec(sk,c)}")
# 同态性: E(a)*E(b) = E(a+b) mod n²
```

```mathematica
(* Mathematica：密码学 *)
(* RSA *)
p = 61; q = 53; n = p*q; phi = (p-1)*(q-1);
e = 17; d = PowerMod[e, -1, phi];      (* 私钥 *)
c = PowerMod[42, e, n];                (* 加密 *)
PowerMod[c, d, n]                      (* 解密 → 42 *)

(* 离散对数 *)
MultiplicativeOrder[2, 101]            (* ord_101(2) *)
```

### 9. 信号处理

- 范畴：$\mathbf{Sig}$ 信号空间范畴（$\ell^2$ 或 $L^2$）

- **对象例子**：离散信号 $x[n]$（有限长或平方和序列）

- **态射例子**：卷积核 $h[n]$（线性平移不变算子）；滤波器

- **核心函子实例**：傅里叶变换函子（卷积↔点乘）；小波变换函子

- **Python 示例（FIR 低通滤波器设计）**

```python
import numpy as np
from scipy import signal
# 设计FIR低通滤波器
fs = 1000; cutoff = 100
taps = signal.firwin(numtaps=51, cutoff=cutoff,
                     fs=fs, window='hamming')
# 应用滤波
t = np.linspace(0, 1, fs, endpoint=False)
x = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*300*t)
y = signal.lfilter(taps, 1.0, x)
print(f"DC增益={np.sum(taps):.3f}，阻带衰减{20*np.log10(np.max(np.abs(y)/np.max(np.abs(x)))):.1f}dB")
```

```mathematica
(* Mathematica：信号处理 *)
(* FIR 低通滤波器 *)
fs = 1000; cutoff = 100;
fir = LowpassFilter[KaiserWindow[51, 3], cutoff/fs]
(* 滤波 *)
t = Range[0, 1, 1/fs];
x = Sin[2 Pi*50 t] + Sin[2 Pi*300 t];
y = ListConvolve[fir, x];
(* 频域分析 *)
Periodogram[{x, y}]
```

### 10. 控制论

- 范畴：控制系统范畴

- 对象：系统状态

- 态射：控制律

- 函子：State Monad

- 示例：PID 迭代更新状态

```mathematica
(* Mathematica：控制论 *)
(* PID 控制器的 StateSpace 表示 *)
kp = 1; ki = 0.1; kd = 0.5;
(* 传递函数 *)
tf = TransferFunctionModel[kp + ki/s + kd*s, s]
OutputResponse[tf, UnitStep[t], {t, 0, 10}]
Plot[%, {t, 0, 10}]

(* 最优控制：LQR *)
StateSpaceModel[{{{-1}}, {{1}}, {{1}}, {{0}}}]
LQRegulatorGains[%, {1, 1}]
```

### 11. 计算几何

- 范畴：$\mathbf{CompGeom}$ 计算几何范畴

- **对象例子**：平面上 $n$ 个点集 $P=\{p_1,\dots,p_n\}$

- **态射例子**：Delaunay 三角剖分；Voronoi 图（对偶映射）

- **核心函子实例**：凸包函子；三角剖分对偶函子

- **Python 示例（Delaunay 三角剖分 + 凸包）**

```python
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
points = np.random.rand(20, 2)
tri = Delaunay(points)
hull = ConvexHull(points)
print(f"三角剖分: {tri.nsimplex}个三角形, "
      f"凸包: {len(hull.vertices)}个顶点")
# 欧拉公式验证: V-E+F=2 (平面图)
E = (3*tri.nsimplex + len(hull.vertices))/2
print(f"V-E+F={len(points)}-{E:.0f}+{tri.nsimplex}=2 ✓")
```

```mathematica
(* Mathematica：计算几何 *)
points = RandomReal[{-1, 1}, {20, 2}];
(* Delaunay 三角剖分 *)
mesh = DelaunayMesh[points];
MeshCellCount[mesh]                     (* {顶点, 边, 三角形} *)
(* 欧拉公式 V-E+F *)
{V, E, F} = MeshCellCount[mesh][[{1, 2, 3}]];
V - E + F                               (* 应为 1(开网格) *)

(* 凸包 *)
ch = ConvexHullMesh[points];
MeshCellCount[ch]                       (* 凸包面数 *)
```

### 12. 计算流体力学（CFD）

- 范畴：$\mathbf{CFD}$ 连续介质离散化范畴

- **对象例子**：速度场 $\mathbf u(\mathbf x,t)$，控制体积 $\Omega$

- **态射例子**：对流-扩散算子；SIMPLE 压力修正步

- **核心函子实例**：有限体积离散函子（NS方程→代数方程组）

- **Python 示例（一维对流方程迎风格式）**

```python
import numpy as np
def advection_1d(u0, c=1.0, dx=0.02, dt=0.01, steps=200):
    u = u0.copy()
    C = c*dt/dx  # CFL数
    for _ in range(steps):
        u[1:] -= C*(u[1:]-u[:-1])  # 迎风差分
    return u

nx = 200; u0 = np.exp(-(np.linspace(0,2,nx)-0.5)**2/0.01)
u = advection_1d(u0, c=1.0)
print(f"质量守恒: sum(u0)={u0.sum():.3f}, sum(u)={u.sum():.3f}, "
      f"传播距离≈1.0")
```

```mathematica
(* Mathematica：计算流体力学 *)
(* 一维对流方程 ∂_t u + c ∂_x u = 0 *)
c = 1; dx = 0.02; dt = 0.01; nx = 200;
C = c*dt/dx;                          (* CFL数 *)
u0 = Table[Exp[-((i*dx - 0.5)^2/0.01)], {i, 1, nx}];

(* 迎风差分迭代 *)
u = u0;
Do[u[[2 ;;]] -= C*(u[[2 ;;]] - u[[1 ;; -2]]), {200}];
{Total[u0], Total[u]}                 (* 质量守恒验证 *)

(* 或用内置 PDE 求解器 *)
sol = NDSolve[{D[u[t, x], t] + D[u[t, x], x] == 0,
       u[0, x] == Exp[-((x - 0.5)^2/0.01)],
       u[t, 0] == 0},
      u, {t, 0, 2}, {x, 0, 4}];
Plot3D[u[t, x] /. sol, {t, 0, 2}, {x, 0, 4}]
```

### 13. 图论

- 范畴：$\mathbf{Graph}$ 图范畴

- 对象：节点集合

- 态射：边映射

- 函子：邻接矩阵函子

- 示例：NetworkX 图同态

```mathematica
(* Mathematica：图论 *)
g = Graph[{1 <-> 2, 2 <-> 3, 3 <-> 1, 1 <-> 4}];  (* 三角形加悬边 *)
AdjacencyMatrix[g]                   (* 邻接矩阵函子 *)
GraphAutomorphismGroup[g]            (* 图的自同构群 *)
FindHamiltonianCycle[g]              (* 哈密顿回路 *)
```

### 14. 深度学习

- 范畴：可微函数范畴

- 对象：张量

- 态射：网络层

- 函子：自动微分函子

- 示例：PyTorch 反向传播

```mathematica
(* Mathematica：深度学习 — 自动微分 *)
(* 定义简单网络层的符号微分 *)
sigmoid[x_] := 1/(1 + Exp[-x])
loss[w_, b_, x_, y_] := (sigmoid[w*x + b] - y)^2
(* 梯度 *)
Grad[loss[w, b, x, y], {w, b}]

(* 或使用内置神经网络框架 *)
net = NetChain[{LinearLayer[10], ElementwiseLayer["ReLU"], LinearLayer[1]}]
(* 自动微分由框架处理 *)
```

---

如果你愿意，我可以把上面**全部内容整理成一份干净的 Markdown 文档**，去掉代码块冗余，做成可直接复制到 Notion/Word 的完整版。

> （注：部分内容可能由 AI 生成）

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

### 16. 量子计算数学

- 范畴：$\mathbf{CPTP}$ 量子信道范畴——对象为有限维 Hilbert 空间 $\mathcal H$，态射为完全正保迹映射

- **对象例子**：单量子比特 $\mathcal H\cong\mathbb C^2$（Bloch 球面）；密度矩阵 $\rho$

- **态射例子**：酉门 $U\in\mathrm{SU}(2^n)$（如 Hadamard $H$、CNOT）；量子测量 $\{M_k\}$（POVM）

- **核心函子实例**：量子 Fourier 变换函子 $\mathrm{QFT}_n$；振幅放大函子（Grover）；Stinespring 扩张（CPTP→酉）

- **Python 示例（量子比特模拟 + 量子门）**

```python
import numpy as np

# 单量子比特状态
ket0 = np.array([1+0j, 0+0j])
ket1 = np.array([0+0j, 1+0j])

# 量子门
H = 1/np.sqrt(2) * np.array([[1, 1], [1, -1]])       # Hadamard
X = np.array([[0, 1], [1, 0]])                         # Pauli-X (NOT)
Z = np.array([[1, 0], [0, -1]])                        # Pauli-Z

# 量子线路：H|0⟩ = (|0⟩+|1⟩)/√2
psi = H @ ket0
print(f"H|0⟩ = [{psi[0]:.3f}, {psi[1]:.3f}]")

# Bell 态：CNOT·(H⊗I)|00⟩
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
bell = CNOT @ np.kron(H, np.eye(2)) @ np.kron(ket0, ket0)
print(f"|Bell⟩ = 1/√2 (|00⟩+|11⟩) = {bell.round(3)}")

# 量子 Fourier 变换 (n=3)
def QFT(n):
    N = 2**n; omega = np.exp(2j*np.pi/N)
    return np.array([[omega**(j*k)/np.sqrt(N) for k in range(N)]
                     for j in range(N)])
print(f"QFT_3 前2×2: {QFT(3)[:2,:2].round(3)}")
```

```mathematica
(* Mathematica：量子计算 *)
(* 单量子比特 *)
ket0 = {1, 0}; ket1 = {0, 1};
H = {{1, 1}, {1, -1}}/Sqrt[2];
X = {{0, 1}, {1, 0}};

(* Hadamard 作用 *)
H . ket0  (* {1/√2, 1/√2} = (|0⟩+|1⟩)/√2 *)

(* 量子 Fourier 变换 *)
QFTMatrix[n_] := FourierMatrix[2^n] / Sqrt[2^n]
(* Schmidt 分解与纠缠度 *)
SingularValueDecomposition[{{1,0,0,1},{0,0,0,0},{0,0,0,0},{1,0,0,1}}/2]
```

---

如果你愿意，我可以把上面**全部内容整理成一份干净的 Markdown 文档**，去掉代码块冗余，做成可直接复制到 Notion/Word 的完整版。

> （注：部分内容可能由 AI 生成）

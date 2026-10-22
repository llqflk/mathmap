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

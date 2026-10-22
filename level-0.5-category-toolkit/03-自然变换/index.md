<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 自然变换

> 层级 0.5：范畴论基础工具箱 · 第 3/6 条

[← 函子](../02-函子/index.md) · [总目录](../../README.md) · [米田嵌入 →](../04-米田嵌入/index.md)

- 范畴：$\mathbf{Fun}(\mathcal C,\mathcal D)$——以函子为对象，以自然变换为态射的函子范畴

- **对象例子**：两个平行函子 $F,G:\mathbf{Grp}\to\mathbf{Set}$

- **态射例子**：自然变换 $\eta:F\Rightarrow G$——对 $\mathcal C$ 中每个对象 $A$，给出 $\mathcal D$ 中态射 $\eta_A:F(A)\to G(A)$，使得对所有 $f:A\to B$，下图交换：
  $$\begin{CD}F(A)@>{\eta_A}>>G(A)\\@V{F(f)}VV@VV{G(f)}V\\F(B)@>{\eta_B}>>G(B)\end{CD}$$

- **核心函子实例**：米田嵌入（见下一条）

- **Python 示例（对角线自然变换 $\eta:\mathrm{Id}\Rightarrow(-)\times(-)$）**

```python
# 两个函子 Set → Set：F = Id，G = (·)×(·)
F_mor = lambda f: f                                # F(f) = f
G_mor = lambda f: (lambda p: (f(p[0]), f(p[1])))   # G(f) = f×f

eta = lambda x: (x, x)        # η_X: X → X×X，取对角线
eta_bad = lambda x: (x, x+1)  # 看起来也像自然变换，其实不是

# 自然性：对每个 f: X→Y 都有 G(f)∘η_X = η_Y∘F(f)
for f in (lambda n: n + 1, lambda n: 2 * n, str):
    for x in [0, 1, 2, 7]:
        assert G_mor(f)(eta(x)) == eta(F_mor(f)(x))
print("✓ 对角线 η 是自然的：G(f)∘η_X = η_Y∘F(f)")

# 反例：换一个 f 就能看出 η' 的方块不交换
f = lambda n: 2 * n
print("✗ η' 非自然:", G_mor(f)(eta_bad(1)), "≠", eta_bad(F_mor(f)(1)))  # (2,4) ≠ (2,3)
```

```mathematica
(* Mathematica：自然变换 *)
(* 函子 Set→Set：F = Id，G = (·)×(·) *)
FMor[f_][x_] := f[x];
GMor[f_][{x_, y_}] := {f[x], f[y]};
eta[x_] := {x, x};                  (* η_X: X → X×X，对角线 *)
etaBad[x_] := {x, x + 1};           (* 候选：并不自然 *)

f = Function[n, n + 1];
Table[GMor[f][eta[x]] == eta[FMor[f][x]], {x, {0, 1, 2, 7}}]  (* 全为 True *)

f2 = Function[n, 2 n];
GMor[f2][etaBad[1]] == etaBad[FMor[f2][1]]                    (* False: {2,4} ≠ {2,3} *)
```

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

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

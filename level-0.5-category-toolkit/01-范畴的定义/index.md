<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 范畴的定义

> 层级 0.5：范畴论基础工具箱 · 第 1/6 条

[总目录](../../README.md) · [函子 →](../02-函子/index.md)

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

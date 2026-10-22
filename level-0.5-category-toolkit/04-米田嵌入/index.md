<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 米田嵌入

> 层级 0.5：范畴论基础工具箱 · 第 4/6 条

[← 自然变换](../03-自然变换/index.md) · [总目录](../../README.md) · [伴随函子 →](../05-伴随函子/index.md)

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

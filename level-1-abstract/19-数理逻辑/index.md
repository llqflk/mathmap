<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 数理逻辑

> 层级 1：抽象结构层 · 分组：概率结构 · 第 19/21 条

[← 动力系统](../18-动力系统/index.md) · [总目录](../../README.md) · [集合论 →](../20-集合论/index.md)

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

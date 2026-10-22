<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 组合与离散数学

> 层级 2：具体结构层 · 分组：概率与统计类 · 第 10/11 条

[← 概率论与数理统计](../09-概率论与数理统计/index.md) · [总目录](../../README.md) · [博弈论 →](../11-博弈论/index.md)

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

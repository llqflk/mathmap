<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 集合论

> 层级 1：抽象结构层 · 分组：概率结构 · 第 20/21 条

[← 数理逻辑](../19-数理逻辑/index.md) · [总目录](../../README.md) · [模形式 →](../21-模形式/index.md)

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

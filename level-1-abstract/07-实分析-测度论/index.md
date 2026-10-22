<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 实分析（测度论）

> 层级 1：抽象结构层 · 第 7/21 条

[← 泛函分析与算子代数](../06-泛函分析与算子代数/index.md) · [总目录](../../README.md) · [调和分析 →](../08-调和分析/index.md)

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

<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 多项式代数 / 矩阵论

> 层级 2：具体结构层 · 分组：代数类 · 第 6/11 条

[← 线性代数](../05-线性代数/index.md) · [总目录](../../README.md) · [初等数论 →](../07-初等数论/index.md)

- 范畴：$\mathbf{Poly}$ 多项式环范畴

- **对象例子**：$p(x)=x^2+1$

- **态射例子**：多项式复合 $p(q(x))$

- **核心函子实例**：求值函子（多项式→数值）

- **Python 示例**

```python
p = lambda x: x**2 + 1
q = lambda x: 2*x
compose = lambda x: p(q(x))
print(compose(3))  # (6)^2+1=37
```

```mathematica
(* Mathematica：多项式复合 *)
p[x_] := x^2 + 1
q[x_] := 2 x
Composition[p, q][x]      (* p[q[x]] = 1 + 4x^2 *)
Composition[p, q][3]      (* 输出：37 *)

(* 直接符号复合 *)
p[q[x]]                   (* 1 + 4x^2 *)
```

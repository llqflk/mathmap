### 7. 多项式代数 / 矩阵论

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

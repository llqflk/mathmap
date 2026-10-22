### 1. 抽象代数（群 / 环 / 域 / 模）

- 范畴：$\mathbf{Grp}$ 群范畴

- **对象例子**：整数加法群 $\mathbb Z$

- **态射例子**：同态 $f(n)=2n$（保持加法）

- **核心函子实例**：自由群函子；遗忘函子（忘掉群结构只看集合）

- **Python 示例（群同态）**

```python
def hom_z(n): return 2*n
print(hom_z(2+3) == hom_z(2)+hom_z(3))  # True，保持运算
```

```mathematica
(* Mathematica：群同态 *)
homZ[n_] := 2 n
homZ[2 + 3] == homZ[2] + homZ[3]  (* True *)

(* 群论：对称群、循环群等内置 *)
GroupElements[SymmetricGroup[3]]
(* {Cycles[{}], Cycles[{{2,3}}], Cycles[{{1,2}}], ...} *)

(* 商群 Z/nZ 等价于模运算 *)
Mod[7 + 5, 12]  (* 模12加法 *)
```

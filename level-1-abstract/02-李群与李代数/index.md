<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 李群与李代数

> 层级 1：抽象结构层 · 第 2/21 条

[← 抽象代数（群 / 环 / 域 / 模）](../01-抽象代数/index.md) · [总目录](../../README.md) · [表示论 →](../03-表示论/index.md)

- 范畴：$\mathbf{LieGrp}$ 李群范畴

- **对象例子**：旋转群 $\mathrm{SO}(2)$

- **态射例子**：旋转矩阵

- **核心函子实例**：李代数函子（群→无穷小生成元）

- **Python 示例（SO2 生成元）**

```python
import numpy as np
J = np.array([[0,-1],[1,0]])  # so(2)李代数元素
print(J)
```

```mathematica
(* Mathematica：李代数生成元 *)
J = {{0, -1}, {1, 0}};              (* so(2) 生成元 *)
MatrixExp[theta*J]                   (* SO(2): 旋转矩阵 e^{θJ} *)

(* 李括号 *)
Comm[A_, B_] := A . B - B . A
Comm[{{0,1},{0,0}}, {{0,0},{1,0}}]  (* = {{1,0},{0,-1}} *)
```

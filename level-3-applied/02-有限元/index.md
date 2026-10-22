### 2. 有限元

- 范畴：连续→离散网格函子

- 对象：三角形网格

- 态射：刚度矩阵

- 函子：离散化函子

- 示例：FEniCS 刚度矩阵组装

```mathematica
(* Mathematica：有限元 *)
Needs["NDSolve`FEM`"]
mesh = ToElementMesh[Rectangle[]];   (* 三角形网格 *)
(* 刚度矩阵组装 *)
NDEigensystem[{-Laplacian[u[x, y]], DirichletCondition[u[x, y]==0, True]},
              u[x, y], {x, y} ∈ mesh, 5]
```

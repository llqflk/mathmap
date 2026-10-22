### 1. 数值线性代数

- 范畴：离散化 $\mathbf{Vect}$

- 对象：numpy 数组

- 态射：矩阵乘法

- 函子：向量化函子

- 示例：`A @ v`

```mathematica
(* Mathematica：数值线性代数 *)
A = {{1, 2}, {3, 4}}; v = {1, 0};
A . v                                (* 矩阵乘法 = {1, 3} *)
LinearSolve[A, {5, 11}]              (* 解方程组 = {1, 2} *)
SingularValueDecomposition[A]         (* SVD 分解 *)
```

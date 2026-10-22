<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# PDE 进阶（索伯列夫空间）

> 层级 1：抽象结构层 · 第 9/21 条

[← 调和分析](../08-调和分析/index.md) · [总目录](../../README.md) · [点集拓扑 →](../10-点集拓扑/index.md)

- 范畴：索伯列夫空间范畴

- **对象例子**：函数空间 $H^1$

- **态射例子**：拉普拉斯算子

- **核心函子实例**：离散化函子（无穷维→稀疏矩阵）

- **Python 示例（稀疏矩阵离散）**

```python
import scipy.sparse
# 二阶差分=一维拉普拉斯离散化
```

```mathematica
(* Mathematica：有限差分离散化 *)
n = 10;
(* 一维拉普拉斯二阶差分矩阵 *)
laplacian1D = SparseArray[{Band[{1, 1}] -> -2, Band[{1, 2}] -> 1, 
                          Band[{2, 1}] -> 1}, {n, n}];
laplacian1D // MatrixForm
(* 这是 Dirichlet 边界条件下的离散 −Δ *)
```

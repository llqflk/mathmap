### 4. 同调代数

- 范畴：$\mathbf{Ch}(R)$ 链复形范畴（R-模上的链复形）

- **对象例子**：链复形 $\cdots\xrightarrow{d_2}C_1\xrightarrow{d_1}C_0\to0$

- **态射例子**：链映射 $f_\bullet:C_\bullet\to D_\bullet$（满足 $fd=df$）

- **核心函子实例**：同调函子 $H_n$（链复形→同调模）；$\mathrm{Ext}^n$、$\mathrm{Tor}_n$ 导出函子

- **Python 示例（单纯复形边界算子 + 同调计算）**

```python
import numpy as np
# 三角形ABC的边界矩阵
# 顶点A(0),B(1),C(2) 边AB(0,1),BC(1,2),AC(0,2)
vertices = 3
edges = [(0,1),(1,2),(0,2)]  # 3条边
# 边界算子∂_1 (边→顶点)
b1 = np.zeros((vertices, len(edges)))
for j,(u,v) in enumerate(edges):
    b1[u,j] = -1; b1[v,j] = 1
# 同调 H_1 = ker∂_1 (因为没有2-单形，im∂_2=0)
rank = np.linalg.matrix_rank(b1)
print(f"b1秩={rank}, H_1维数={len(edges)-rank}")  # 1个生成元=1维洞
```

```mathematica
(* Mathematica：链复形与同调 *)
(* 单纯复形同调 *)
tri = SimplicialComplex[{{1, 2, 3}, {1, 2}, {2, 3}, {1, 3}}]
Homology[tri]                    (* H_0=Z, H_1=Z, H_2=0 *)

(* 边界矩阵 *)
b1 = {{-1, -1, 0}, {1, 0, -1}, {0, 1, 1}};   (* ∂_1 *)
MatrixRank[b1]                                  (* 2 *)
NullSpace[Transpose[b1]]                        (* H_1 生成元 *)
```

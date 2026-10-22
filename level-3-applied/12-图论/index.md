### 13. 图论

- 范畴：$\mathbf{Graph}$ 图范畴

- 对象：节点集合

- 态射：边映射

- 函子：邻接矩阵函子

- 示例：NetworkX 图同态

```mathematica
(* Mathematica：图论 *)
g = Graph[{1 <-> 2, 2 <-> 3, 3 <-> 1, 1 <-> 4}];  (* 三角形加悬边 *)
AdjacencyMatrix[g]                   (* 邻接矩阵函子 *)
GraphAutomorphismGroup[g]            (* 图的自同构群 *)
FindHamiltonianCycle[g]              (* 哈密顿回路 *)
```

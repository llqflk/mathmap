### 4. 凸优化

- 范畴：凸集范畴

- 对象：凸函数

- 态射：梯度下降

- 函子：共轭对偶函子

- 示例：CVXPY 最小二乘

```mathematica
(* Mathematica：凸优化 *)
(* 无约束优化 *)
Minimize[x^2 + 2 Sin[x], x]         (* 全局最小 *)

(* 约束优化：min x^2 s.t. x >= 1 *)
Minimize[{x^2, x >= 1}, x]          (* x=1, 最小=1 *)

(* 线性规划 *)
LinearOptimization[2 x + y, {x + y >= 1, x >= 0, y >= 0}, {x, y}]
```

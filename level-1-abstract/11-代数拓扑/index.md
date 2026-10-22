### 12. 代数拓扑

- 范畴：拓扑空间→代数的函子范畴

- **对象例子**：圆环（1 个洞）

- **态射例子**：连续形变

- **核心函子实例**：同调函子（圆环→整数加法群）

- **Python 示例（持续同调库，示意）**

```python
# 第三方库gudhi，提取点云拓扑洞
# import gudhi
```

```mathematica
(* Mathematica：持久同调 *)
(* 点云构建Vietoris-Rips复形 *)
points = RandomReal[{-1, 1}, {30, 2}];
(* 或使用Euler示性数 *)
Simplify[PolyhedronData["Torus", "EulerCharacteristic"]]  (* 0 *)
PolyhedronData["Torus", "Genus"]                          (* 1 *)
```

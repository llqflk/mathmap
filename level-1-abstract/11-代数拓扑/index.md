<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 代数拓扑

> 层级 1：抽象结构层 · 分组：拓扑与几何 · 第 11/21 条

[← 点集拓扑](../10-点集拓扑/index.md) · [总目录](../../README.md) · [微分拓扑 →](../12-微分拓扑/index.md)

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

<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 解析几何 / 微分几何入门

> 层级 2：具体结构层 · 分组：几何类 · 第 8/11 条

[← 初等数论](../07-初等数论/index.md) · [总目录](../../README.md) · [概率论与数理统计 →](../09-概率论与数理统计/index.md)

- 范畴：$\mathbf{Euc}$ 欧氏空间范畴

- **对象例子**：平面点集、球面

- **态射例子**：旋转矩阵、平移变换

- **核心函子实例**：切平面函子（曲面→切空间）

- **Python 示例（2D 旋转）**

```python
import numpy as np
def rotate(theta):
    return np.array([[np.cos(theta),-np.sin(theta)],
                     [np.sin(theta),np.cos(theta)]])
v = np.array([1,0])
print(rotate(np.pi/2) @ v)
```

```mathematica
(* Mathematica：内置旋转矩阵 *)
RotationMatrix[Pi/2]          (* {{0,-1},{1,0}} *)

(* 或手动定义 *)
rotate[theta_] := RotationMatrix[theta]
rotate[Pi/2] . {1, 0}         (* 输出：{0, 1} *)
```

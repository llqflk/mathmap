<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 调和分析

> 层级 1：抽象结构层 · 第 8/21 条

[← 实分析（测度论）](../07-实分析-测度论/index.md) · [总目录](../../README.md) · [PDE 进阶（索伯列夫空间） →](../09-PDE进阶/index.md)

- 范畴：拓扑群上函数空间范畴

- **对象例子**：周期函数空间

- **态射例子**：周期函数

- **核心函子实例**：傅里叶变换函子（卷积→点乘）

- **Python 示例（FFT）**

```python
import numpy as np
x = np.array([1,2,3,4])
print(np.fft.fft(x))
```

```mathematica
(* Mathematica：傅里叶变换 *)
Fourier[{1, 2, 3, 4}]               (* 离散傅里叶变换 *)
FourierTransform[E^(-x^2), x, ω]     (* 连续傅里叶变换 *)

(* 卷积定理验证 *)
a = {1, 2, 3}; b = {4, 5, 6};
Fourier[ListConvolve[a, b]] == Fourier[a] * Fourier[b]  (* True *)
```

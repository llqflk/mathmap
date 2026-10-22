<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 信号处理

> 层级 3：模型与计算层 · 第 8/15 条

[← 密码学](../07-密码学/index.md) · [总目录](../../README.md) · [控制论 →](../09-控制论/index.md)

- 范畴：$\mathbf{Sig}$ 信号空间范畴（$\ell^2$ 或 $L^2$）

- **对象例子**：离散信号 $x[n]$（有限长或平方和序列）

- **态射例子**：卷积核 $h[n]$（线性平移不变算子）；滤波器

- **核心函子实例**：傅里叶变换函子（卷积↔点乘）；小波变换函子

- **Python 示例（FIR 低通滤波器设计）**

```python
import numpy as np
from scipy import signal
# 设计FIR低通滤波器
fs = 1000; cutoff = 100
taps = signal.firwin(numtaps=51, cutoff=cutoff,
                     fs=fs, window='hamming')
# 应用滤波
t = np.linspace(0, 1, fs, endpoint=False)
x = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*300*t)
y = signal.lfilter(taps, 1.0, x)
print(f"DC增益={np.sum(taps):.3f}，阻带衰减{20*np.log10(np.max(np.abs(y)/np.max(np.abs(x)))):.1f}dB")
```

```mathematica
(* Mathematica：信号处理 *)
(* FIR 低通滤波器 *)
fs = 1000; cutoff = 100;
fir = LowpassFilter[KaiserWindow[51, 3], cutoff/fs]
(* 滤波 *)
t = Range[0, 1, 1/fs];
x = Sin[2 Pi*50 t] + Sin[2 Pi*300 t];
y = ListConvolve[fir, x];
(* 频域分析 *)
Periodogram[{x, y}]
```

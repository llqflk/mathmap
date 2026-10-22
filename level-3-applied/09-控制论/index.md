<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 控制论

> 层级 3：模型与计算层 · 第 9/15 条

[← 信号处理](../08-信号处理/index.md) · [总目录](../../README.md) · [计算几何 →](../10-计算几何/index.md)

- 范畴：$\mathbf{Sys}$ 线性系统范畴——对象是 LTI 系统 $(A,B,C,D)$，态射是系统互连（串联、反馈）

- **对象例子**：双积分器 $\dot x=Ax+Bu$，$A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，$B=\begin{pmatrix}0\\1\end{pmatrix}$

- **态射例子**：状态反馈 $u=-Kx$（把 $(A,B)$ 变成闭环 $A-BK$）

- **核心函子实例**：能控性函子（系统→能控子空间 $\mathrm{im}[B\ \ AB]$）；极点配置函子（期望谱→增益 $K$）

- **Python 示例（Ackermann 极点配置）**

```python
import numpy as np
A = np.array([[0., 1.], [0., 0.]])          # 双积分器 x'' = u
B = np.array([[0.], [1.]])
poles = [-1.0, -2.0]                        # 期望闭环极点

C = np.hstack([B, A @ B])                   # 能控性矩阵
phi = np.eye(2)
for lam in poles:                           # φ(A) = Π(A - λI)
    phi = phi @ (A - lam * np.eye(2))
K = np.array([0., 1.]) @ np.linalg.inv(C) @ phi   # Ackermann 公式

print("反馈增益 K =", np.round(K, 4))
print("闭环谱 =", np.round(np.sort(np.linalg.eigvals(A - B @ K.reshape(1, -1))), 4))
```

```mathematica
(* Mathematica：控制论 *)
(* PID 控制器的 StateSpace 表示 *)
kp = 1; ki = 0.1; kd = 0.5;
(* 传递函数 *)
tf = TransferFunctionModel[kp + ki/s + kd*s, s]
OutputResponse[tf, UnitStep[t], {t, 0, 10}]
Plot[%, {t, 0, 10}]

(* 最优控制：LQR *)
StateSpaceModel[{{{-1}}, {{1}}, {{1}}, {{0}}}]
LQRegulatorGains[%, {1, 1}]
```

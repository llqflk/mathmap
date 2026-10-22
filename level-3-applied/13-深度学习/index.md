<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 深度学习

> 层级 3：模型与计算层 · 第 13/15 条

[← 图论](../12-图论/index.md) · [总目录](../../README.md) · [金融数学 →](../14-金融数学/index.md)

- 范畴：$\mathbf{Smooth}$ 可微映射范畴——对象是 $\mathbb R^n$（张量空间），态射是可微映射

- **对象例子**：XOR 的四个输入点 $\{(0,0),(0,1),(1,0),(1,1)\}\subset\mathbb R^2$

- **态射例子**：两层 MLP $f_\theta:\mathbb R^2\to(0,1)$（仿射 + sigmoid 复合）；损失 $L=\frac1N\sum(f_\theta(x_i)-y_i)^2$

- **核心函子实例**：切函子 $T$（可微映射↦其导数）；反向传播 = $T$ 在计算图上的反向复合

- **Python 示例（手写反向传播 + 梯度校验 + 训练 XOR）**

```python
import numpy as np
rng = np.random.default_rng(0)
X = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = np.array([[0., 1., 1., 0.]]).T          # XOR
sig = lambda z: 1 / (1 + np.exp(-z))

W1 = rng.normal(0, 1, (2, 4)); b1 = np.zeros((1, 4))
W2 = rng.normal(0, 1, (4, 1)); b2 = np.zeros((1, 1))
params = [W1, b1, W2, b2]

def forward():
    h = sig(X @ W1 + b1)                    # 隐层把 4 个点摊开
    return h, sig(h @ W2 + b2)

def loss():
    _, o = forward()
    return float(np.mean((o - y) ** 2))

def grads():                                # 反向传播：链式法则逐层回传
    h, o = forward()
    d2 = 2 * (o - y) / y.size * o * (1 - o)
    d1 = (d2 @ W2.T) * h * (1 - h)
    return [X.T @ d1, d1.sum(0, keepdims=True), h.T @ d2, d2.sum(0, keepdims=True)]

# 梯度校验：解析梯度 vs 中心差分
g = grads(); eps = 1e-6
W1[0, 0] += eps; lp = loss()
W1[0, 0] -= 2 * eps; lm = loss()
W1[0, 0] += eps
print("梯度校验: 解析 =", f"{g[0][0, 0]:+.6f}", " 差分 =", f"{(lp - lm) / (2 * eps):+.6f}")

for _ in range(20000):                      # 全批梯度下降
    for p, gi in zip(params, grads()):
        p -= 0.5 * gi
_, o = forward()
print("训练后 loss =", f"{loss():.5f}")
print("预测 =", np.round(o.ravel(), 3), "目标 =", y.ravel().astype(int))
```

```mathematica
(* Mathematica：深度学习 — 自动微分 *)
(* 定义简单网络层的符号微分 *)
sigmoid[x_] := 1/(1 + Exp[-x])
loss[w_, b_, x_, y_] := (sigmoid[w*x + b] - y)^2
(* 梯度 *)
Grad[loss[w, b, x, y], {w, b}]

(* 或使用内置神经网络框架 *)
net = NetChain[{LinearLayer[10], ElementwiseLayer["ReLU"], LinearLayer[1]}]
(* 自动微分由框架处理 *)
```

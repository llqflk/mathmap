### 14. 深度学习

- 范畴：可微函数范畴

- 对象：张量

- 态射：网络层

- 函子：自动微分函子

- 示例：PyTorch 反向传播

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

---

如果你愿意，我可以把上面**全部内容整理成一份干净的 Markdown 文档**，去掉代码块冗余，做成可直接复制到 Notion/Word 的完整版。

> （注：部分内容可能由 AI 生成）

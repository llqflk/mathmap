### 13. 微分拓扑

- 范畴：$\mathbf{Diff}$ 微分流形范畴（对象为光滑流形，态射为光滑映射）

- **对象例子**：$S^2$ 二维球面；环面 $T^2=S^1\times S^1$

- **态射例子**：光滑浸入 $f:S^1\looparrowright\mathbb R^2$；横截映射

- **核心函子实例**：切丛函子 $T:M\mapsto TM$；配边函子

- **Python 示例（Morse 函数临界点检测）**

```python
import numpy as np
def morse_f(x):
    """f(x,y) = x^2 - y^2 (鞍点 Morse 函数)"""
    return x[0]**2 - x[1]**2

def is_critical(grad, x, h=1e-5):
    return np.linalg.norm(grad(morse_f, x, h)) < 1e-3

# 复用在多变量微积分中定义的 gradient 函数
def gradient(f, x, h=1e-5):
    n = len(x)
    grad = np.zeros(n)
    for i in range(n):
        dx = np.zeros(n); dx[i] = h
        grad[i] = (f(x+dx)-f(x-dx))/(2*h)
    return grad

print(f"(0,0)是临界点吗？{is_critical(gradient, np.array([0.,0.]))}")  # True
```

```mathematica
(* Mathematica：Morse 理论 *)
(* Morse 函数 f = x^2 - y^2，鞍点 *)
f[x_, y_] := x^2 - y^2
Grad[f[x, y], {x, y}]                    (* {2x, -2y} *)
Solve[Grad[f[x, y], {x, y}] == {0, 0}]  (* 唯一临界点 (0,0) *)
(* Hessian 行列式 = -4 < 0 → 非退化鞍点 *)
Det[D[f[x, y], {{x, y}, 2}]]             (* -4 *)
```

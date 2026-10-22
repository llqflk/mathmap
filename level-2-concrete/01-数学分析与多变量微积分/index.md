<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 数学分析与多变量微积分

> 层级 2：具体结构层 · 第 1/11 条

[总目录](../../README.md) · [复变函数论 →](../02-复变函数论/index.md)

- 范畴：$\mathbf{Man}_\infty$ 光滑流形范畴（取特例：$\mathbb R$ 一维欧氏流形）

- **对象例子**：$\mathbb R$，函数 $f(x)=x^2$

- **态射例子**：$f(x)=x^2,\ g(x)=\sin x$（光滑函数）

- **核心函子实例**：切函子 $T$，$T(f)=f'(x)=2x$；积分函子 $\int f=\frac13x^3$

- **Python 示例（高阶函数模拟微分）**

```python
def diff(f, h=1e-5):
    return lambda x: (f(x+h)-f(x))/h

f = lambda x: x**2
df = diff(f)
print(df(2))  # 输出≈4.0
```

```mathematica
(* Mathematica：符号微分与数值微分 *)
f[x_] := x^2
df = f'[x]           (* 符号导数：2x *)
dfn[x_] := f'[x]
dfn[2]               (* 输出：4 *)

(* 或用数值微分 *)
g[x_] := x^2
ND[g[x], x, 2]       (* 数值导数在x=2处 *)
```



- 范畴：$\mathbf{Man}_\infty$ 光滑流形范畴中的 $\mathbb R^n$ 对象

- **对象例子**：$\mathbb R^3$ 中的标量场 $f(x,y,z)$ 和向量场 $\mathbf F$

- **态射例子**：梯度 $\nabla f$（纯量→向量）；旋度 $\nabla\times\mathbf F$

- **核心函子实例**：de Rham 复形函子 $\Omega^0\xrightarrow{d}\Omega^1\xrightarrow{d}\Omega^2\xrightarrow{d}\Omega^3$

- **Python 示例（数值梯度）**

```python
import numpy as np
def gradient(f, x, h=1e-5):
    n = len(x)
    grad = np.zeros(n)
    for i in range(n):
        dx = np.zeros(n); dx[i] = h
        grad[i] = (f(x+dx)-f(x-dx))/(2*h)
    return grad

f = lambda x: x[0]**2 + x[1]**3  # f(x,y)=x^2+y^3
print(gradient(f, np.array([1.0, 2.0])))  # ≈[2, 12]
```

```mathematica
(* Mathematica：符号梯度 *)
f[x_, y_] := x^2 + y^3
Grad[f[x, y], {x, y}]                   (* {2x, 3y^2} *)
Grad[f[x, y], {x, y}] /. {x -> 1, y -> 2}  (* {2, 12} *)

(* 散度、旋度等 *)
Div[{x^2, y^2, z^2}, {x, y, z}]          (* 2x + 2y + 2z *)
Curl[{x*y, y*z, z*x}, {x, y, z}]         (* {-y, -z, -x} *)
```

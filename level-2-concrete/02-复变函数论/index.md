### 2. 复变函数论

- 范畴：$\mathbf{Hol}$ 复解析空间范畴

- **对象例子**：复平面区域 $\mathbb C$，解析函数 $f(z)=z^2$

- **态射例子**：$f(z)=e^z,\ f(z)=z^3$（全纯 / 解析映射）

- **核心函子实例**：复微分函子，$T(f)=2z$；留数积分函子

- **Python 示例（复函数）**

```python
import cmath
f = lambda z: z**2
df = lambda z: 2*z
print(df(1+2j))  # (2+4j)
```

```mathematica
(* Mathematica：复数内置原生支持 *)
f[z_] := z^2
df = f'[z]              (* 2z，自动处理复数 *)
df /. z -> 1 + 2 I      (* 输出：2 + 4 I *)

(* 复函数可视化 *)
ComplexPlot[f[z], {z, -2-2I, 2+2I}]
```

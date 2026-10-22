<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 表示论

> 层级 1：抽象结构层 · 第 3/21 条

[← 李群与李代数](../02-李群与李代数/index.md) · [总目录](../../README.md) · [同调代数 →](../04-同调代数/index.md)

- 范畴：$\mathbf{Rep}(G)$ 群表示范畴——对象是 $G$-模（带群作用的向量空间），态射是 $G$-等变线性映射

- **对象例子**：$\mathrm{SO}(2)$ 在 $\mathbb R^2$ 上的标准表示 $(\mathbb R^2,\rho)$

- **态射例子**：$g\mapsto\rho(g)$（群元映成矩阵）；等变映射 $T\rho(g)=\rho'(g)T$

- **核心函子实例**：表示函子 $\rho:G\to\mathbf{Vect}$；特征标函子 $\chi_\rho(g)=\mathrm{tr}\,\rho(g)$

- **Python 示例（SO(2) 二维表示 + 同态性检验）**

```python
import numpy as np
def rep(theta):                       # ρ: SO(2) → GL(2, ℝ)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])

a, b = 0.7, 1.3
print("同态性 ρ(a+b)=ρ(a)ρ(b):", np.allclose(rep(a + b), rep(a) @ rep(b)))
print("正交性 ρᵀρ=I:", np.allclose(rep(a).T @ rep(a), np.eye(2)))
print("行列式恒为 1:", round(float(np.linalg.det(rep(a))), 12))
```

```mathematica
(* Mathematica：SO(2) 的二维表示 *)
(* 群元 → 矩阵 *)
rep[theta_] := RotationMatrix[theta]
rep[Pi/3] . {1, 0}                      (* 旋转作用 *)

(* 同态性：ρ(a)·ρ(b) = ρ(a+b) *)
Chop[rep[0.7] . rep[1.3] - rep[2.0]]    (* 零矩阵 {{0,0},{0,0}} *)

(* 不可约表示分解 *)
rep[theta] // MatrixForm
(* SO(2) 在 R^2 上的标准表示 *)
```

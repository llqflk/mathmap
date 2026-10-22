### 6. 泛函分析与算子代数

- 范畴：$\mathbf{Hilb}$ 希尔伯特空间范畴

- **对象例子**：$L^2[0,1]$ 平方可积函数空间

- **态射例子**：积分算子 $Tf(x)=\int_0^x f(t)dt$

- **核心函子实例**：对偶函子、傅里叶变换酉算子

- **Python 示例（简单线性算子）**

```python
def integral_op(f):
    return lambda x: sum(f(i*0.01)*0.01 for i in range(int(x/0.01)))
```

```mathematica
(* Mathematica：泛函分析中的算子 *)
(* 积分算子 T: f -> ∫_0^x f(t) dt *)
T[f_][x_] := Integrate[f[t], {t, 0, x}]
T[Sin][x]                           (* 1 - Cos[x] *)

(* 内积空间 *)
f[x_] := x; g[x_] := x^2
Integrate[f[x]*g[x], {x, 0, 1}]     (* L^2[0,1] 内积 = 1/4 *)

(* Gram-Schmidt 正交化 *)
Orthogonalize[{1, x, x^2}, Integrate[#1*#2, {x, -1, 1}] &]
```



- 范畴：$\mathbf{C^*Alg}$ C*-代数范畴

- **对象例子**：$C(X)$ 紧空间上连续函数的 C*-代数；$M_n(\mathbb C)$ 矩阵代数

- **态射例子**：*-同态 $f:A\to B$（保持加法、乘法、对合）

- **核心函子实例**：Gelfand 对偶（交换C*-代数↔紧Hausdorff空间）；包络 von Neumann 代数

- **Python 示例（矩阵作为C*-代数元素）**

```python
import numpy as np
A = np.array([[0,1],[0,0]])       # 幂零算子
A_dag = A.conj().T                 # 对合 *
comm = A @ A_dag - A_dag @ A      # 自伴交换子
norm_A = np.linalg.norm(A, 2)     # C*-范数 = 谱半径
print(f"‖A‖={norm_A:.3f}, A*A={A_dag@A}")
# C*恒等式 ‖A*A‖=‖A‖² 验证
print(f"‖A*A‖={np.linalg.norm(A_dag@A,2):.3f}, ‖A‖²={norm_A**2:.3f}")
```

```mathematica
(* Mathematica：C* 代数 *)
A = {{0, 1}, {0, 0}};          (* 幂零算子 *)
Adag = ConjugateTranspose[A];   (* 对合 *)
Norm[A]                         (* C* 范数 *)

(* 自伴交换子 *)
Adag . A - A . Adag             (* {{1, 0}, {0, -1}} *)
(* C* 恒等式验证 *)
Norm[Adag . A] == Norm[A]^2    (* True *)
```

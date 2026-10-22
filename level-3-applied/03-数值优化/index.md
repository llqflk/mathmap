### 3. 数值优化

- 范畴：$\mathbf{Opt}$ 优化问题范畴

- **对象例子**：目标函数 $f(x)=x^2+2\sin(x)$

- **态射例子**：牛顿法迭代步；拟牛顿Hessian更新（BFGS）

- **核心函子实例**：梯度下降函子；拉格朗日对偶函子（原问题↔对偶问题）

- **Python 示例（牛顿法与 BFGS 对比）**

```python
import numpy as np
from scipy.optimize import minimize
f = lambda x: x[0]**2 + 2*np.sin(x[0])
res = minimize(f, x0=3.0, method='BFGS')
print(f"BFGS: x*={res.x[0]:.4f}, f*={res.fun:.4f}")
# 约束优化: min x^2 s.t. x>=1
cons = {'type':'ineq','fun':lambda x: x[0]-1}
res_c = minimize(lambda x: x[0]**2, 0.0,
                 constraints=cons, method='SLSQP')
print(f"约束解 x*={res_c.x[0]:.4f}")
```

```mathematica
(* Mathematica：数值优化 *)
(* 无约束：BFGS *)
FindMinimum[x^2 + 2 Sin[x], {x, 3}]    (* {x->-0.379, 最小值→-1.77} *)

(* 约束优化 *)
NMinimize[{x^2, x >= 1}, x]            (* {1., {x->1.}} *)

(* 符号优化 *)
Minimize[{x^2, x >= 1}, x]             (* 精确解 *)
```

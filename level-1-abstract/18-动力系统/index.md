### 20. 动力系统

- 范畴：$\mathbf{Dyn}$ 状态自函子范畴

- **对象例子**：混沌映射状态

- **态射例子**：逻辑斯蒂映射 $x\to4x(1-x)$

- **核心函子实例**：迭代自函子

- **Python 示例**

```python
def logistic(x): return 4*x*(1-x)
x=0.2
for _ in range(10): x=logistic(x); print(x)
```

```mathematica
(* Mathematica：动力系统 *)
logistic[x_] := 4 x (1 - x)
(* 迭代 *)
NestList[logistic, 0.2, 10]          (* 10步迭代 *)
(* 相图 *)
ListPlot[NestList[logistic, 0.2, 100]]
```

---

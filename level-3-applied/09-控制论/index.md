### 10. 控制论

- 范畴：控制系统范畴

- 对象：系统状态

- 态射：控制律

- 函子：State Monad

- 示例：PID 迭代更新状态

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

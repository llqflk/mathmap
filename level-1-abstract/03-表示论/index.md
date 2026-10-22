### 3. 表示论

- 范畴：$\mathbf{Rep}(G)$ 群表示范畴

- **对象例子**：二维线性空间

- **态射例子**：群元素对应矩阵

- **核心函子实例**：表示函子 $G\to\mathbf{Vect}$

- **Python 示例**：上面旋转矩阵例子就是 SO(2) 的二维表示

```mathematica
(* Mathematica：SO(2) 的二维表示 *)
(* 群元 → 矩阵 *)
rep[theta_] := RotationMatrix[theta]
rep[Pi/3] . {1, 0}                      (* 旋转作用 *)

(* 不可约表示分解 *)
rep[theta] // MatrixForm
(* SO(2) 在 R^2 上的标准表示 *)
```

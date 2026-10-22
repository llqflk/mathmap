<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 代数几何

> 层级 1：抽象结构层 · 分组：代数几何与数论 · 第 15/21 条

[← 辛几何](../14-辛几何/index.md) · [总目录](../../README.md) · [代数数论 →](../16-代数数论/index.md)

- 范畴：$\mathbf{Sch}$ 概形范畴，或 $\mathbf{Var}_k$ 代数簇范畴

- **对象例子**：仿射直线 $\mathbb A_k^1$；椭圆曲线 $y^2=x^3-x$

- **态射例子**：态射 $f:\mathbb A^1\to\mathbb A^1,\ f(x)=x^2$

- **核心函子实例**：全局截影函子 $\Gamma$（概形→环）；结构层函子

- **Python 示例（椭圆曲线点加法）**

```python
def elliptic_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    x1,y1 = P; x2,y2 = Q
    if x1==x2 and (y1+y2)%p==0: return None
    if P==Q:
        m = (3*x1*x1+a)*pow(2*y1,-1,p)%p
    else:
        m = (y2-y1)*pow(x2-x1,-1,p)%p
    x3 = (m*m-x1-x2)%p
    y3 = (m*(x1-x3)-y1)%p
    return (x3, y3)

# 曲线 y^2=x^3-x over F_7
P=(0,0); Q=(1,0)
print(elliptic_add(P, Q, -1, 7))
```

```mathematica
(* Mathematica：椭圆曲线 *)
(* 曲线 y^2 = x^3 - x 在域 F_7 上 *)
ec = EllipticCurve[{-1, 0}, Modulus -> 7];
pts = Points[ec]                    (* 有限域上的有理点 *)
PointAdd[ec, {0, 0}, {1, 0}]       (* 点加法 *)

(* 复数域上的椭圆曲线 *)
ec2 = EllipticCurve[{-1, 0}];
ParametricPlot[Through[{Re, Im}[WeierstrassP[t, {-1, 0}]]], {t, 0, 2Pi}]
```

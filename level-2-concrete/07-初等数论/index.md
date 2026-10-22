<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 初等数论

> 层级 2：具体结构层 · 分组：代数类 · 第 7/11 条

[← 多项式代数 / 矩阵论](../06-多项式代数/index.md) · [总目录](../../README.md) · [解析几何 / 微分几何入门 →](../08-解析几何/index.md)

- 范畴：$\mathbf{Arith}$ 算术范畴（$\mathbb Z$ 及其同余结构）

- **对象例子**：整数 $\mathbb Z$，模 $n$ 剩余类环 $\mathbb Z/n\mathbb Z$

- **态射例子**：同余映射 $a\mapsto a\bmod n$；欧拉函数 $\varphi(n)$

- **核心函子实例**：局部化函子（$\mathbb Z\to\mathbb Z_{(p)}$）；模约化函子

- **Python 示例（RSA 密钥生成思想）**

```python
import math
def lcm(a, b): return a*b//math.gcd(a,b)
def modinv(a, m):
    def egcd(a,b):
        if b==0: return a,1,0
        g,x,y = egcd(b, a%b)
        return g,y,x-(a//b)*y
    g,x,_ = egcd(a,m)
    return x%m if g==1 else None
# 小规模RSA：p=61, q=53
phi = (61-1)*(53-1)
e = 17
d = modinv(e, phi)
print(f"公钥({e},{61*53}) 私钥({d},{61*53})")
```

```mathematica
(* Mathematica：数论内置函数 *)
(* 扩展欧几里得 *)
ExtendedGCD[17, (61-1)*(53-1)]   (* {1, {233, -1}} *)

(* RSA 核心：模逆用 PowerMod *)
phi = (61-1)*(53-1);
e = 17;
d = PowerMod[e, -1, phi]         (* 私钥指数 *)

(* 加密/解密 *)
n = 61*53;
m = 42;                           (* 明文 *)
c = PowerMod[m, e, n];            (* 密文 *)
PowerMod[c, d, n]                 (* 解密还原 → 42 *)
```

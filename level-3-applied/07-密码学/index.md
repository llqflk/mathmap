<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 密码学

> 层级 3：模型与计算层 · 第 7/15 条

[← 信息论](../06-信息论/index.md) · [总目录](../../README.md) · [信号处理 →](../08-信号处理/index.md)

- 范畴：$\mathbf{Crypt}$ 密码系统范畴

- **对象例子**：明文空间 $\mathcal M$（有限集上的消息）

- **态射例子**：加密函数 $E_k:\mathcal M\to\mathcal C$（密钥 $k$ 参数化）

- **核心函子实例**：同态加密函子（明文运算↔密文运算）

- **Python 示例（Paillier 加法同态示意）**

```python
import math
def paillier_keygen(bits=16):
    p, q = 17, 19  # 小素数示例
    n = p*q; lam = math.lcm(p-1, q-1)
    g = n+1; mu = pow(lam, -1, n)
    return (n,g), (lam,mu,n)  # 公钥, 私钥

def paillier_enc(pk, m):
    n,g = pk; r = 7  # 随机数(实际应随机)
    n2 = n*n
    return (pow(g,m,n2)*pow(r,n,n2))%n2

def paillier_dec(sk, c):
    lam,mu,n = sk; n2 = n*n
    L = (pow(c,lam,n2)-1)//n
    return (L*mu)%n

pk, sk = paillier_keygen()
c = paillier_enc(pk, 42)
print(f"Enc(42)={c}, Dec={paillier_dec(sk,c)}")
# 同态性: E(a)*E(b) = E(a+b) mod n²
```

```mathematica
(* Mathematica：密码学 *)
(* RSA *)
p = 61; q = 53; n = p*q; phi = (p-1)*(q-1);
e = 17; d = PowerMod[e, -1, phi];      (* 私钥 *)
c = PowerMod[42, e, n];                (* 加密 *)
PowerMod[c, d, n]                      (* 解密 → 42 *)

(* 离散对数 *)
MultiplicativeOrder[2, 101]            (* ord_101(2) *)
```

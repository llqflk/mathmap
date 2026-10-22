### 6. 单子（Monad）

- 范畴：自函子范畴上的 Monoid——$(T,\eta,\mu)$，$T:\mathcal C\to\mathcal C$ 是自函子

- **对象例子**：Maybe 单子 $T(X)=X\sqcup\{\text{None}\}$（处理可能缺失的值）

- **态射例子**：单位 $\eta_X:X\to T(X)$ 把纯值提升进单子上下文；乘法 $\mu_X:T(T(X))\to T(X)$ 把嵌套单子摊平

- **核心函子实例**：每个伴随 $F\dashv G$ 产生单子 $G\circ F$

- **Python 示例（Maybe/List 单子的 bind）**

```python
class Maybe:
    """Maybe Monad: T(X) = X | None"""
    @staticmethod
    def pure(x): return ('Just', x)   # η: X → T(X)

    @staticmethod
    def bind(mx, f):                  # >>= : T(X) × (X→T(Y)) → T(Y)
        if mx[0] == 'Nothing': return mx
        return f(mx[1])

# Maybe 链式计算
result = Maybe.bind(
    Maybe.pure(42),
    lambda x: Maybe.pure(x / 2) if x != 0 else ('Nothing',)
)
print(result)  # ('Just', 21.0)

# List Monad: T(X) = [X], bind = flatMap
List = type('List', (), {
    'pure': staticmethod(lambda x: [x]),
    'bind': staticmethod(lambda xs, f: [y for x in xs for y in f(x)])
})
print(List.bind([1,2,3], lambda x: [x, -x]))  # [1,-1,2,-2,3,-3]
```

```mathematica
(* Mathematica：单子 *)
(* Maybe 单子 *)
Just[x_] := x; NothingQ = Nothing;
(* pure = η: X → T(X) *)
pure[x_] := x
(* bind = >>= : T(X) × (X→T(Y)) → T(Y) *)
bind[mx_, f_] := If[mx === Nothing, Nothing, f[mx]]

(* 安全除法：a/b，b=0 时返回 Nothing *)
safeDiv[a_, b_] := If[b == 0, Nothing, a/b]
bind[pure[42], safeDiv[#, 2] &]    (* 21 *)
bind[pure[42], safeDiv[#, 0] &]    (* Nothing *)
```

---

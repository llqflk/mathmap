<!-- 自动生成：由 tools/build.py 从 math.md 抽取。要改内容请改 math.md。 -->

# 量子计算数学

> 层级 3：模型与计算层 · 第 15/15 条

[← 金融数学](../14-金融数学/index.md) · [总目录](../../README.md)

- 范畴：$\mathbf{CPTP}$ 量子信道范畴——对象为有限维 Hilbert 空间 $\mathcal H$，态射为完全正保迹映射

- **对象例子**：单量子比特 $\mathcal H\cong\mathbb C^2$（Bloch 球面）；密度矩阵 $\rho$

- **态射例子**：酉门 $U\in\mathrm{SU}(2^n)$（如 Hadamard $H$、CNOT）；量子测量 $\{M_k\}$（POVM）

- **核心函子实例**：量子 Fourier 变换函子 $\mathrm{QFT}_n$；振幅放大函子（Grover）；Stinespring 扩张（CPTP→酉）

- **Python 示例（量子比特模拟 + 量子门）**

```python
import numpy as np

# 单量子比特状态
ket0 = np.array([1+0j, 0+0j])
ket1 = np.array([0+0j, 1+0j])

# 量子门
H = 1/np.sqrt(2) * np.array([[1, 1], [1, -1]])       # Hadamard
X = np.array([[0, 1], [1, 0]])                         # Pauli-X (NOT)
Z = np.array([[1, 0], [0, -1]])                        # Pauli-Z

# 量子线路：H|0⟩ = (|0⟩+|1⟩)/√2
psi = H @ ket0
print(f"H|0⟩ = [{psi[0]:.3f}, {psi[1]:.3f}]")

# Bell 态：CNOT·(H⊗I)|00⟩
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
bell = CNOT @ np.kron(H, np.eye(2)) @ np.kron(ket0, ket0)
print(f"|Bell⟩ = 1/√2 (|00⟩+|11⟩) = {bell.round(3)}")

# 量子 Fourier 变换 (n=3)
def QFT(n):
    N = 2**n; omega = np.exp(2j*np.pi/N)
    return np.array([[omega**(j*k)/np.sqrt(N) for k in range(N)]
                     for j in range(N)])
print(f"QFT_3 前2×2: {QFT(3)[:2,:2].round(3)}")
```

```mathematica
(* Mathematica：量子计算 *)
(* 单量子比特 *)
ket0 = {1, 0}; ket1 = {0, 1};
H = {{1, 1}, {1, -1}}/Sqrt[2];
X = {{0, 1}, {1, 0}};

(* Hadamard 作用 *)
H . ket0  (* {1/√2, 1/√2} = (|0⟩+|1⟩)/√2 *)

(* 量子 Fourier 变换 *)
QFTMatrix[n_] := FourierMatrix[2^n] / Sqrt[2^n]
(* Schmidt 分解与纠缠度 *)
SingularValueDecomposition[{{1,0,0,1},{0,0,0,0},{0,0,0,0},{1,0,0,1}}/2]
```

---

如果你愿意，我可以把上面**全部内容整理成一份干净的 Markdown 文档**，去掉代码块冗余，做成可直接复制到 Notion/Word 的完整版。

> （注：部分内容可能由 AI 生成）

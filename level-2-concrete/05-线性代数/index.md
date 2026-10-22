# 线性代数

[← 返回总目录](../../README.md) · 12 章讲义，含章节表与 Python/Mathematica 双示例

> **范畴**：$\mathbf{Vect}_k$ — 以域 $k$ 上有限维向量空间为对象，线性映射为态射。
> 线性代数之所以"线性"，本质上是因为 $\mathbf{Vect}_k$ 是一个 **Abel 范畴**——态射集 $\mathrm{Hom}(V,W)$ 自带向量空间结构。

## 目录

| 章 | 标题 | 范畴论视角 |
|---|---|---|
| 1 | [向量空间与子空间](01-向量空间.md) | 对象语言：$\mathbf{Vect}_k$ 中的对象与子对象 |
| 2 | [线性变换与矩阵](02-线性变换与矩阵.md) | 态射语言：$\mathrm{Hom}(V,W)$ 与矩阵表示函子 |
| 3 | [线性方程组](03-线性方程组.md) | 态射的核与像：$\ker T$、$\mathrm{im}\,T$ |
| 4 | [行列式](04-行列式.md) | 外幂函子 $\Lambda^n:\mathbf{Vect}_k\to\mathbf{Vect}_k$ |
| 5 | [特征值与特征向量](05-特征值与特征向量.md) | 自态射的谱：$T:V\to V$ 的不变子空间 |
| 6 | [内积空间](06-内积空间.md) | $\mathbf{Hilb}_{\text{fd}}$：带内积的向量空间范畴 |
| 7 | [正交性与 Gram-Schmidt](07-正交化.md) | 正交分解：$\mathbf{Hilb}_{\text{fd}}$ 中的直和 |
| 8 | [对角化与谱定理](08-对角化.md) | 自伴算子的谱分解 |
| 9 | [Jordan 标准形](09-Jordan标准形.md) | 幂零自态射的分类 |
| 10 | [二次型](10-二次型.md) | 对称双线性形式与 Sylvester 惯性律 |
| 11 | [奇异值分解 (SVD)](11-奇异值分解.md) | 任意态射的极分解 $T=U\Sigma V^*$ |
| 12 | [应用](12-应用.md) | 最小二乘、PCA、PageRank |

## 范畴论全局视角

整个线性代数可以用一句话概括：**研究 $\mathbf{Vect}_k$ 这个 Abel 范畴的内蕴结构**。

| 线性代数概念 | 范畴论对应 | 函子/自然变换 |
|---|---|---|
| 向量空间 $V$ | $\mathbf{Vect}_k$ 的对象 | — |
| 线性映射 $T$ | $\mathbf{Vect}_k$ 的态射 | — |
| 直和 $V\oplus W$ | 双积（积=余积） | 加法函子 |
| 核 $\ker T$ | 等化子 | $\ker:\mathrm{Hom}\to\mathrm{Sub}$ |
| 对偶空间 $V^*$ | 反变函子 $(-)^*$ | $(-)^*:\mathbf{Vect}_k^{op}\to\mathbf{Vect}_k$ |
| 双重对偶 $V^{**}$ | $(-)^{**}\cong\mathrm{Id}$ | 自然同构（有限维） |
| 张量积 | 幺半积 | $\otimes:\mathbf{Vect}_k\times\mathbf{Vect}_k\to\mathbf{Vect}_k$ |
| 行列式 | 外幂 | $\Lambda^{\dim V}:\mathbf{Vect}_k\to\mathbf{Vect}_k$ |
| SVD | 极分解 | $T=U\circ\Sigma\circ V^*$ |

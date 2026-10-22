# 数学范畴与应用实例

用范畴论作统一语言，把数学拆成五个层级：**元框架 → 范畴论工具 → 抽象结构 → 具体实例 → 模型计算**。
每个主题条目都给出同一套东西：`范畴` → `对象例子` → `态射例子` → `核心函子` → `Python` + `Mathematica` 双示例。

**规模**：5 个层级 · 54 个主题条目 · 59 个 Python 示例 · 59 个 Mathematica 示例
**两种读法**：通读看单文件 [math.md](math.md)；按主题跳转用下面的目录。

## 怎么读

| 目的 | 路径 |
|---|---|
| 建立元视角 | 层级 0：为什么用范畴论给数学分类 |
| 学会语言 | 层级 0.5：范畴、函子、自然变换、米田、伴随、单子 |
| 看结构 | 层级 1：代数 / 拓扑 / 几何 / 数论 / 逻辑的一般框架 |
| 看实例 | 层级 2：分析、线性代数、概率统计等可以直接算的对象 |
| 看算法 | 层级 3：优化、数值 PDE、机器学习、密码学等工程化模型 |
| 想跑一遍 | `python tools/check.py`（逐个执行文中 Python 示例） |

## 层级 0：元框架

> **定位**：站在数学之外看数学——将整份文档的分类法本身作为范畴论对象。

| # | 条目 | 范畴 | 代码 |
|---|---|---|---|
| — | [数学分支的范畴 $\mathbf{Math}$](level-0-meta/数学分支的范畴/index.md) | $\mathbf{Math}$——以数学分支为对象，以分支间的结构映射为态射 | py · mma |

## 层级 0.5：范畴论基础工具箱

> **定位**：在讨论 Grp、Top、Vect 这些具体范畴之前，先定义"范畴"本身是什么。

| # | 条目 | 范畴 | 代码 |
|---|---|---|---|
| 01 | [范畴的定义](level-0.5-category-toolkit/01-范畴的定义/index.md) | $\mathbf{Cat}$——范畴的范畴（以范畴为对象，以函子为态射） | py · mma |
| 02 | [函子](level-0.5-category-toolkit/02-函子/index.md) | $\mathbf{Cat}$ 中的态射就是函子——保持结构的范畴间映射 | py · mma |
| 03 | [自然变换](level-0.5-category-toolkit/03-自然变换/index.md) | $\mathbf{Fun}(\mathcal C,\mathcal D)$——以函子为对象，以自然变换为态射的函子范畴 | py · mma |
| 04 | [米田嵌入](level-0.5-category-toolkit/04-米田嵌入/index.md) | $[\mathcal C^{op},\mathbf{Set}]$ 预层范畴 | py · mma |
| 05 | [伴随函子](level-0.5-category-toolkit/05-伴随函子/index.md) | 伴随对 $(F,G,\eta,\varepsilon)$，写作 $F\dashv G$ | py · mma |
| 06 | [单子（Monad）](level-0.5-category-toolkit/06-单子/index.md) | 自函子范畴上的 Monoid——$(T,\eta,\mu)$，$T:\mathcal C\to\mathcal C$ 是自函子 | py · mma |

## 层级 1：抽象结构层

> **判断标准**：对象是"结构的结构"——你不能用一个具体数值来举例，只能描述结构之间的映射关系。

| # | 条目 | 范畴 | 代码 |
|---|---|---|---|
| 01 | [抽象代数（群 / 环 / 域 / 模）](level-1-abstract/01-抽象代数/index.md) | $\mathbf{Grp}$ 群范畴 | py · mma |
| 02 | [李群与李代数](level-1-abstract/02-李群与李代数/index.md) | $\mathbf{LieGrp}$ 李群范畴 | py · mma |
| 03 | [表示论](level-1-abstract/03-表示论/index.md) | $\mathbf{Rep}(G)$ 群表示范畴——对象是 $G$-模（带群作用的向量空间），态射是 $G$-等变线性映射 | py · mma |
| 04 | [同调代数](level-1-abstract/04-同调代数/index.md) | $\mathbf{Ch}(R)$ 链复形范畴（R-模上的链复形） | py · mma |
| 05 | [范畴论（作为独立学科：高阶结构）](level-1-abstract/05-范畴论/index.md) | $\mathbf{2Cat}$ 2-范畴的范畴——对象是 2-范畴，态射是 2-函子 | py · mma |
| 06 | [泛函分析与算子代数](level-1-abstract/06-泛函分析与算子代数/index.md) | $\mathbf{Hilb}$ 希尔伯特空间范畴 | py · mma |
| 07 | [实分析（测度论）](level-1-abstract/07-实分析-测度论/index.md) | $\mathbf{Meas}$ 可测空间范畴 | py · mma |
| 08 | [调和分析](level-1-abstract/08-调和分析/index.md) | 拓扑群上函数空间范畴 | py · mma |
| 09 | [PDE 进阶（索伯列夫空间）](level-1-abstract/09-PDE进阶/index.md) | 索伯列夫空间范畴 | py · mma |
| 10 | [点集拓扑](level-1-abstract/10-点集拓扑/index.md) | $\mathbf{Top}$ 拓扑空间范畴 | py · mma |
| 11 | [代数拓扑](level-1-abstract/11-代数拓扑/index.md) | 拓扑空间→代数的函子范畴 | py · mma |
| 12 | [微分拓扑](level-1-abstract/12-微分拓扑/index.md) | $\mathbf{Diff}$ 微分流形范畴（对象为光滑流形，态射为光滑映射） | py · mma |
| 13 | [黎曼几何 / 微分几何](level-1-abstract/13-黎曼几何/index.md) | $\mathbf{Riem}$ 黎曼流形范畴 | py · mma |
| 14 | [辛几何](level-1-abstract/14-辛几何/index.md) | $\mathbf{Sympl}$ 辛流形范畴 | py · mma |
| 15 | [代数几何](level-1-abstract/15-代数几何/index.md) | $\mathbf{Sch}$ 概形范畴，或 $\mathbf{Var}_k$ 代数簇范畴 | py · mma |
| 16 | [代数数论](level-1-abstract/16-代数数论/index.md) | $\mathbf{NumFld}$ 数域范畴 | py · mma |
| 17 | [概率论与随机过程](level-1-abstract/17-概率论与随机过程/index.md) | 带滤波概率空间范畴 | py · mma |
| 18 | [动力系统](level-1-abstract/18-动力系统/index.md) | $\mathbf{Dyn}$ 状态自函子范畴 | py · mma |
| 19 | [数理逻辑](level-1-abstract/19-数理逻辑/index.md) | $\mathbf{Th}$ 理论范畴——对象是一阶理论 $T$，态射是理论间的解释（interpretation） | py · mma |
| 20 | [集合论](level-1-abstract/20-集合论/index.md) | $\mathbf{V}$ von Neumann 宇宙——以累积层级 $V_\alpha$ 为对象 | py · mma |
| 21 | [模形式](level-1-abstract/21-模形式/index.md) | $M_k(\Gamma)$ 权 $k$ 模形式空间（$\Gamma=\mathrm{SL}(2,\mathbb Z)$） | py · mma |

## 层级 2：具体结构层

> **判断标准**：对象可以写出一个具体数值——你可以用代码跑出一个数字来。

| # | 条目 | 范畴 | 代码 |
|---|---|---|---|
| 01 | [数学分析与多变量微积分](level-2-concrete/01-数学分析与多变量微积分/index.md) | $\mathbf{Man}_\infty$ 光滑流形范畴（取特例：$\mathbb R$ 一维欧氏流形） | py · mma |
| 02 | [复变函数论](level-2-concrete/02-复变函数论/index.md) | $\mathbf{Hol}$ 复解析空间范畴 | py · mma |
| 03 | [常微分方程 ODE](level-2-concrete/03-常微分方程/index.md) | $\mathbf{Dyn}$ 动力系统范畴 | py · mma |
| 04 | [偏微分方程入门（PDE）](level-2-concrete/04-偏微分方程入门/index.md) | $\mathbf{DiffOp}$ 微分算子范畴 | py · mma |
| 05 | [线性代数](level-2-concrete/05-线性代数/index.md) | $\mathbf{Vect}_\mathbb R$ 有限维实线性空间 | py · mma · 12 章讲义 |
| 06 | [多项式代数 / 矩阵论](level-2-concrete/06-多项式代数/index.md) | $\mathbf{Poly}$ 多项式环范畴 | py · mma |
| 07 | [初等数论](level-2-concrete/07-初等数论/index.md) | $\mathbf{Arith}$ 算术范畴（$\mathbb Z$ 及其同余结构） | py · mma |
| 08 | [解析几何 / 微分几何入门](level-2-concrete/08-解析几何/index.md) | $\mathbf{Euc}$ 欧氏空间范畴 | py · mma |
| 09 | [概率论与数理统计](level-2-concrete/09-概率论与数理统计/index.md) | $\mathbf{FinProb}$ 有限概率空间范畴 | py · mma |
| 10 | [组合与离散数学](level-2-concrete/10-组合与离散数学/index.md) | $\mathbf{FinSet}$ 有限集范畴 | py · mma |
| 11 | [博弈论](level-2-concrete/11-博弈论/index.md) | $\mathbf{Game}$ 博弈范畴——对象为博弈（策略式或展开式），态射为博弈间的态射 | py · mma |

## 层级 3：模型与计算层

> **判断标准**：以解决具体工程问题为目的——数学结构在这里被算法化。

| # | 条目 | 范畴 | 代码 |
|---|---|---|---|
| 01 | [数值线性代数](level-3-applied/01-数值线性代数/index.md) | $\mathbf{Vect}_{\mathbb R}^{\mathrm{fd}}$ 的浮点实现——把 Abel 范畴搬到 IEEE 754 数组上 | py · mma |
| 02 | [有限元](level-3-applied/02-有限元/index.md) | $\mathbf{FE}(\Omega)$ 有限元空间范畴——对象是网格上的有限元空间，态射是插值与限制映射 | py · mma |
| 03 | [数值优化](level-3-applied/03-数值优化/index.md) | $\mathbf{Opt}$ 优化问题范畴 | py · mma |
| 04 | [凸优化](level-3-applied/04-凸优化/index.md) | $\mathbf{Conv}$ 凸集范畴——对象是凸集，态射是仿射映射（保持凸组合） | py · mma |
| 05 | [贝叶斯统计与MCMC](level-3-applied/05-贝叶斯统计与MCMC/index.md) | $\mathbf{MC}$ 随机模拟范畴 | py · mma |
| 06 | [信息论](level-3-applied/06-信息论/index.md) | $\mathbf{Prob}$ 概率分布范畴（对象为分布，态射为信道） | py · mma |
| 07 | [密码学](level-3-applied/07-密码学/index.md) | $\mathbf{Crypt}$ 密码系统范畴 | py · mma |
| 08 | [信号处理](level-3-applied/08-信号处理/index.md) | $\mathbf{Sig}$ 信号空间范畴（$\ell^2$ 或 $L^2$） | py · mma |
| 09 | [控制论](level-3-applied/09-控制论/index.md) | $\mathbf{Sys}$ 线性系统范畴——对象是 LTI 系统 $(A,B,C,D)$，态射是系统互连（串联、反馈） | py · mma |
| 10 | [计算几何](level-3-applied/10-计算几何/index.md) | $\mathbf{CompGeom}$ 计算几何范畴 | py · mma |
| 11 | [计算流体力学（CFD）](level-3-applied/11-计算流体力学/index.md) | $\mathbf{CFD}$ 连续介质离散化范畴 | py · mma |
| 12 | [图论](level-3-applied/12-图论/index.md) | $\mathbf{Graph}$ 图范畴——对象是图，态射是图同态（把边映成边） | py · mma |
| 13 | [深度学习](level-3-applied/13-深度学习/index.md) | $\mathbf{Smooth}$ 可微映射范畴——对象是 $\mathbb R^n$（张量空间），态射是可微映射 | py · mma |
| 14 | [金融数学](level-3-applied/14-金融数学/index.md) | $\mathbf{Mkt}$ 市场模型范畴——对象为概率空间上的资产与衍生品 | py · mma |
| 15 | [量子计算数学](level-3-applied/15-量子计算数学/index.md) | $\mathbf{CPTP}$ 量子信道范畴——对象为有限维 Hilbert 空间 $\mathcal H$，态射为完全正保迹映射 | py · mma |

## 维护方式

`math.md` 是唯一真相源；目录树与根 README 都是它的投影，不要手改生成物。

```bash
python tools/build.py           # 从 math.md 重新生成 README.md 与各主题 index.md
python tools/build.py --check   # 只校验：编号↔目录是否对齐、相对链接是否都可解析
python tools/check.py           # 逐个运行文中 Python 示例（-v 显示每个块的位置）
python tools/site.py            # 生成静态站点 _site/（含三维交互页 /3d.html）
python -m http.server 8765 --directory _site   # 打开 http://127.0.0.1:8765/
```

`check.py` 的判定分五档：独立跑通 / 依赖同文件前文 / 用 matplotlib 替身跑通（数值逻辑已验证、绘图未验证）/ 缺库跳过 / 失败。装了 `numpy` 就能跑通绝大多数示例，`scipy`、`matplotlib`、`networkx` 只影响个别条目。

例外：`level-2-concrete/05-线性代数/` 是手写的 12 章讲义（含章节表与可视化），
生成器不会覆盖它；改动请直接改该目录下的章节文件。

> 需要 Python 3.9+。

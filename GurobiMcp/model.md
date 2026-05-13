## 数学规划与优化建模模型大全

| 类别 | 模型全称 | 缩写 | 核心特征 |
|------|----------|------|----------|
| **线性规划类** | Linear Programming | LP | 目标函数与约束均为线性 |
| | Integer Linear Programming | ILP | 决策变量为整数，约束线性 |
| | Mixed-Integer Linear Programming | MILP | 部分变量为整数，线性结构 |
| | Binary Integer Programming | BIP | 决策变量仅取 0/1 |
| | Multi-objective Linear Programming | MOLP | 多个线性目标函数 |
| **非线性规划类** | Nonlinear Programming | NLP | 目标或约束含非线性项 |
| | Mixed-Integer Nonlinear Programming | MINLP | 含整数变量的非线性规划 |
| | Quadratic Programming | QP | 目标为二次函数，约束线性 |
| | Mixed-Integer Quadratic Programming | MIQP | QP + 整数变量 |
| | Quadratically Constrained Quadratic Programming | QCQP | 目标与约束均为二次函数 |
| | Mixed-Integer QCQP | MIQCQP | QCQP + 整数变量 |
| | Geometric Programming | GP | 目标与约束为正项式/单项式 |
| | Signomial Programming | SP | GP 的推广，允许负系数 |
| **锥规划类** | Second-Order Cone Programming | SOCP | 约束为二阶锥，LP 的推广 |
| | Mixed-Integer SOCP | MISOCP | SOCP + 整数变量 |
| | Semidefinite Programming | SDP | 约束含矩阵正半定条件 |
| | Mixed-Integer SDP | MISDP | SDP + 整数变量 |
| | Copositive Programming | CP | 约束含余正矩阵锥 |
| | Completely Positive Programming | CPP | CP 的对偶形式 |
| **动态规划类** | Dynamic Programming | DP | 多阶段决策，最优子结构 |
| | Stochastic Dynamic Programming | SDP* | DP + 随机状态转移 |
| | Approximate Dynamic Programming | ADP | 大规模 DP 的近似求解 |
| **随机规划类** | Stochastic Programming | SP | 含随机参数的规划模型 |
| | Two-Stage Stochastic Programming | 2SSP | 先决策后观察不确定性 |
| | Chance-Constrained Programming | CCP | 约束以一定概率成立 |
| | Robust Optimization | RO | 对最坏情形不确定性免疫 |
| | Distributionally Robust Optimization | DRO | 对分布的模糊集鲁棒优化 |
| **多目标规划类** | Multi-objective Programming | MOP | 同时优化多个目标函数 |
| | Goal Programming | GoalP | 最小化与目标值的偏差 |
| | Pareto Optimization | — | 求解 Pareto 前沿解集 |
| | Lexicographic Optimization | LexO | 按优先级顺序优化目标 |
| **网络与图模型** | Network Flow Programming | NFP | 基于网络图的流量优化 |
| | Minimum Cost Flow | MCF | 最小化网络总流动成本 |
| | Maximum Flow | MaxFlow | 最大化源到汇的流量 |
| | Shortest Path Problem | SPP | 图中最短路径求解 |
| | Traveling Salesman Problem | TSP | 最短哈密顿回路（NP-hard）|
| | Vehicle Routing Problem | VRP | TSP 推广，多车辆路径优化 |
| | Minimum Spanning Tree | MST | 最小生成树问题 |
| **均衡与博弈类** | Complementarity Problem | CP | 含互补条件的均衡模型 |
| | Linear Complementarity Problem | LCP | 线性互补问题 |
| | Nonlinear Complementarity Problem | NCP | 非线性互补问题 |
| | Mixed Complementarity Problem | MCP | 混合互补问题 |
| | Mathematical Program with Equilibrium Constraints | MPEC | 下层为均衡问题的双层规划 |
| | Variational Inequality | VI | 广义均衡条件建模 |
| | Nash Equilibrium Problem | NEP | 多主体博弈均衡 |
| | Generalized Nash Equilibrium Problem | GNEP | 共享约束的 Nash 均衡 |
| **双层规划类** | Bilevel Programming | BLP | 上下两层嵌套优化结构 |
| | Multilevel Programming | MLP | 三层及以上嵌套优化 |
| | Stackelberg Game | — | 主从博弈的双层规划 |
| **分解与大规模** | Column Generation | CG | 动态生成变量的大规模 LP |
| | Benders Decomposition | BD | 主子问题交替迭代求解 |
| | Dantzig-Wolfe Decomposition | DWD | 块结构 LP 的分解方法 |
| | Lagrangian Relaxation | LR | 松弛约束引入乘子求解 |
| **变分与连续优化** | Convex Optimization | ConvOpt | 目标为凸函数，约束为凸集 |
| | DC Programming | DCP | 目标为两凸函数之差 |
| | Semi-infinite Programming | SIP | 有限变量，无限约束 |
| | Infinite-dimensional Optimization | — | 变量为函数的优化问题 |
| | Optimal Control | OC | 动态系统的控制优化 |
| | Model Predictive Control | MPC | 滚动时域的最优控制 |
| **黑箱与仿真优化** | Derivative-Free Optimization | DFO | 无梯度信息的优化 |
| | Simulation-based Optimization | SimOpt | 目标通过仿真计算得出 |
| | Surrogate-based Optimization | SBO | 用代理模型替代昂贵评估 |
| | Bayesian Optimization | BO | 用贝叶斯后验指导搜索 |
| **模糊与区间类** | Fuzzy Programming | FP | 参数或约束含模糊集 |
| | Interval Programming | IP | 参数为区间数的规划 |
| | Possibilistic Programming | PP | 基于可能性理论的规划 |
| **其他经典模型** | Constraint Programming | CP | 用约束传播求可行解 |
| | Satisfiability Problem | SAT / MaxSAT | 布尔变量满足性问题 |
| | Cutting Plane Method | — | 逐步添加割平面收紧松弛 |
| | Assignment Problem | AP | 最优一对一分配问题 |
| | Scheduling Problem | — | 工序/资源时序优化 |
| | Lot Sizing Problem | LSP | 生产批量与库存决策 |
| | Facility Location Problem | FLP | 最优设施选址与分配 |

> **层级关系速查**：LP ⊂ QP ⊂ QCQP ⊂ SOCP ⊂ SDP（凸松弛层级）；LP ⊂ MILP ⊂ MINLP（整数规划层级）；LP ⊂ NLP ⊂ MINLP（非线性层级）
## Gurobi 13.0 对各模型类型的支持情况

| 模型                                    | 缩写           | Gurobi 13.0 支持？ | 支持细节                                          | 备注                                        |
|---------------------------------------|--------------|:---------------:|-----------------------------------------------|-------------------------------------------|
| Linear Programming                    | LP           |   ✅ **完全支持**    | Simplex + Interior Point + **新增 PDHG（GPU加速）** | 13.0 新增 PDHG 算法，专为超大规模 LP 设计              |
| Mixed Integer Linear Programming      | MILP/MIP     |   ✅ **完全支持**    | Branch-and-Bound + Cutting Planes             | 13.0 对困难 MIP 平均提速 **~16%**                |
| Integer Linear Programming            | ILP          |   ✅ **完全支持**    | 与 MILP 同一求解框架，所有变量为整数                         | ILP 是 MILP 的特例，完全覆盖                       |
| Quadratic Programming                 | QP           |   ✅ **完全支持**    | 凸/非凸均支持（非凸自 v9.0 起）                           | 凸 QP 用 Interior Point；非凸 QP 用 spatial B&B |
| Mixed Integer Quadratic Programming   | MIQP         |   ✅ **完全支持**    | 13.0 对 MIQP 提速 **~5%**                        | 官方 benchmark 明确列出                         |
| Quadratically Constrained QP          | QCQP / MIQCP |   ✅ **完全支持**    | 凸 QCQP 和非凸 QCQP 均支持                           | 13.0 对非凸 MIQCP 提速高达 **2.68x**             |
| Second-Order Cone Programming         | SOCP         |   ✅ **完全支持**    | SOCP 约束可与整数变量混合（MISOCP）                       | Gurobi 将 SOCP 作为 QCP 的子类原生支持              |
| Nonlinear Programming                 | NLP          |   ✅ **完全支持**    | 支持多元复合非线性函数约束（exp, log, sin 等）                | 13.0 新增 **Nonlinear Barrier Method**      |
| Mixed Integer Nonlinear Programming   | MINLP        |   ✅ **完全支持**    | Outer Approximation + spatial B&B             | 13.0 对 MINLP 提速超过 **2.5x**（困难模型 6.34x）    |


---
name: Gurobi MCP 服务集合
description: 为 Gurobi 13.0 支持的 9 种数学规划模型提供统一 MCP 工具服务
version: 2.0.0
author: Gurobi Expert
tags: [gurobi, optimization, mcp, linear-programming, integer-programming, quadratic-programming, nonlinear-programming]
---

# Gurobi MCP 服务集合

为 Gurobi 13.0 优化求解器支持的 9 种核心数学规划模型类型提供统一的 MCP (Model Context Protocol) 服务。
单一入口，面向对象架构，大模型自动判断问题类型并调用对应 tool。

## 架构

```
GurobiMcp/
├── main.py              # 唯一入口，注册所有 tool，启动 MCP 服务
├── solver/
│   ├── __init__.py      # 导出所有求解器
│   ├── base.py          # BaseSolver 基类 - 公共逻辑
│   ├── lp.py            # LPSolver - 线性规划
│   ├── ilp.py           # ILPSolver - 纯整数线性规划
│   ├── milp.py          # MILPSolver - 混合整数线性规划
│   ├── qp.py            # QPSolver - 二次规划
│   ├── miqp.py          # MIQPSolver - 混合整数二次规划
│   ├── qcqp.py          # QCQPSolver - 二次约束二次规划
│   ├── socp.py          # SOCPSolver - 二阶锥规划
│   ├── nlp.py           # NLPSolver - 非线性规划
│   └── minlp.py         # MINLPSolver - 混合整数非线性规划
├── pyproject.toml
└── SKILL.md
```

## 快速开始

### 环境要求

- Python 3.12+
- Gurobi 13.0+ (需要有效许可证)
- `mcp[cli]>=1.27.1`
- `gurobipy`


## 通用参数配置

所有求解器默认使用以下 Gurobi 参数：

| 参数 | 值 | 说明 |
|------|-----|------|
| Threads | 0 | 自动选择线程数 |
| MIPGap | 0.01 | 1% MIP 间隙容差 |
| TimeLimit | 300 | 5 分钟求解时间限制 |
| OutputFlag | 1 | 显示求解日志 |

## Tool 列表

| Tool 名称 | 模型类型 | 说明 |
|-----------|---------|------|
| `solve_lp` | LP | 线性规划，返回影子价格和简约成本 |
| `solve_ilp` | ILP | 纯整数线性规划，支持 BIP 模式 |
| `solve_milp` | MILP | 混合整数线性规划 |
| `solve_qp` | QP | 二次目标，支持凸/非凸 |
| `solve_miqp` | MIQP | 混合整数二次规划 |
| `solve_qcqp` | QCQP/MIQCQP | 二次约束二次规划 |
| `solve_socp` | SOCP/MISOCP | 二阶锥规划 |
| `solve_nlp` | NLP | 非线性规划 (nlfunc 接口) |
| `solve_minlp` | MINLP | 混合整数非线性规划 |

## 使用示例

### LP

```json
{
  "objective": {"x1": 3.0, "x2": 5.0},
  "constraints": [
    {"coeffs": {"x1": 1.0, "x2": 2.0}, "sense": "<=", "rhs": 10.0, "name": "c1"},
    {"coeffs": {"x1": 2.0, "x2": 1.0}, "sense": "<=", "rhs": 8.0, "name": "c2"}
  ],
  "sense": "maximize"
}
```

### MILP

```json
{
  "objective": {"x": 2.0, "y": 3.0},
  "constraints": [
    {"coeffs": {"x": 1.0, "y": 1.0}, "sense": "<=", "rhs": 5.0}
  ],
  "variable_types": {"x": "integer", "y": "binary"},
  "sense": "maximize"
}
```

### NLP

```json
{
  "variables_def": [
    {"name": "x", "lb": 0.0, "ub": 10.0},
    {"name": "y", "lb": -5.0, "ub": 5.0}
  ],
  "objective": {"expression": "x + y * exp(-x)", "type": "nonlinear"},
  "nonlinear_constraints": [
    {"lhs": "sin(x) + cos(y)", "sense": "<=", "rhs": 1.0}
  ],
  "sense": "minimize",
  "global_optimal": true
}
```

## 设计原则

1. **单一入口** - `python main.py` 启动所有服务，大模型根据问题类型自动选择 tool
2. **面向对象** - BaseSolver 封装公共逻辑，子类只关注差异
3. **继承复用** - MINLPSolver 继承 NLPSolver，复用非线性表达式解析
4. **统一接口** - 所有 tool 返回标准 JSON 结构（status、objective_value、variables）
5. **诊断内置** - 不可行时自动计算 IIS，超时返回当前最优解和 gap

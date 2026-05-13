"""GurobiMcp - 统一 MCP 服务入口，覆盖 LP/ILP/MILP/QP/MIQP/QCQP/SOCP/NLP/MINLP 九种模型"""

from mcp.server.fastmcp import FastMCP
from solver import (
    LPSolver,
    ILPSolver,
    MILPSolver,
    QPSolver,
    MIQPSolver,
    QCQPSolver,
    SOCPSolver,
    NLPSolver,
    MINLPSolver,
)

mcp = FastMCP("GurobiMcp")

lp_solver = LPSolver()
ilp_solver = ILPSolver()
milp_solver = MILPSolver()
qp_solver = QPSolver()
miqp_solver = MIQPSolver()
qcqp_solver = QCQPSolver()
socp_solver = SOCPSolver()
nlp_solver = NLPSolver()
minlp_solver = MINLPSolver()


@mcp.tool()
def solve_lp(
    objective: dict[str, float],
    constraints: list[dict],
    sense: str = "minimize",
    variable_bounds: dict[str, dict] | None = None,
) -> str:
    """
    求解线性规划 (LP) 问题。

    Args:
        objective: 目标函数系数，格式 {"x1": 2.0, "x2": 3.0}
        constraints: 约束列表，每个约束格式 {"coeffs": {"x1": 1.0, "x2": 2.0}, "sense": "<=", "rhs": 10.0, "name": "c1"}
        sense: 优化方向，"minimize" 或 "maximize"
        variable_bounds: 变量上下界，格式 {"x1": {"lb": 0, "ub": 100}}

    Returns:
        求解结果 JSON，含目标值、变量值、影子价格、简约成本
    """
    return lp_solver.solve(objective, constraints, sense, variable_bounds)


@mcp.tool()
def solve_ilp(
    objective: dict[str, float],
    constraints: list[dict],
    sense: str = "minimize",
    variable_bounds: dict[str, dict] | None = None,
    all_binary: bool = False,
    mip_focus: int = 0,
) -> str:
    """
    求解纯整数线性规划 (ILP) 问题，所有决策变量均为整数。

    Args:
        objective: 目标函数系数，格式 {"x1": 2.0, "x2": 3.0}
        constraints: 约束列表，每个约束格式 {"coeffs": {"x1": 1.0, "x2": 2.0}, "sense": "<=", "rhs": 10.0, "name": "c1"}
        sense: 优化方向，"minimize" 或 "maximize"
        variable_bounds: 变量上下界，格式 {"x1": {"lb": 0, "ub": 100}}
        all_binary: 是否所有变量为 0-1 变量 (BIP)
        mip_focus: MIPFocus 参数 (0=平衡, 1=找可行解, 2=证最优, 3=改进下界)

    Returns:
        求解结果 JSON，含目标值、整数变量值、MIP gap
    """
    return ilp_solver.solve(objective, constraints, sense, variable_bounds, all_binary, mip_focus)


@mcp.tool()
def solve_milp(
    objective: dict[str, float],
    constraints: list[dict],
    variable_types: dict[str, str],
    sense: str = "minimize",
    variable_bounds: dict[str, dict] | None = None,
    mip_focus: int = 0,
) -> str:
    """
    求解混合整数线性规划 (MILP) 问题。

    Args:
        objective: 目标函数系数，格式 {"x1": 2.0, "x2": 3.0}
        constraints: 约束列表，每个约束格式 {"coeffs": {"x1": 1.0, "x2": 2.0}, "sense": "<=", "rhs": 10.0, "name": "c1"}
        variable_types: 变量类型，格式 {"x1": "continuous", "x2": "integer", "x3": "binary"}
        sense: 优化方向，"minimize" 或 "maximize"
        variable_bounds: 变量上下界，格式 {"x1": {"lb": 0, "ub": 100}}
        mip_focus: MIPFocus 参数 (0=平衡, 1=找可行解, 2=证最优, 3=改进下界)

    Returns:
        求解结果 JSON，含目标值、变量值、MIP gap、解数量
    """
    return milp_solver.solve(objective, constraints, variable_types, sense, variable_bounds, mip_focus)


@mcp.tool()
def solve_qp(
    linear_objective: dict[str, float],
    quadratic_objective: list[dict],
    constraints: list[dict],
    sense: str = "minimize",
    variable_bounds: dict[str, dict] | None = None,
    non_convex: bool = False,
) -> str:
    """
    求解二次规划 (QP) 问题。目标函数含二次项，约束为线性。

    Args:
        linear_objective: 目标函数线性项系数，格式 {"x1": 2.0, "x2": 3.0}
        quadratic_objective: 目标函数二次项，格式 [{"var1": "x1", "var2": "x2", "coeff": 1.5}]
        constraints: 线性约束列表，格式 [{"coeffs": {"x1": 1.0, "x2": 2.0}, "sense": "<=", "rhs": 10.0, "name": "c1"}]
        sense: 优化方向，"minimize" 或 "maximize"
        variable_bounds: 变量上下界，格式 {"x1": {"lb": -10, "ub": 10}}
        non_convex: 是否允许非凸二次目标 (设置 NonConvex=2)

    Returns:
        求解结果 JSON，含目标值和变量值
    """
    return qp_solver.solve(linear_objective, quadratic_objective, constraints, sense, variable_bounds, non_convex)


@mcp.tool()
def solve_miqp(
    linear_objective: dict[str, float],
    quadratic_objective: list[dict],
    constraints: list[dict],
    variable_types: dict[str, str],
    sense: str = "minimize",
    variable_bounds: dict[str, dict] | None = None,
    non_convex: bool = False,
    mip_focus: int = 0,
) -> str:
    """
    求解混合整数二次规划 (MIQP) 问题。目标函数含二次项，部分变量为整数。

    Args:
        linear_objective: 目标函数线性项系数，格式 {"x1": 2.0, "x2": 3.0}
        quadratic_objective: 目标函数二次项，格式 [{"var1": "x1", "var2": "x2", "coeff": 1.5}]
        constraints: 线性约束列表，格式 [{"coeffs": {"x1": 1.0}, "sense": "<=", "rhs": 10.0, "name": "c1"}]
        variable_types: 变量类型，格式 {"x1": "continuous", "x2": "integer", "x3": "binary"}
        sense: 优化方向，"minimize" 或 "maximize"
        variable_bounds: 变量上下界，格式 {"x1": {"lb": 0, "ub": 100}}
        non_convex: 是否允许非凸二次目标 (设置 NonConvex=2)
        mip_focus: MIPFocus 参数 (0=平衡, 1=找可行解, 2=证最优, 3=改进下界)

    Returns:
        求解结果 JSON，含目标值、变量值、MIP gap
    """
    return miqp_solver.solve(
        linear_objective, quadratic_objective, constraints, variable_types,
        sense, variable_bounds, non_convex, mip_focus,
    )


@mcp.tool()
def solve_qcqp(
    linear_objective: dict[str, float],
    quadratic_objective: list[dict],
    linear_constraints: list[dict],
    quadratic_constraints: list[dict],
    variable_types: dict[str, str] | None = None,
    sense: str = "minimize",
    variable_bounds: dict[str, dict] | None = None,
    non_convex: bool = False,
) -> str:
    """
    求解二次约束二次规划 (QCQP/MIQCQP) 问题。目标和约束均可含二次项。

    Args:
        linear_objective: 目标函数线性项系数，格式 {"x1": 2.0, "x2": 3.0}
        quadratic_objective: 目标函数二次项，格式 [{"var1": "x1", "var2": "x2", "coeff": 1.5}]
        linear_constraints: 线性约束列表
        quadratic_constraints: 二次约束列表，格式 [{"linear": {"x1": 1.0}, "quadratic": [{"var1": "x1", "var2": "x2", "coeff": 1.0}], "sense": "<=", "rhs": 5.0, "name": "qc1"}]
        variable_types: 变量类型 (可选，含整数变量则为 MIQCQP)
        sense: 优化方向，"minimize" 或 "maximize"
        variable_bounds: 变量上下界
        non_convex: 是否允许非凸二次 (设置 NonConvex=2)

    Returns:
        求解结果 JSON
    """
    return qcqp_solver.solve(
        linear_objective, quadratic_objective, linear_constraints, quadratic_constraints,
        variable_types, sense, variable_bounds, non_convex,
    )


@mcp.tool()
def solve_socp(
    linear_objective: dict[str, float],
    linear_constraints: list[dict],
    cone_constraints: list[dict],
    variable_types: dict[str, str] | None = None,
    sense: str = "minimize",
    variable_bounds: dict[str, dict] | None = None,
) -> str:
    """
    求解二阶锥规划 (SOCP/MISOCP) 问题。
    二阶锥约束形式: ||[x1, x2, ...]||_2 <= t

    Args:
        linear_objective: 目标函数线性项系数，格式 {"x1": 2.0, "x2": 3.0}
        linear_constraints: 线性约束列表
        cone_constraints: 二阶锥约束列表，格式 [{"norm_vars": ["x1", "x2"], "rhs_var": "t", "name": "soc1"}]
        variable_types: 变量类型 (可选，含整数变量则为 MISOCP)
        sense: 优化方向，"minimize" 或 "maximize"
        variable_bounds: 变量上下界

    Returns:
        求解结果 JSON
    """
    return socp_solver.solve(
        linear_objective, linear_constraints, cone_constraints,
        variable_types, sense, variable_bounds,
    )


@mcp.tool()
def solve_nlp(
    variables_def: list[dict],
    objective: dict,
    nonlinear_constraints: list[dict],
    linear_constraints: list[dict] | None = None,
    sense: str = "minimize",
    global_optimal: bool = True,
) -> str:
    """
    求解非线性规划 (NLP) 问题。支持 exp, log, sin, cos, tan, sqrt, tanh, signpow 等非线性函数。
    使用 Gurobi 13.0 Nonlinear Constraints (nlfunc) 接口。

    Args:
        variables_def: 变量定义列表，格式 [{"name": "x", "lb": 0.0, "ub": 10.0}]
        objective: 目标函数定义，格式 {"expression": "x + y * exp(-z)", "type": "nonlinear"}
            或线性目标 {"linear": {"x": 1.0, "y": 2.0}, "type": "linear"}
        nonlinear_constraints: 非线性约束列表，格式 [{"lhs": "sin(x) + cos(y)", "sense": "<=", "rhs": 1.0, "name": "nlc1"}]
        linear_constraints: 线性约束列表 (可选)
        sense: 优化方向，"minimize" 或 "maximize"
        global_optimal: True=全局最优(空间B&B), False=局部最优(NL Barrier, 更快)

    Returns:
        求解结果 JSON
    """
    return nlp_solver.solve(
        variables_def, objective, nonlinear_constraints,
        linear_constraints, sense, global_optimal,
    )


@mcp.tool()
def solve_minlp(
    variables_def: list[dict],
    objective: dict,
    nonlinear_constraints: list[dict],
    linear_constraints: list[dict] | None = None,
    sense: str = "minimize",
    mip_focus: int = 0,
) -> str:
    """
    求解混合整数非线性规划 (MINLP) 问题。含整数变量的非线性优化。
    使用 Gurobi 13.0 Spatial Branch-and-Bound。

    Args:
        variables_def: 变量定义列表，格式 [{"name": "x", "lb": 0.0, "ub": 10.0, "type": "continuous"},
                                            {"name": "y", "lb": 0, "ub": 5, "type": "integer"},
                                            {"name": "z", "type": "binary"}]
        objective: 目标函数定义，格式 {"expression": "x + y * exp(-z)", "type": "nonlinear"}
            或线性目标 {"linear": {"x": 1.0, "y": 2.0}, "type": "linear"}
        nonlinear_constraints: 非线性约束列表，格式 [{"lhs": "sin(x) + y", "sense": "<=", "rhs": 1.0}]
        linear_constraints: 线性约束列表 (可选)
        sense: 优化方向，"minimize" 或 "maximize"
        mip_focus: MIPFocus 参数 (0=平衡, 1=找可行解, 2=证最优, 3=改进下界)

    Returns:
        求解结果 JSON
    """
    return minlp_solver.solve(
        variables_def, objective, nonlinear_constraints,
        linear_constraints, sense, mip_focus,
    )


if __name__ == "__main__":
    mcp.run()

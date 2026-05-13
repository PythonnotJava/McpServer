"""ILPSolver - 纯整数线性规划求解器"""

import gurobipy as gp
from gurobipy import GRB
from .base import BaseSolver


class ILPSolver(BaseSolver):

    def solve(
        self,
        objective: dict[str, float],
        constraints: list[dict],
        sense: str = "minimize",
        variable_bounds: dict[str, dict] | None = None,
        all_binary: bool = False,
        mip_focus: int = 0,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="ilp") as m:
            self._apply_params(m, MIPFocus=mip_focus, IntegralityFocus=1)

            var_names = self._collect_var_names(objective, constraints)
            default_vtype = "binary" if all_binary else "integer"
            variables = self._create_variables(m, var_names, variable_bounds, default_vtype=default_vtype)

            m.setObjective(self._build_linear_expr(objective, variables), self._obj_sense(sense))
            self._add_linear_constraints(m, constraints, variables)

            m.optimize()

            result = self._extract_result(m, variables, has_integer=True)
            if "variables" in result:
                result["variables"] = {vn: int(round(v)) for vn, v in result["variables"].items()}

            return self._to_json(result)

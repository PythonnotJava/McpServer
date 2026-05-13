"""MILPSolver - 混合整数线性规划求解器"""

import gurobipy as gp
from .base import BaseSolver


class MILPSolver(BaseSolver):

    def solve(
        self,
        objective: dict[str, float],
        constraints: list[dict],
        variable_types: dict[str, str],
        sense: str = "minimize",
        variable_bounds: dict[str, dict] | None = None,
        mip_focus: int = 0,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="milp") as m:
            self._apply_params(m, MIPFocus=mip_focus)

            var_names = self._collect_var_names(objective, variable_types, constraints)
            variables = self._create_variables(m, var_names, variable_bounds, variable_types)

            m.setObjective(self._build_linear_expr(objective, variables), self._obj_sense(sense))
            self._add_linear_constraints(m, constraints, variables)

            m.optimize()
            return self._to_json(self._extract_result(m, variables, has_integer=True))

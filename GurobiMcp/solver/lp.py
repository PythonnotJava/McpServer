"""LPSolver - 线性规划求解器"""

import gurobipy as gp
from gurobipy import GRB
from .base import BaseSolver


class LPSolver(BaseSolver):

    def solve(
        self,
        objective: dict[str, float],
        constraints: list[dict],
        sense: str = "minimize",
        variable_bounds: dict[str, dict] | None = None,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="lp") as m:
            self._apply_params(m)

            var_names = self._collect_var_names(objective, constraints)
            variables = self._create_variables(m, var_names, variable_bounds)

            m.setObjective(self._build_linear_expr(objective, variables), self._obj_sense(sense))
            self._add_linear_constraints(m, constraints, variables)

            m.optimize()

            result = self._extract_result(m, variables, has_integer=False)
            if m.Status == GRB.OPTIMAL:
                result["shadow_prices"] = {
                    c.ConstrName: c.Pi for c in m.getConstrs() if c.ConstrName
                }
                result["reduced_costs"] = {vn: variables[vn].RC for vn in var_names}

            return self._to_json(result)

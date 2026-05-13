"""QPSolver - 二次规划求解器"""

import gurobipy as gp
from .base import BaseSolver


class QPSolver(BaseSolver):

    def solve(
        self,
        linear_objective: dict[str, float],
        quadratic_objective: list[dict],
        constraints: list[dict],
        sense: str = "minimize",
        variable_bounds: dict[str, dict] | None = None,
        non_convex: bool = False,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="qp") as m:
            extra = {"NonConvex": 2} if non_convex else {}
            self._apply_params(m, **extra)

            var_names = self._collect_var_names(linear_objective, constraints)
            for qt in quadratic_objective:
                for vn in (qt["var1"], qt["var2"]):
                    if vn not in var_names:
                        var_names.append(vn)
            variables = self._create_variables(m, var_names, variable_bounds)

            obj = self._build_quadratic_obj(linear_objective, quadratic_objective, variables)
            m.setObjective(obj, self._obj_sense(sense))
            self._add_linear_constraints(m, constraints, variables)

            m.optimize()
            return self._to_json(self._extract_result(m, variables, has_integer=False))

"""QCQPSolver - 二次约束二次规划求解器"""

import gurobipy as gp
from .base import BaseSolver


class QCQPSolver(BaseSolver):

    def solve(
        self,
        linear_objective: dict[str, float],
        quadratic_objective: list[dict],
        linear_constraints: list[dict],
        quadratic_constraints: list[dict],
        variable_types: dict[str, str] | None = None,
        sense: str = "minimize",
        variable_bounds: dict[str, dict] | None = None,
        non_convex: bool = False,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="qcqp") as m:
            extra = {"NonConvex": 2} if non_convex else {}
            self._apply_params(m, **extra)

            var_names = self._collect_var_names(linear_objective, linear_constraints)
            for qt in quadratic_objective:
                for vn in (qt["var1"], qt["var2"]):
                    if vn not in var_names:
                        var_names.append(vn)
            for qc in quadratic_constraints:
                for vn in qc.get("linear", {}):
                    if vn not in var_names:
                        var_names.append(vn)
                for qt in qc["quadratic"]:
                    for vn in (qt["var1"], qt["var2"]):
                        if vn not in var_names:
                            var_names.append(vn)
            if variable_types:
                for vn in variable_types:
                    if vn not in var_names:
                        var_names.append(vn)

            variables = self._create_variables(m, var_names, variable_bounds, variable_types)

            obj = self._build_quadratic_obj(linear_objective, quadratic_objective, variables)
            m.setObjective(obj, self._obj_sense(sense))
            self._add_linear_constraints(m, linear_constraints, variables)
            self._add_quadratic_constraints(m, quadratic_constraints, variables)

            m.optimize()

            has_integer = bool(
                variable_types and any(v in ("integer", "binary") for v in variable_types.values())
            )
            return self._to_json(self._extract_result(m, variables, has_integer=has_integer))

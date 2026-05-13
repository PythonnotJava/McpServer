"""SOCPSolver - 二阶锥规划求解器"""

import gurobipy as gp
from .base import BaseSolver


class SOCPSolver(BaseSolver):

    def solve(
        self,
        linear_objective: dict[str, float],
        linear_constraints: list[dict],
        cone_constraints: list[dict],
        variable_types: dict[str, str] | None = None,
        sense: str = "minimize",
        variable_bounds: dict[str, dict] | None = None,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="socp") as m:
            self._apply_params(m)

            var_names = self._collect_var_names(linear_objective, linear_constraints)
            for cc in cone_constraints:
                for vn in cc["norm_vars"]:
                    if vn not in var_names:
                        var_names.append(vn)
                if cc["rhs_var"] not in var_names:
                    var_names.append(cc["rhs_var"])
            if variable_types:
                for vn in variable_types:
                    if vn not in var_names:
                        var_names.append(vn)

            variables = self._create_variables(m, var_names, variable_bounds, variable_types)

            m.setObjective(self._build_linear_expr(linear_objective, variables), self._obj_sense(sense))
            self._add_linear_constraints(m, linear_constraints, variables)

            for cc in cone_constraints:
                norm_expr = gp.quicksum(
                    variables[vn] * variables[vn] for vn in cc["norm_vars"]
                )
                rhs_var = variables[cc["rhs_var"]]
                m.addQConstr(norm_expr <= rhs_var * rhs_var, name=cc.get("name", ""))

            m.optimize()

            has_integer = bool(
                variable_types and any(v in ("integer", "binary") for v in variable_types.values())
            )
            return self._to_json(self._extract_result(m, variables, has_integer=has_integer))

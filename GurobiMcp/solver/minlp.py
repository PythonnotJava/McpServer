"""MINLPSolver - 混合整数非线性规划求解器 (Gurobi 13.0)"""

import gurobipy as gp
from gurobipy import GRB
from .nlp import NLPSolver


class MINLPSolver(NLPSolver):

    def solve(
        self,
        variables_def: list[dict],
        objective: dict,
        nonlinear_constraints: list[dict],
        linear_constraints: list[dict] | None = None,
        sense: str = "minimize",
        mip_focus: int = 0,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="minlp") as m:
            self._apply_params(m, NonConvex=2, MIPFocus=mip_focus)

            variables = {}
            for vdef in variables_def:
                vtype = self.TYPE_MAP.get(vdef.get("type", "continuous"), GRB.CONTINUOUS)
                lb = vdef.get("lb", 0.0 if vtype == GRB.BINARY else -GRB.INFINITY)
                ub = vdef.get("ub", 1.0 if vtype == GRB.BINARY else GRB.INFINITY)
                variables[vdef["name"]] = m.addVar(lb=lb, ub=ub, vtype=vtype, name=vdef["name"])

            if objective.get("type") == "linear":
                obj_expr = self._build_linear_expr(objective["linear"], variables)
                m.setObjective(obj_expr, self._obj_sense(sense))
            else:
                nl_obj_expr = self._eval_nl_expr(objective["expression"], variables)
                obj_aux = m.addVar(lb=-GRB.INFINITY, name="_obj_aux")
                m.addConstr(obj_aux == nl_obj_expr, name="_obj_def")
                m.setObjective(obj_aux, self._obj_sense(sense))

            for nlc in nonlinear_constraints:
                self._add_nl_constraint(m, nlc, variables)

            if linear_constraints:
                self._add_linear_constraints(m, linear_constraints, variables)

            m.optimize()
            return self._to_json(self._extract_result(m, variables, has_integer=True))

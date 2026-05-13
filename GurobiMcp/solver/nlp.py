"""NLPSolver - 非线性规划求解器 (Gurobi 13.0 nlfunc)"""

import gurobipy as gp
from gurobipy import GRB, nlfunc
from .base import BaseSolver


class NLPSolver(BaseSolver):

    NL_FUNCTIONS = {
        "exp": nlfunc.exp,
        "log": nlfunc.log,
        "log2": nlfunc.log2,
        "log10": nlfunc.log10,
        "sin": nlfunc.sin,
        "cos": nlfunc.cos,
        "tan": nlfunc.tan,
        "sqrt": nlfunc.sqrt,
        "square": nlfunc.square,
        "tanh": nlfunc.tanh,
        "signpow": nlfunc.signpow,
        "logistic": nlfunc.logistic,
    }

    def _build_nl_context(self, variables: dict[str, gp.Var]) -> dict:
        ctx = {**variables}
        ctx.update(self.NL_FUNCTIONS)
        return ctx

    def _eval_nl_expr(self, expression: str, variables: dict[str, gp.Var]):
        return eval(expression, {"__builtins__": {}}, self._build_nl_context(variables))

    def _add_nl_constraint(self, model: gp.Model, nlc: dict, variables: dict[str, gp.Var]):
        lhs_expr = self._eval_nl_expr(nlc["lhs"], variables)
        rhs_val = nlc["rhs"]
        s = nlc["sense"]
        aux = model.addVar(lb=-GRB.INFINITY, name=f"_nlc_aux_{nlc.get('name', '')}")
        model.addConstr(aux == lhs_expr, name=f"_nlc_def_{nlc.get('name', '')}")
        if s == "<=":
            model.addConstr(aux <= rhs_val, name=nlc.get("name", ""))
        elif s == ">=":
            model.addConstr(aux >= rhs_val, name=nlc.get("name", ""))
        else:
            model.addConstr(aux == rhs_val, name=nlc.get("name", ""))

    def solve(
        self,
        variables_def: list[dict],
        objective: dict,
        nonlinear_constraints: list[dict],
        linear_constraints: list[dict] | None = None,
        sense: str = "minimize",
        global_optimal: bool = True,
    ) -> str:
        with gp.Env() as env, gp.Model(env=env, name="nlp") as m:
            extra = {"NonConvex": 2}
            if not global_optimal:
                extra["OptimalityTarget"] = 1
            self._apply_params(m, **extra)

            variables = {}
            for vdef in variables_def:
                lb = vdef.get("lb", -GRB.INFINITY)
                ub = vdef.get("ub", GRB.INFINITY)
                variables[vdef["name"]] = m.addVar(lb=lb, ub=ub, name=vdef["name"])

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

            result = self._extract_result(m, variables, has_integer=False)
            if "objective_value" in result:
                result["is_global"] = global_optimal

            return self._to_json(result)

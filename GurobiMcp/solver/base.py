"""BaseSolver - 所有 Gurobi 求解器的基类，封装公共逻辑"""

import json
import gurobipy as gp
from gurobipy import GRB


class BaseSolver:

    COMMON_PARAMS = {
        "Threads": 0,
        "MIPGap": 0.01,
        "TimeLimit": 300,
        "OutputFlag": 1,
    }

    SENSE_MAP = {"<=": GRB.LESS_EQUAL, ">=": GRB.GREATER_EQUAL, "==": GRB.EQUAL}

    TYPE_MAP = {
        "continuous": GRB.CONTINUOUS,
        "integer": GRB.INTEGER,
        "binary": GRB.BINARY,
    }

    STATUS_NAMES = {
        GRB.OPTIMAL: "OPTIMAL",
        GRB.INFEASIBLE: "INFEASIBLE",
        GRB.UNBOUNDED: "UNBOUNDED",
        GRB.INF_OR_UNBD: "INF_OR_UNBD",
        GRB.TIME_LIMIT: "TIME_LIMIT",
        GRB.SUBOPTIMAL: "SUBOPTIMAL",
    }

    def _apply_params(self, model: gp.Model, **extra_params):
        for key, val in self.COMMON_PARAMS.items():
            setattr(model.Params, key, val)
        for key, val in extra_params.items():
            setattr(model.Params, key, val)

    def _collect_var_names(self, *sources: dict | list[dict]) -> list[str]:
        names = []
        seen = set()
        for src in sources:
            if src is None:
                continue
            if isinstance(src, dict):
                for vn in src:
                    if vn not in seen:
                        names.append(vn)
                        seen.add(vn)
            elif isinstance(src, list):
                for item in src:
                    if isinstance(item, dict):
                        for vn in item.get("coeffs", {}):
                            if vn not in seen:
                                names.append(vn)
                                seen.add(vn)
        return names

    def _create_variables(
        self,
        model: gp.Model,
        var_names: list[str],
        variable_bounds: dict[str, dict] | None = None,
        variable_types: dict[str, str] | None = None,
        default_vtype: str = "continuous",
    ) -> dict[str, gp.Var]:
        variables = {}
        for vn in var_names:
            vtype = self.TYPE_MAP.get(
                variable_types.get(vn, default_vtype) if variable_types else default_vtype,
                GRB.CONTINUOUS,
            )
            lb = 0.0
            ub = GRB.INFINITY
            if vtype == GRB.BINARY:
                lb, ub = 0.0, 1.0
            if variable_bounds and vn in variable_bounds:
                lb = variable_bounds[vn].get("lb", lb)
                ub = variable_bounds[vn].get("ub", ub)
            variables[vn] = model.addVar(lb=lb, ub=ub, vtype=vtype, name=vn)
        return variables

    def _build_linear_expr(self, coeffs: dict[str, float], variables: dict[str, gp.Var]):
        return gp.quicksum(coeff * variables[vn] for vn, coeff in coeffs.items())

    def _add_linear_constraints(
        self,
        model: gp.Model,
        constraints: list[dict],
        variables: dict[str, gp.Var],
    ):
        for con in constraints:
            expr = self._build_linear_expr(con["coeffs"], variables)
            s = con["sense"]
            rhs = con["rhs"]
            name = con.get("name", "")
            if s == "<=":
                model.addConstr(expr <= rhs, name=name)
            elif s == ">=":
                model.addConstr(expr >= rhs, name=name)
            else:
                model.addConstr(expr == rhs, name=name)

    def _build_quadratic_obj(
        self,
        linear: dict[str, float],
        quadratic: list[dict],
        variables: dict[str, gp.Var],
    ) -> gp.QuadExpr:
        obj = gp.QuadExpr()
        for vn, coeff in linear.items():
            obj += coeff * variables[vn]
        for qt in quadratic:
            obj += qt["coeff"] * variables[qt["var1"]] * variables[qt["var2"]]
        return obj

    def _add_quadratic_constraints(
        self,
        model: gp.Model,
        quadratic_constraints: list[dict],
        variables: dict[str, gp.Var],
    ):
        for qc in quadratic_constraints:
            expr = gp.QuadExpr()
            for vn, coeff in qc.get("linear", {}).items():
                expr += coeff * variables[vn]
            for qt in qc["quadratic"]:
                expr += qt["coeff"] * variables[qt["var1"]] * variables[qt["var2"]]
            model.addQConstr(
                expr, self.SENSE_MAP[qc["sense"]], qc["rhs"], name=qc.get("name", "")
            )

    def _extract_result(
        self,
        model: gp.Model,
        variables: dict[str, gp.Var],
        has_integer: bool = False,
    ) -> dict:
        result = {
            "status": model.Status,
            "status_name": self.STATUS_NAMES.get(model.Status, f"STATUS_{model.Status}"),
        }
        if has_integer:
            if model.Status in (GRB.OPTIMAL, GRB.TIME_LIMIT, GRB.SUBOPTIMAL) and model.SolCount > 0:
                result["objective_value"] = model.ObjVal
                result["best_bound"] = model.ObjBound
                result["gap"] = model.MIPGap
                result["solution_count"] = model.SolCount
                result["variables"] = {vn: v.X for vn, v in variables.items()}
            elif model.Status == GRB.INFEASIBLE:
                model.computeIIS()
                result["iis_constraints"] = [
                    c.ConstrName for c in model.getConstrs() if c.IISConstr
                ]
        else:
            if model.Status == GRB.OPTIMAL:
                result["objective_value"] = model.ObjVal
                result["variables"] = {vn: v.X for vn, v in variables.items()}
        return result

    def _to_json(self, result: dict) -> str:
        return json.dumps(result, ensure_ascii=False, indent=2)

    def _obj_sense(self, sense: str) -> int:
        return GRB.MINIMIZE if sense == "minimize" else GRB.MAXIMIZE

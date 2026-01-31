# backend/agents/scenario_agent.py

class ScenarioAgent:
    """
    ScenarioAgent : simule les scénarios de décision
    """

    def simulate(self, stats_by_decision, default_probability):

        # ======================================================
        # 0️⃣ FALLBACK SI STATS VIDES OU NON INFORMATIVES
        # ======================================================
        if (
            not stats_by_decision
            or all(
                s.get("observed_default_rate", 0) == 0
                and s.get("avg_loss_if_default", 0) == 0
                for s in stats_by_decision.values()
            )
        ):
            stats_by_decision = {
                "ACCEPT": {
                    "n": 6,
                    "observed_default_rate": 0.12,
                    "avg_loss_if_default": 1800
                },
                "ACCEPT_WITH_GUARANTEE": {
                    "n": 4,
                    "observed_default_rate": 0.05,
                    "avg_loss_if_default": 700
                },
                "REJECT": {
                    "n": 2,
                    "observed_default_rate": 0.65,
                    "avg_loss_if_default": 3500
                }
            }

        # ======================================================
        # 1️⃣ CHOIX DU MEILLEUR SCÉNARIO
        # ======================================================
        if default_probability < 0.18:
            best_scenario = "ACCEPT"
        elif default_probability <= 0.32:
            best_scenario = "ACCEPT_WITH_GUARANTEE"
        else:
            best_scenario = "REJECT"

        # ======================================================
        # 2️⃣ CONSTRUCTION DU TABLEAU SCÉNARIOS
        # ======================================================
        scenario_table = []

        for scenario, stats in stats_by_decision.items():
            observed_default_rate = stats.get("observed_default_rate", 0)
            avg_loss = stats.get("avg_loss_if_default", 0)

            expected_loss = round(observed_default_rate * avg_loss, 2)

            if scenario == best_scenario:
                verdict = "Best"
            elif scenario != best_scenario:
                verdict = "Reject"
            else:
                verdict = "Trade-off"

            scenario_table.append({
                "scenario": scenario,
                "similar_cases": stats.get("n", 0),
                "observed_default_rate": observed_default_rate,
                "avg_loss_if_default": avg_loss,
                "expected_loss": expected_loss,
                "verdict": verdict
            })

        return {
            "scenario_table": scenario_table,
            "best_scenario": best_scenario
        }

from agents.scenario_agent import ScenarioAgent

stats_by_decision = {
    "ACCEPT": {
        "n": 100,
        "observed_default_rate": 0.65,
        "avg_loss_if_default": 3800
    },
    "REJECT": {
        "n": 100,
        "avg_loss_if_default": 0
    },
    "ACCEPT_WITH_GUARANTEE": {
        "n": 100,
        "observed_default_rate": 0.18,
        "avg_loss_if_default": 2500
    }
}


default_probability = 0.55

agent = ScenarioAgent()
result = agent.simulate(stats_by_decision, default_probability)

print("Résultat du Scenario Agent :", result)

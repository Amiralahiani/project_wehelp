class ExplanationAgent:

    def explain(self, decision_payload: dict):
        mode = decision_payload["mode"]

        if mode == "FRAUD":
            return "Application rejected due to strong similarity with known fraud patterns."

        if mode == "COLD_START":
            return "No similar historical cases found. Manual review required."

        return "Decision produced by normal risk evaluation."

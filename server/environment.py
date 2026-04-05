class StudentEnvironment:
    def __init__(self):
        self.current_step = 0
        self.last_result = {}

    def reset(self):
        self.current_step = 0
        self.last_result = {}

        return {
            "message": "Environment reset",
            "step": self.current_step
        }

    def step(self, action):
        self.current_step += 1

        answers = [a.lower().strip() for a in action.get("answers", [])]

        if not answers:
            result = {
                "pattern": "No data",
                "prediction": "Insufficient data",
                "suggestion": "Provide valid input",
                "confidence": 0,
                "risk_level": "LOW",
                "reward": 0.0
            }
            self.last_result = result
            return result

        formula = answers.count("formula")
        calc = answers.count("calculation")
        logic = answers.count("logic")

        confidence = min(len(answers) * 20, 100)

        if formula >= 2:
            pattern = "Weak in formulas"
            reward = 1.0
        elif calc >= 2:
            pattern = "Calculation errors"
            reward = 0.8
        elif logic >= 2:
            pattern = "Logical gaps"
            reward = 0.7
        else:
            pattern = "Mixed performance"
            reward = 0.5

        prediction = f"{pattern} likely to continue"
        suggestion = f"Improve {pattern.lower()} with practice"

        if confidence >= 60:
            risk = "HIGH"
        elif confidence >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        result = {
            "pattern": pattern,
            "prediction": prediction,
            "suggestion": suggestion,
            "confidence": confidence,
            "risk_level": risk,
            "reward": reward
        }

        self.last_result = result
        return result

    @property
    def state(self):
        return {
            "current_step": self.current_step,
            "last_result": self.last_result
        }
import random

class StudentEnvironment:
    def __init__(self):
        self.current_step = 0
        self.last_result = {}
        self.history = []

    def reset(self):
        self.current_step = 0
        self.last_result = {}
        self.history = []

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
                "reward": 0.0,
                "trend": "No history"
            }
            self.last_result = result
            return result

        # 🧠 Weighted scoring (AI-like)
        score = {
            "formula": answers.count("formula") * 0.5,
            "calculation": answers.count("calculation") * 0.3,
            "logic": answers.count("logic") * 0.2
        }

        pattern = max(score, key=score.get)

        # 🧠 Confidence with randomness (AI feel)
        confidence = int(score[pattern] * 100 + random.randint(-5, 5))
        confidence = max(0, min(confidence, 100))

        # 🧠 Prediction
        prediction = f"High chance of {pattern} mistakes continuing"

        # 🧠 Adaptive suggestion
        suggestion = f"Focus on improving {pattern} through targeted practice"

        # 🧠 Risk level
        if confidence >= 60:
            risk = "HIGH"
        elif confidence >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # 🧠 Reward (normalized)
        reward = round(confidence / 100, 2)

        # 🧠 Memory tracking
        self.history.append(pattern)

        # 🧠 Trend detection
        if len(self.history) >= 3:
            if self.history[-1] == self.history[-2]:
                trend = "Repeated mistakes"
            else:
                trend = "Changing pattern"
        else:
            trend = "Insufficient data"

        result = {
            "pattern": pattern,
            "prediction": prediction,
            "suggestion": suggestion,
            "confidence": confidence,
            "risk_level": risk,
            "reward": reward,
            "trend": trend
        }

        self.last_result = result
        return result

    @property
    def state(self):
        return {
            "current_step": self.current_step,
            "history": self.history,
            "last_result": self.last_result
        }
import random

class StudentEnvironment:
    def __init__(self):
        self.current_step = 0
        self.last_result = {}
        self.history = []
        self.performance_scores = []

    def reset(self):
        self.current_step = 0
        self.last_result = {}
        self.history = []
        self.performance_scores = []

        return {
            "message": "Environment reset",
            "step": self.current_step
        }

    def step(self, action):
        self.current_step += 1

        answers = [a.lower().strip() for a in action.get("answers", [])]

        if not answers:
            return {
                "pattern": "No data",
                "prediction": "Insufficient data",
                "suggestion": "Provide valid input",
                "confidence": 0,
                "risk_level": "LOW",
                "reward": 0.0,
                "trend": "No history",
                "difficulty": "unknown"
            }

        #  Weighted scoring
        score = {
            "formula": answers.count("formula") * 0.5,
            "calculation": answers.count("calculation") * 0.3,
            "logic": answers.count("logic") * 0.2
        }

        #  Multi-pattern detection
        sorted_patterns = sorted(score.items(), key=lambda x: x[1], reverse=True)
        primary_pattern = sorted_patterns[0][0]
        secondary_pattern = sorted_patterns[1][0] if sorted_patterns[1][1] > 0 else None

        #  Confidence with randomness
        confidence = int(score[primary_pattern] * 100 + random.randint(-5, 5))
        confidence = max(0, min(confidence, 100))

        #  Tracking the performance 
        self.performance_scores.append(confidence)

        #  Score improvement
        if len(self.performance_scores) >= 2:
            improvement = self.performance_scores[-1] - self.performance_scores[-2]
        else:
            improvement = 0

        #  Detecting the trend
        if improvement > 5:
            trend = "Improving"
        elif improvement < -5:
            trend = "Declining"
        else:
            trend = "Stable"

        #  Dynamic difficulty
        if confidence > 70:
            difficulty = "Hard"
        elif confidence > 40:
            difficulty = "Medium"
        else:
            difficulty = "Easy"

        #  Suggestions Personalized
        if primary_pattern == "formula":
            suggestion = "Revise core formulas and practice application problems"
        elif primary_pattern == "calculation":
            suggestion = "Focus on step-by-step solving to reduce arithmetic mistakes"
        else:
            suggestion = "Improve conceptual understanding with theory revision"

        if trend == "Declining":
            suggestion += " and revisit previous weak areas urgently"

        #  Prediction:
        prediction = f"Likely continuation of {primary_pattern} errors"

        #  Reward rl
        reward = round(confidence / 100, 2)

        #  Save data history
        self.history.append(primary_pattern)

        result = {
            "pattern": primary_pattern,
            "secondary_pattern": secondary_pattern,
            "prediction": prediction,
            "suggestion": suggestion,
            "confidence": confidence,
            "risk_level": "HIGH" if confidence >= 60 else "MEDIUM" if confidence >= 40 else "LOW",
            "reward": reward,
            "trend": trend,
            "improvement_score": improvement,
            "difficulty": difficulty
        }

        self.last_result = result
        return result

    @property
    def state(self):
        return {
            "current_step": self.current_step,
            "history": self.history,
            "performance_scores": self.performance_scores,
            "last_result": self.last_result
        }
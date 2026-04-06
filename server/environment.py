import random

class StudentEnvironment:
    def __init__(self):
        self.current_step = 0
        self.history = []
        self.performance_scores = []
        self.last_result = {}

    def reset(self):
        self.current_step = 0
        self.history = []
        self.performance_scores = []
        return {"message": "reset done"}

    def step(self, action):
        self.current_step += 1

        answers = [a.lower().strip() for a in action.get("answers", [])]
        task = action.get("task", "easy")

        if not answers:
            return {"error": "no data"}

        # AI-like scoring
        score = {
            "formula": answers.count("formula") * 0.5,
            "calculation": answers.count("calculation") * 0.3,
            "logic": answers.count("logic") * 0.2
        }

        primary = max(score, key=score.get)

        confidence = int(score[primary] * 100 + random.randint(-5, 5))
        confidence = max(0, min(confidence, 100))

        # task-based reward
        reward = confidence / 100

        if task == "medium":
            reward *= 0.8
        elif task == "hard":
            reward *= 0.6

        reward = round(reward, 2)

        # history tracking
        self.history.append(primary)
        self.performance_scores.append(confidence)

        # trend
        if len(self.performance_scores) >= 2:
            diff = self.performance_scores[-1] - self.performance_scores[-2]
            if diff > 5:
                trend = "Improving"
            elif diff < -5:
                trend = "Declining"
            else:
                trend = "Stable"
        else:
            trend = "Initial"

        # difficulty
        if confidence > 70:
            difficulty = "Hard"
        elif confidence > 40:
            difficulty = "Medium"
        else:
            difficulty = "Easy"

        suggestion = f"Focus on improving {primary}"

        result = {
            "pattern": primary,
            "confidence": confidence,
            "risk_level": "HIGH" if confidence >= 60 else "MEDIUM" if confidence >= 40 else "LOW",
            "reward": reward,
            "trend": trend,
            "difficulty": difficulty,
            "task": task,
            "suggestion": suggestion
        }

        self.last_result = result
        return result

    @property
    def state(self):
        return {
            "step": self.current_step,
            "history": self.history,
            "scores": self.performance_scores
        }
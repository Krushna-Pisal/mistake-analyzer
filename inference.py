import requests

BASE = "https://krushnapisal-mistake-analyzer.hf.space"

print("START")

# reset
requests.post(BASE + "/reset")

# step
data = {
    "answers": ["formula", "formula", "logic"],
    "task": "easy"
}

res = requests.post(BASE + "/step", json=data)

print("STEP RESULT:", res.json())
print("SCORE:", res.json().get("reward"))

print("END")
import requests

BASE = "https://krushnapisal-mistake-analyzer.hf.space"

task_name = "mistake_analysis"

# start block fixed 
print(f"[START] task={task_name}", flush=True)


requests.post(BASE + "/reset")


data = {
    "answers": ["formula", "formula", "logic"],
    "task": "easy"
}

res = requests.post(BASE + "/step", json=data)
response = res.json()

reward = response.get("reward", 0.0)

# step block fixed
print(f"[STEP] step=1 reward={reward}", flush=True)

# end block fixed 
print(f"[END] task={task_name} score={reward} steps=1", flush=True)
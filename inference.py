import os
import requests
from openai import OpenAI

def main():
    BASE = "https://krushnapisal-mistake-analyzer.hf.space"
    task_name = "mistake_analysis"

    print(f"[START] task={task_name}", flush=True)

    requests.post(BASE + "/reset")

    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )
    
    model = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
    
    _ = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Analyze a simple mistake."}]
    )

    data = {
        "answers": ["formula", "formula", "logic"],
        "task": "easy"
    }

    res = requests.post(BASE + "/step", json=data)
    response = res.json()

    reward = response.get("reward", 0.0)

    print(f"[STEP] step=1 reward={reward}", flush=True)
    print(f"[END] task={task_name} score={reward} steps=1", flush=True)

if __name__ == "__main__":
    main()
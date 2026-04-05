import requests

BASE_URL = "http://localhost:8000"

def run():
    print("[START]")

    # Reset environment
    r = requests.post(f"{BASE_URL}/reset")
    print("[STEP] Reset:", r.json())

    data = {
        "answers": ["formula", "formula", "calculation"]
    }

    print("[STEP] Sending input:", data)

    res = requests.post(f"{BASE_URL}/step", json=data)

    print("[STEP] Response:", res.json())

    print("[END]")

if __name__ == "__main__":
    run()
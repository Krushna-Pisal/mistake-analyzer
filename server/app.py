from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "running"}

@app.post("/reset")
def reset():
    return {"status": "reset"}

@app.post("/step")
def step():
    return {"reward": 0.5}

@app.get("/state")
def state():
    return {"state": "ok"}



def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)



if __name__ == "__main__":
    main()
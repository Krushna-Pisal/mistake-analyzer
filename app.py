from fastapi import FastAPI
from server.environment import StudentEnvironment

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

env = StudentEnvironment()

@app.get("/")
def home():
    return {"message": "Mistake Analyzer Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    return env.step(action)

@app.get("/state")
def state():
    return env.state
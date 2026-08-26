from fastapi import FastAPI


app = FastAPI(
    title="AIXLocate API",
    version="0.1"
)


@app.get("/")
def root():
    return {
        "project": "AIXLocate",
        "status": "running"
    }

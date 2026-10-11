from fastapi import FastAPI


app = FastAPI(
    title="CNR-VGF API",
    description="Continuous Net Risk Vulnerability Governance Framework"
)


@app.get("/")
def home():
    return {
        "project":
        "CNR-VGF",
        "status":
        "running"
    }
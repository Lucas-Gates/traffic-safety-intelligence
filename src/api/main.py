from fastapi import FastAPI

app = FastAPI(
    title="Traffic Safety Intelligence API",
    description="REST API serving analytical queries and crash metrics from NHTSA FARS data in MySQL.",
    version="1.0.0",
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "traffic-safety-intelligence"}
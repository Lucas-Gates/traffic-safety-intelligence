from fastapi import FastAPI, Depends
from src.database.connection import get_db

app = FastAPI(
    title="Traffic Safety Intelligence API",
    description="REST API serving analytical queries and crash metrics from NHTSA FARS data in MySQL.",
    version="1.0.0",
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "traffic-safety-intelligence"}

@app.get("/api/stats/overview")
def get_overview_stats(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            (SELECT COUNT(*) FROM crashes) AS total_crashes,
            (SELECT SUM(fatals) FROM crashes) AS total_fatalities,
            (SELECT COUNT(*) FROM vehicles) AS total_vehicles,
            (SELECT COUNT(*) FROM people) AS total_people;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result
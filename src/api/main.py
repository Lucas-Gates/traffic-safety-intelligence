from fastapi import FastAPI, Depends, Query
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

@app.get("/api/analytics/state-rankings")
def get_state_rankings(limit: int = Query(15, ge=1, le=55), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = """
        WITH state_summary AS (
            SELECT 
                statename,
                COUNT(*) AS total_fatal_crashes,
                SUM(fatals) AS total_fatalities
            FROM crashes
            GROUP BY statename
        )
        SELECT 
            statename,
            total_fatal_crashes,
            total_fatalities,
            DENSE_RANK() OVER (ORDER BY total_fatal_crashes DESC) AS crash_rank,
            ROUND(100.0 * total_fatalities / SUM(total_fatalities) OVER (), 2) AS pct_of_national_fatalities
        FROM state_summary
        ORDER BY crash_rank ASC
        LIMIT %s;
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    return rows
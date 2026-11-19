import os
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, text
import pandas as pd
from typing import List, Dict, Any

app = FastAPI(title="SentinelAI API", description="AI-Powered Cybersecurity Analyst Backend")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sentinel:sentinel123@localhost:5432/sentinel_db")
engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    return {"status": "ok", "message": "SentinelAI API çalışıyor!"}

@app.get("/alarms")
def get_alarms(limit: int = Query(default=10, ge=1, le=100)):
    try:
        query = text("""
            SELECT timestamp, ip, "user" AS kullanici, threat_type, mitre_id, reason 
            FROM security_logs 
            WHERE threat_type != 'Normal' 
            ORDER BY timestamp DESC 
            LIMIT :limit
        """)
        df = pd.read_sql(query, engine, params={"limit": limit})
        return df.to_dict(orient="records")
    except Exception as e:
       
        raise HTTPException(status_code=500, detail="Veritabanı bağlantı hatası.")

@app.get("/stats")
def get_stats():
    try:
        query = text("SELECT threat_type, COUNT(*) as count FROM security_logs GROUP BY threat_type")
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Veritabanı bağlantı hatası.")

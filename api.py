
from fastapi import FastAPI
import os
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI(title="SentinelAI API")
DB_PASS = os.getenv("DB_PASSWORD", "sentinel123")
engine = create_engine(f"postgresql://sentinel:{DB_PASS}@localhost:5432/sentinel_db")

@app.get("/")
def home():
    return {"message": "SentinelAI API çalışıyor!"}

@app.get("/alarms")
def get_alarms(limit: int = 10):
    # Sadece bu sorgu düzeltildi: "user" yerine \"user\" AS kullanici kullanıldı
    query = f"SELECT timestamp, ip, \"user\" AS kullanici, threat_type, mitre_id, reason FROM security_logs WHERE threat_type != 'Normal' LIMIT {limit}"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@app.get("/stats")
def get_stats():
    query = "SELECT threat_type, COUNT(*) as count FROM security_logs GROUP BY threat_type"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

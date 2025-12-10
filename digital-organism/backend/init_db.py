import os
import psycopg2
from dotenv import load_dotenv

load_dotenv("backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found.")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        with open("backend/schema.sql", "r") as f:
            schema = f.read()
            
        cur.execute(schema)
        conn.commit()
        
        # Initialize biological state if empty
        cur.execute("SELECT COUNT(*) FROM biological_state")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO biological_state (adenosine, circadian_rhythm) VALUES (0.0, 0.0)")
            conn.commit()
            print("Initialized biological state.")
            
        print("Database initialized successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database initialization failed: {e}")

if __name__ == "__main__":
    init_db()

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv("backend/.env")

def migrate():
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("Error: DATABASE_URL not set.")
        return

    conn = psycopg2.connect(url)
    try:
        with conn.cursor() as cur:
            print("Adding 'name' column to relationships...")
            cur.execute("ALTER TABLE relationships ADD COLUMN IF NOT EXISTS name TEXT;")
            
            print("Adding 'secret_phrase' column to relationships...")
            cur.execute("ALTER TABLE relationships ADD COLUMN IF NOT EXISTS secret_phrase TEXT;")
            
            conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()

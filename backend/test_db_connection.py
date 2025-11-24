import psycopg2
import os

urls_to_try = [
    "postgresql://localhost:5432/postgres",
    "postgresql://saipittala@localhost:5432/postgres",
    "postgresql://saipittala@localhost:5432/railway",
    "postgresql://postgres:password@localhost:5432/railway"
]

for url in urls_to_try:
    try:
        print(f"Trying {url}...")
        conn = psycopg2.connect(url)
        print(f"Success! Connected to {url}")
        conn.close()
        break
    except Exception as e:
        print(f"Failed: {e}")

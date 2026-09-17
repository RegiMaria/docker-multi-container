from fastapi import FastAPI
from database import get_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend FastAPI funcionando!"}

@app.get("/api/messages")
def get_messages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, author, content, created_at FROM messages ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    messages = [
        {"id": r[0], "author": r[1], "content": r[2], "created_at": str(r[3])}
        for r in rows
    ]
    return messages
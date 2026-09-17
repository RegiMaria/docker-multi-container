from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

app = FastAPI()


class MessageCreate(BaseModel):
    author: str
    content: str


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


@app.post("/api/messages")
def create_message(message: MessageCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (author, content) VALUES (%s, %s) RETURNING id, created_at;",
        (message.author, message.content)
    )
    new_id, created_at = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {
        "id": new_id,
        "author": message.author,
        "content": message.content,
        "created_at": str(created_at)
    }
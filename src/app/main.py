from app.db import ensure_table
from app.init import create_app
from flask import request

from app.schemas import ChatRequest

app = create_app()
_ = ensure_table()

@app.get("/health")
def health():
    return {"stats": "ok"}

@app.get("/conversation/{id}")
def get_conversation(id: str):
    #We'll pull the message from dynamo db
    pass

@app.post("/chat")
def chat():
    data = request.get_json(force=True)
    # { 'message': 'User message', 'age': 28 , 'conver_id': '3244' ...}
    req = ChatRequest(**data)

    # We'll run the graph based on the user input










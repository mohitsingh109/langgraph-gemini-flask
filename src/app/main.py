import uuid
from http.client import responses

from app.db import ensure_table, put_message
from app.graph import run_graph
from app.init import create_app
from flask import request, jsonify
from app.db import get_history

from app.schemas import ChatRequest, ChatResponse

app = create_app()
_ = ensure_table()

@app.get("/health")
def health():
    return {"stats": "ok"}

@app.get("/conversation/<conversation_id>")
def get_conversation(conversation_id: str):
    #We'll pull the message from dynamo db
    conversation_history = get_history(conversation_id)
    return jsonify({
        "conversation_id": conversation_id,
        "history": conversation_history
    })

@app.post("/chat")
def chat():
    data = request.get_json(force=True)
    print(data)
    # { 'message': 'User message', 'age': 28 , 'conversation_id': None ...}
    req = ChatRequest(**data)

    # get or create new conversation_id
    conversation_id = req.conversation_id or str(uuid.uuid4())

    # Save the user message
    put_message(conversation_id, "user", req.message)

    # run graph
    reply = run_graph(req.message)

    # Save AI reply
    put_message(conversation_id, "ai", reply)

    # Create response payload
    resp = ChatResponse(conversation_id=conversation_id, reply=reply)
    return jsonify(resp.model_dump())










from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.generator import generate_answer

app = FastAPI()

# Allow frontend access (for Streamlit running separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(request: QueryRequest):
    answer = generate_answer(request.query)
    return {"answer": answer}

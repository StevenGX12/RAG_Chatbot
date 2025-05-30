from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.generator import Generator

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


# Initialize the Generator class once
generator = Generator()


@app.post("/chat")
def chat(request: QueryRequest):
    answer = generator.generate_answer(request.query)
    return {"answer": answer}

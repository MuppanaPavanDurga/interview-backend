from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai_utils import generate_question  # make sure this file exists
import uvicorn

app = FastAPI()

# ✅ Allow frontend requests from Vite (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check route
@app.get("/")
def root():
    return {"message": "LLM Interview Coach backend is running."}

# ✅ Chat endpoint that interacts with LLM
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    role = data.get("role", "Student")
    chat_history = data.get("chat", [])

    response = generate_question(role, chat_history)
    return {"response": response}

# Optional: run directly with `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

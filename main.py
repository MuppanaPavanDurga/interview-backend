from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai_utils import generate_question  # Ensure this file exists and works
import uvicorn

app = FastAPI()

# ✅ Allow requests from both local frontend and deployed frontend
origins = [
    "http://localhost:5173",  # Vite local dev
    "https://your-frontend-name.netlify.app",  # Replace with actual Netlify/Vercel domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check route
@app.get("/")
def root():
    return {"message": "LLM Interview Coach backend is running."}

# ✅ Chat endpoint
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    role = data.get("role", "Student")
    chat_history = data.get("chat", [])

    response = generate_question(role, chat_history)
    return {"response": response}

# ✅ Local dev run command
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

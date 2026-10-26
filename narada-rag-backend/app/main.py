import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from CHATREQUEST.index import ChatRequest

load_dotenv()

app_name = os.getenv("APP_NAME", "Narada")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

print(app_name)
print("OpenRouter API key configured:", bool(openrouter_key))


app = FastAPI(title="Narada API")

comany_id_var = "123"
question_var = "What is the capital of France?"
top_k_var = 5

x = ChatRequest(company_id=comany_id_var, question=question_var, top_k=top_k_var)

print("Validation of Argument Class:", x.validationOfArgumentClass())


@app.get("/health")
def health():
    return {"status": "ok"}



@app.post("/chat")
def chat(request: ChatRequest):
    if request.company_id != "acme":
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )
    

    return {
        "company_id": request.company_id,
        "answer": f"You asked: {request.question}",
    }
    


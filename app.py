from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

app = FastAPI(title="Gemma-3 API")

# Load model & tokenizer once at startup
model_name = "google/gemma-3-270m-it"  # or base model
HF_TOKEN = os.getenv("HF_TOKEN")

tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HF_TOKEN)

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 150  # optional override from n8n

@app.post("/generate")
async def generate(request: PromptRequest):
    # Tokenize input
    inputs = tokenizer(request.prompt, return_tensors="pt")

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            eos_token_id=tokenizer.eos_token_id
        )

    # Decode and clean output
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove repeated code blocks / markdown if any
    if "```" in text:
        parts = text.split("```")
        text = "".join(parts[1:2]).strip()

    # Truncate long outputs (optional for n8n)
    text = text[:1000]  # adjust as needed

    return {"response": text}

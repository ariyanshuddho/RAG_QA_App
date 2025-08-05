from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model and tokenizer once
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def format_prompt(question: str, context: str) -> str:
    return f"Use the following context to answer the question:\n\nContext: {context}\n\nQuestion: {question}"

def ask_llm(question: str, context: str, max_tokens: int = 200) -> str:
    prompt = format_prompt(question, context)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.7,
        top_p=0.95,
        do_sample=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

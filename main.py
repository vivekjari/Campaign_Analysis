from fastapi import FastAPI, UploadFile, File
import pandas as pd
from analyzer import analyze_dataset
from llm_router import ask_llm

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    insights, suggestions = analyze_dataset(df)
    llm_response = ask_llm(df, insights)
    return {
        "pro_insights": insights,
        "llm_suggestions": llm_response,
        "suggested_paths": suggestions
    }
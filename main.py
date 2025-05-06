from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import traceback

from analyzer import analyze_dataset
from llm_router import ask_llm

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        insights, suggestions = analyze_dataset(df)
        llm_response = ask_llm(df, insights)

        return {
            "pro_insights": insights,
            "llm_suggestions": llm_response,
            "suggested_paths": suggestions
        }

    except Exception as e:
        print("ERROR TRACEBACK:\n", traceback.format_exc())
        return JSONResponse(
            content={"error": str(e), "details": traceback.format_exc()},
            status_code=500
        )

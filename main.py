from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import traceback

from analyzer import analyze_dataset
from llm_router import ask_llm, continue_chat

app = FastAPI()

# CORS for frontend (e.g., Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory DataFrame
last_uploaded_df = None

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    global last_uploaded_df
    try:
        df = pd.read_csv(file.file)
        last_uploaded_df = df.copy()
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

@app.post("/ask")
async def ask_question(request: Request):
    global last_uploaded_df
    try:
        payload = await request.json()
        question = payload.get("question")
        if not last_uploaded_df is not None:
            return JSONResponse(content={"error": "No dataset in memory. Please upload and analyze first."}, status_code=400)

        response = continue_chat(last_uploaded_df, question)
        return {"response": response}

    except Exception as e:
        print("ASK ENDPOINT ERROR:\n", traceback.format_exc())
        return JSONResponse(
            content={"error": str(e), "details": traceback.format_exc()},
            status_code=500
        )

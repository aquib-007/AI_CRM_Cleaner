from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import re
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import io

nltk.download('punkt')

app = FastAPI(title="AI CRM Data Cleaner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CRMEntry(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]

class CRMData(BaseModel):
    records: List[CRMEntry]

def clean_text(text):
    if not text or pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def find_duplicates(data, threshold=90):
    duplicates = []
    seen = set()
    for i in range(len(data)):
        if i in seen:
            continue
        for j in range(i+1, len(data)):
            score = fuzz.token_sort_ratio(data[i], data[j])
            if score >= threshold:
                duplicates.append((i, j, score))
                seen.add(j)
    return duplicates

def clean_crm_data(df: pd.DataFrame) -> pd.DataFrame:
    for col in ['name', 'email', 'address']:
        df[col] = df[col].astype(str).apply(clean_text)

    df['phone'].fillna('unknown', inplace=True)
    df['email'].fillna('unknown@example.com', inplace=True)

    duplicate_indices = find_duplicates(df['name'].tolist(), threshold=90)
    to_drop = {j for _, j, _ in duplicate_indices}
    df_cleaned = df.drop(list(to_drop)).reset_index(drop=True)

    df_cleaned['combined'] = df_cleaned[['name', 'email', 'address']].apply(lambda x: ' '.join(x), axis=1)
    tfidf = TfidfVectorizer().fit_transform(df_cleaned['combined'])
    sim = cosine_similarity(tfidf, tfidf)

    to_drop_ml = set()
    for i in range(sim.shape[0]):
        for j in range(i+1, sim.shape[1]):
            if sim[i, j] > 0.85:
                to_drop_ml.add(j)

    df_final = df_cleaned.drop(list(to_drop_ml)).reset_index(drop=True)
    return df_final[['name', 'email', 'phone', 'address']]

@app.post("/clean-data/")
def clean_data(crm_data: CRMData):
    try:
        df = pd.DataFrame([entry.dict() for entry in crm_data.records])
        cleaned_df = clean_crm_data(df)
        return cleaned_df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        cleaned_df = clean_crm_data(df)
        return cleaned_df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

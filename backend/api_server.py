from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
import uuid
import os
from extractor import extract

app = FastAPI()

@app.post("/extract_from_doc")
def extract_from_doc(file: UploadFile = File(...), file_format: str = Form(...)):
    file_path = f"upload_{uuid.uuid4()}.pdf"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    try:
        data = extract(file_path, file_format)
    except Exception as e:
        data = {"error": str(e)}
    
    os.remove(file_path)
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI,File,HTTPException,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
app = FastAPI()

class FilePathInput(BaseModel):
 file_path :str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/importfile")
async def importfile(file: UploadFile = File(...)):
    try:
        # Define where to save the uploaded file
        upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"uploads")
        os.makedirs(upload_dir, exist_ok=True)  # Create directory if it doesn't exist

        file_path = os.path.join(upload_dir, file.filename)
        
        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        return {"statusCode": 200, "message": "File uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""@app.post("/importfile")
def import_file(input : FilePathInput):
 file_path = input.file_path
 if not file_path:
    raise HTTPException(status_code=400, detail="File path is empty")
 return {"statusCode":200}"""
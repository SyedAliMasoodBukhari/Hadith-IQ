from typing import List
from pydantic import BaseModel

class GetAllNarratorsResponse(BaseModel):
        results: List[str]
        totalPages:int
        currentpage:int
class FileResponse(BaseModel):
        message:str
        success:bool
        filePath:str
class FetchNarratorResponse(BaseModel):
        response:dict
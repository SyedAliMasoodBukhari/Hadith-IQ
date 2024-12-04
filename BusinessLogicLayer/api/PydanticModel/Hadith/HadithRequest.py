from pydantic import BaseModel
from typing import List

class SemanticSearchRequest(BaseModel):
    hadith: str
    project_name: str

class ExpandSearchRequest(BaseModel):
    hadithTO: List[str]  
    project_name: str 
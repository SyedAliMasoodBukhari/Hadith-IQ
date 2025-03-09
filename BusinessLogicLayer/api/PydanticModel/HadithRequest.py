from pydantic import BaseModel
from typing import List

class SemanticSearchRequest(BaseModel):
    hadith: str
    projectName: str
    threshold:float


class ExpandSearchRequest(BaseModel):
    hadithTO: List[str]  
    projectName: str 
    threshold:float

class SortResultRequest(BaseModel):
    hadithList: List[str]
    sortByNarrator: bool
    sortByAuthenticity: bool
    authenticityType: str

class ImportBookRequest(BaseModel):
    projectName: str
    filePath: str
class FilePathRequest(BaseModel):
    filePath:str
class GetAllProjectHadithsRequest(BaseModel):
    projectName:str
    page:int
class GetHadithDetails(BaseModel):
    matn:str
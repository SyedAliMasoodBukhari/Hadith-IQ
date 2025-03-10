from pydantic import BaseModel

class GetAllNarratorsRequest(BaseModel):
    projectName: str
    page:int
class ConvertToTxt(BaseModel):
    htmlfilepath:str
class CleanFile(BaseModel):
    inputFile:str
    arabic_count:str

from pydantic import BaseModel
from typing import Dict, Any

class ProjectRequest(BaseModel):
    projectName: str

class RenameProjectRequest(BaseModel):
    currentName: str
    newName: str

class SaveProjectStateRequest(BaseModel):
    projectName: str
    stateQuery:str
    stateData: Dict[str, Any]  #this for JSON data

class GetProjectStateRequest(BaseModel):
    projectName: str
    
class GetSingleProjectStateRequest(BaseModel):
    stateQuery:str
    projectName: str
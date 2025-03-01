from pydantic import BaseModel
from typing import Dict, Any

class ProjectResponse(BaseModel):
    projectName: str
    lastUpdated: str
    createdAt: str

class GetProjectStateResponse(BaseModel):
    stateQuery:str
    stateData: Dict[str, Any]

class GetSingleProjectStateResponse(BaseModel):
    stateData: Dict[str, Any]
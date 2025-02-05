from pydantic import BaseModel

class ProjectResponse(BaseModel):
    projectName: str
    lastUpdated: str
    createdAt: str

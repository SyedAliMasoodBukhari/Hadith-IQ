from pydantic import BaseModel

class ProjectRequest(BaseModel):
    projectName: str


class RenameProjectRequest(BaseModel):
    currentName: str
    newName: str

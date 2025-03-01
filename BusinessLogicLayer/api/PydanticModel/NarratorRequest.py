from pydantic import BaseModel

class GetAllNarratorsRequest(BaseModel):
    projectName: str
    page:int
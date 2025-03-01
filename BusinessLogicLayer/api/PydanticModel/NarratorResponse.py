from typing import List
from pydantic import BaseModel

class GetAllNarratorsResponse(BaseModel):
        results: List[str]
        totalPages:int
        currentpage:int
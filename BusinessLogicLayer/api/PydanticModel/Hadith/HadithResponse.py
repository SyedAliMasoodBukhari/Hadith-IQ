from typing import List
from pydantic import BaseModel

class SemanticSearchResult(BaseModel):
    matn: str
    similarity: float

class SemanticSearchResponse(BaseModel):
    query: str
    results: List[SemanticSearchResult]

class ExpandSearchResult(BaseModel):
    matn: str  
    similarity: float

class ExpandSearchResponse(BaseModel):
    query: List[str] 
    results: List[ExpandSearchResult] 

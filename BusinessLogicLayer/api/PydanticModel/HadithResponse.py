from typing import List
from pydantic import BaseModel

class SemanticSearchResult(BaseModel):
    matn: str
    similarity: float


class SemanticSearchResponse(BaseModel):
    query: str
    results: List[SemanticSearchResult]

class SortResultResult(BaseModel):
    matn:str
    narratorName:str
    similarity: float

class SortResultResponse(BaseModel):
    query: List[str]
    results: List[SortResultResult]

class ExpandSearchResult(BaseModel):
    matn: str  
    similarity: float

class ExpandSearchResponse(BaseModel):
    query: List[str] 
    results: List[ExpandSearchResult] 

class GetAllProjectHadithsResponse(BaseModel):
    results: dict
    totalPages:int
    currentpage:int

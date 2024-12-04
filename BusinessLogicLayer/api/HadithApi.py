from typing import List
from fastapi import APIRouter, HTTPException
from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.api.PydanticModel.Hadith.HadithRequest import SemanticSearchRequest
from BusinessLogicLayer.api.PydanticModel.Hadith.HadithResponse import SemanticSearchResponse
from BusinessLogicLayer.api.PydanticModel.Hadith.HadithResponse import SemanticSearchResult
from BusinessLogicLayer.api.PydanticModel.Hadith.HadithRequest import ExpandSearchRequest
from BusinessLogicLayer.api.PydanticModel.Hadith.HadithResponse import ExpandSearchResponse
from BusinessLogicLayer.api.PydanticModel.Hadith.HadithResponse import ExpandSearchResult


def hadith_router(fascade: AbsBLLFascade):
    router = APIRouter()

    @router.post("/semanticSearch", response_model=SemanticSearchResponse)
    async def semantic_search(request: SemanticSearchRequest):
        """
        Perform semantic search on Hadith data.
        """
        try:
            hadith = request.hadith
            project_name = request.project_name
            results = fascade.semanticSearch(hadith, project_name)

            # Assuming `results` is a list of dicts or tuples, convert to SemanticSearchResult
            search_results = [
            SemanticSearchResult(matn=result["matn"], similarity=result["similarity"])
            for result in results
            ]
            
            # Returning the response as expected
            return {"query": hadith, "results": search_results}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @router.post("/expandSearch", response_model=ExpandSearchResponse)
    async def expand_search(request: ExpandSearchRequest):
        """
        Perform expanded search based on the provided Hadith list.
        """
        try:
            hadith_list = request.hadithTO
            project_name = request.project_name
            results = fascade.expandSearch(hadith_list, project_name)
            expanded_results = [
                ExpandSearchResult(matn=result["matn"], similarity=result["similarity"])
                for result in results
            ]

            return {"query": hadith_list,"results": expanded_results}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router

def test_router():
    router = APIRouter()

    @router.get("/test")
    def test_api():
        """
        A simple test endpoint to check the server is running.
        """
        return {"message": "Server is running successfully!"}

    return router
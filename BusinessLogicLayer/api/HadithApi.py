from typing import List
from fastapi import APIRouter, HTTPException
from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.api.PydanticModel.HadithRequest import ExpandSearchRequest, FilePathRequest, SemanticSearchRequest,SortResultRequest,GetAllProjectHadithsRequest,ImportBookRequest
from BusinessLogicLayer.api.PydanticModel.HadithResponse import ExpandSearchResponse, ExpandSearchResult, SemanticSearchResponse,SortResultResponse,GetAllProjectHadithsResponse
from BusinessLogicLayer.api.PydanticModel.HadithResponse import SemanticSearchResult ,SortResultResult

def hadith_router(fascade: AbsBLLFascade):
    router = APIRouter()

    @router.post("/importHadithFile")
    async def import_hadith(request: ImportBookRequest):
        try:
            # Call the function from your BLL
            success = fascade.importHadithFile(request.filePath)
            if success:
                return {"message": "File imported successfully!"}
            else:
                return {"message": "File import failed.", "success": False}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/importHadithFileCSV")
    async def import_hadith_csv(request: FilePathRequest):
        try:
            # Call the function from your BLL
            success = fascade.importHadithFileCSV(request.filePath)
            if success:
                return {"message": "File imported successfully!"}
            else:
                return {"message": "File import failed. Please check the data.", "success": False}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/semanticSearch", response_model=SemanticSearchResponse)
    async def semantic_search(request: SemanticSearchRequest):
        try:
            hadith = request.hadith
            projectName = request.projectName
            threshold=request.threshold
            results = fascade.semanticSearch(hadith, projectName,threshold)

            # Assuming `results` is a list of dicts or tuples, convert to SemanticSearchResult
            searchResults = [
            SemanticSearchResult(matn=result["matn"], similarity=result["similarity"])
            for result in results
            ]
            
            # Returning the response as expected
            return {"query": hadith, "results": searchResults}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @router.post("/expandSearch", response_model=ExpandSearchResponse)
    async def expand_search(request: ExpandSearchRequest):
        try:
            hadith_list = request.hadithTO
            projectName = request.projectName
            threshold=request.threshold
            results = fascade.expandSearch(hadith_list, projectName,threshold)
            expanded_results = [
                ExpandSearchResult(matn=result["matn"], similarity=result["similarity"])
                for result in results
            ]

            return {"query": hadith_list,"results": expanded_results}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @router.post("/sortHadith", response_model=SortResultResponse)
    async def sort_search(request: SortResultRequest):
        try:
            hadithList = request.hadithList
            sortByNarrotor = request.sortByNarrator
            sortByAuthenticity=request.sortByAuthenticity
            authenticityType=request.authenticityType
            results = fascade.sortHadith(sortByNarrotor,sortByAuthenticity,authenticityType,hadithList)
            sorted_results = [
                SortResultResult(matn=result["matn"], narratorName=result["narratorName"], similarity=result["similarity"])
                for result in results
            ]

            return {"query": hadithList,"results": sorted_results}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    
   
    @router.get("/getAllProjectHadiths",response_model=GetAllProjectHadithsResponse)
    async def get_all_project_hadiths(request:GetAllProjectHadithsRequest):
        try:
            print("api")
            projectName=request.projectName
            page=request.page
            hadith=fascade.getAllHadithsOfProject(projectName,page)
            print("func called")
            return GetAllProjectHadithsResponse(results=hadith["results"],  
            totalPages=hadith["total_pages"],
            currentpage=hadith["current_page"],)


            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    return router
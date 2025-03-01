from typing import List
from fastapi import APIRouter, HTTPException
from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.api.PydanticModel.NarratorRequest import GetAllNarratorsRequest
from BusinessLogicLayer.api.PydanticModel.NarratorResponse import GetAllNarratorsResponse

def narrator_router(fascade: AbsBLLFascade):
    router = APIRouter()

    @router.get("/getAllProjectNarrators", response_model=GetAllNarratorsResponse)
    async def get_all_project_narrators(request: GetAllNarratorsRequest):
        try:
            print("in api")
            projectName = request.projectName
            page=request.page
            narrator_names = fascade.getAllNarratorsOfProject(projectName,page)
            print(narrator_names)
            return GetAllNarratorsResponse(
            results=narrator_names["results"],  # Use square brackets for dictionary keys
            totalPages=narrator_names["total_pages"],
            currentpage=narrator_names["current_page"],
        )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
    return router
    

from typing import List
from fastapi import APIRouter, HTTPException,UploadFile
from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.api.PydanticModel.NarratorRequest import GetAllNarratorsRequest,ConvertToTxt,CleanFile
from BusinessLogicLayer.api.PydanticModel.NarratorResponse import GetAllNarratorsResponse,FileResponse,FetchNarratorResponse

def narrator_router(fascade: AbsBLLFascade):
    router = APIRouter()

    @router.get("/getAllProjectNarrators", response_model=GetAllNarratorsResponse)
    async def get_all_project_narrators(projectName:str,page:int):
        try:
            narrator_names = fascade.getAllNarratorsOfProject(projectName,page)
            return GetAllNarratorsResponse(
            results=narrator_names["results"],
            totalPages=narrator_names["total_pages"],
            currentpage=narrator_names["current_page"],
        )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/convertToHtml",response_model=FileResponse)
    async def convert_html(request:ConvertToTxt):
        try:
            success = fascade.convertHtmlToText(request.htmlfilepath)
            if success["success"] is False:
                return FileResponse(success= success["success"],message="File not converted to text file",filePath="none")
            return FileResponse(success=success["success"],message=f"File saved in path: {success['filePath']}",filePath=success["filePath"])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
    
    @router.post("/cleanFile",response_model=FileResponse)
    async def clean_File(request:CleanFile):
        try:
            success = fascade.filter_and_append(request.inputFile,request.arabic_count)
            if success["success"] is False:
                return FileResponse(success= success["success"],message="File not Cleaned",filePath="none")
            return FileResponse(success=success["success"],message=f"File cleaned and saved in path: {success['filePath']}",filePath=success["filePath"])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
    
    @router.post("/fetchNarratorData",response_model=FetchNarratorResponse)
    async def fetch_narrator_data(request:CleanFile):
        try:
            response = fascade.fetch_narrator_data(request.inputFile,request.arabic_count)
            if not response:
                return FetchNarratorResponse(response="No response Found")
            return FetchNarratorResponse(response=response)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
        
    
    @router.get("/getAllNarrators", response_model=GetAllNarratorsResponse)
    async def getAllNarrators(page:int):
        try:
            narrator_names = fascade.getAllNarrators(page)
            return GetAllNarratorsResponse(
                results=narrator_names["results"],
                totalPages=narrator_names["total_pages"],
                currentpage=narrator_names["current_page"],)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
        
    


    
        
    return router
    

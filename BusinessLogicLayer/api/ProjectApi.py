from typing import List
from fastapi import APIRouter, HTTPException
from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.api.PydanticModel.ProjectRequest import ProjectRequest, RenameProjectRequest,SaveProjectStateRequest,GetProjectStateRequest,GetSingleProjectStateRequest,MergeProjectStateRequest,RenameProjectStateRequest,DeleteProjectStateRequest,RemoveHadithRequest
from BusinessLogicLayer.api.PydanticModel.ProjectResponse import ProjectResponse,GetProjectStateResponse,GetSingleProjectStateResponse,MergeProjectStateResponse,RenameProjectStateResponse,DeleteProjectStateResponse,RemoveHadithResponse
def project_router(fascade: AbsBLLFascade):
    router = APIRouter()

    @router.post("/addProject")
    async def addProject(request: ProjectRequest):
        try:
            success = fascade.createProject(request.projectName)
            if success:
                return {"message": "Project created successfully!"}
            else:
                return {"message": "Project creation unsuccessful!", "success": False}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @router.post("/renameProject")
    async def renameProject(request: RenameProjectRequest):
        try:
            success = fascade.renameProject(request.currentName, request.newName)
            if success:
                return {"message": "Project renamed successfully!"}
            else:
                return {"message": "Rename unsuccessful!", "success": False}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @router.post("/deleteProject")
    async def deleteProject(request: ProjectRequest):
        try:
            success = fascade.deleteProject(request.projectName)
            if success:
                return {"message": "Project deleted successfully!"}
            else:
                return {"message": "Project deletion failed!", "success": False}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @router.get("/getProjects", response_model=List[ProjectResponse])
    async def getProjects():
        try:
            projects = fascade.getProjects()
            if not projects:
                return []
            
            response = []

            response = [
            ProjectResponse(
                projectName=project.name,
                lastUpdated=project.lastUpdated,
                createdAt=project.createdAt
            )
            for project in projects
            ]

            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/saveProjectState")
    async def saveProjectState(request: SaveProjectStateRequest):
            try:
                print("mai idhr hunnn")
                success = fascade.saveProjectState(request.projectName,request.stateData,request.stateQuery)
                if success:
                    print("here2")
                    return {"message": "Project State saved successfully!"}
                else:
                    return {"message": "Project State saving is unsuccessful!", "success": False}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            

    @router.get("/getProjectState", response_model=List[GetProjectStateResponse])
    async def getProjectState(request:GetProjectStateRequest):
        try:
            projectState = fascade.getProjectState(request.projectName)
            if not projectState:
                return []
            
            response = [GetProjectStateResponse(
              stateQuery=projectState
            )]
            
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))





    @router.get("/getSingleProjectState", response_model=List[GetSingleProjectStateResponse])
    async def getSingleProjectState(request: GetSingleProjectStateRequest):
        try:
            projectState = fascade.getSingleProjectState(request.projectName, request.stateQuery)
            if not projectState:
                return []
            response = [
                GetSingleProjectStateResponse(
                    stateData=projectState,  # Include matn for each hadith_id
                    query=request.stateQuery      # Include the query
                )
            ]
            return response

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    @router.post("/mergeProjectState",response_model=List[MergeProjectStateResponse])
    async def mergeProjectState(request: MergeProjectStateRequest):
        try:
            success = fascade.mergeProjectState(
                request.projectName,
                request.querynames,
                request.queryName
            )
            if success:
                response=[ MergeProjectStateResponse(message="Project states merged successfully!",success=True)]
                return response
            else:
                response=[MergeProjectStateResponse(message="Project states merged unsuccessful!",success=False)]
                return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @router.post("/renameProjectState",response_model=List[RenameProjectStateResponse])
    async def renameProjectState(request: RenameProjectStateRequest):
        try:
            success = fascade.renameQueryOfState(
                request.projectName,
                request.oldQueryName,
                request.newQueryName
            )
            if success:
                response=[ RenameProjectStateResponse(message="Project State Renamed successfully!",success=True)]
                return response
            else:
                response=[RenameProjectStateResponse(message="Project State Rename unsuccessful!",success=False)]
                return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/deleteProjectState",response_model=List[DeleteProjectStateResponse])
    async def deleteProjectState(request: DeleteProjectStateRequest):
        try:
            success = fascade.deleteState(
                request.projectName,
                request.queryName
            )
            if success:
                response=[ DeleteProjectStateResponse(message="Project State Deleted successfully!",success=True)]
                return response
            else:
                response=[DeleteProjectStateResponse(message="Project State Deletion unsuccessful!",success=False)]
                return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @router.post("/removeHadithFromState", response_model=RemoveHadithResponse)
    async def removeHadithFromStateQuery(request: RemoveHadithRequest):
        try:
            success = fascade.removeHadithFromState(request.matn, request.projectName, request.stateQuery)
            if success:
                return RemoveHadithResponse(
                    success=True,
                    message="Hadith ID successfully removed from stateQuery.",
                )
            else:
                return RemoveHadithResponse(
                    success=False,
                    message="Failed to remove Hadith ID from stateQuery.",
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    



    return router
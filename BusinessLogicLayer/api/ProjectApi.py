from typing import List
from fastapi import APIRouter, HTTPException
from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.api.PydanticModel.ProjectRequest import ProjectRequest, RenameProjectRequest
from BusinessLogicLayer.api.PydanticModel.ProjectResponse import ProjectResponse

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

    return router
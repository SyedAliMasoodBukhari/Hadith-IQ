from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from TO.ProjectTO import ProjectTO
from typing import List
class ProjectDAO(AbsProjectDAO):
    
    
    def createProject(self,name:str)->bool:
        return None
    

    def saveProject()->bool:
        return None
    
    
    def openExistingProject()->bool:
        return None
    
    
    def renameProject(self,currName:str,newName:str)->bool:
        return None

    
    def getProjects(self)->List[ProjectTO]:
        return None

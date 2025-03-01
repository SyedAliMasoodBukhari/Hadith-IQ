from abc import ABC,abstractmethod
from TO.ProjectTO import ProjectTO
from typing import List
class AbsProjectBO(ABC):
 
    @abstractmethod
    def createProject(self,name:str)->bool:
        pass
        
    @abstractmethod
    def saveProject(self)->bool:
        pass
        
    @abstractmethod
    def deleteProject(self, name: str) -> bool:
        pass
        
    @abstractmethod
    def renameProject(self,currName:str,newName:str)->bool:
        pass
        
    @abstractmethod
    def getProjects(self)->List[ProjectTO]:
        pass

    @abstractmethod
    def saveProjectState(self,name:str, stateData: dict,query:str)->bool:
        pass

    @abstractmethod
    def getProjectState(self,name:str)->dict:
        pass
    @abstractmethod
    def getSingleProjectState(self,name:str,query:str)->dict:
      pass

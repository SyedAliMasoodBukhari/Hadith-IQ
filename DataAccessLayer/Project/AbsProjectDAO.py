from abc import ABC,abstractmethod
import datetime
from typing import List
from TO.ProjectTO import ProjectTO
class AbsProjectDAO(ABC):

    @abstractmethod
    def createProject(self,name:str, creationDate: str)->bool:
        pass
    
    @abstractmethod
    def saveProject(self)->bool:
        pass
    
    @abstractmethod
    def renameProject(self,currName:str,newName:str)->bool:
        pass

    @abstractmethod
    def getProjects(self)->List[ProjectTO]:
        pass

    @abstractmethod
    def deleteProject(self, projectName: str) -> bool:
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

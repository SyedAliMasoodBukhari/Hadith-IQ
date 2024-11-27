from abc import ABC,abstractmethod
from typing import List
from TO.ProjectTO import ProjectTO
class AbsProjectDAO(ABC):
    @abstractmethod
    def createProject(self,name:str)->bool:
        pass
    
    @abstractmethod
    def saveProject()->bool:
        pass
    
    @abstractmethod
    def openExistingProject()->bool:
        pass
    
    @abstractmethod
    def renameProject(self,currName:str,newName:str)->bool:
        pass

    @abstractmethod
    def getProjects(self)->List[ProjectTO]:
        pass

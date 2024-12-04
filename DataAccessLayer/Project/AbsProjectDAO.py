from abc import ABC,abstractmethod
import datetime
from typing import List
from TO.ProjectTO import ProjectTO
class AbsProjectDAO(ABC):
    @abstractmethod
    def createProject(self,name:str, currentDate: str)->bool:
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

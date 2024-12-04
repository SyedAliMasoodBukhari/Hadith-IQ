from abc import ABC,abstractmethod
from typing import List
class AbsProjectBO(ABC):
 
 @abstractmethod
 def createProject(self,name:str)->bool:
  pass
 
 @abstractmethod
 def saveProject(self)->bool:
  pass
 
 @abstractmethod
 def openExistingProject(self)->bool:
  pass
 
 @abstractmethod
 def renamepProject(self,currName:str,newName:str)->bool:
  pass
 
 @abstractmethod
 def getProjects(self)->List[str]:
  pass

from abc import ABC,abstractmethod
import datetime
from typing import List
from DataAccessLayer.Hadith import AbsHadithDAO
from TO.HadithTO import HadithTO
from TO.ProjectTO import ProjectTO
class AbsDALFascade(ABC):
 
    @abstractmethod
    def insertHadith(self,hadithTO:HadithTO)->bool:
        pass
    
    @abstractmethod
    def getHadithDetails(self,hadithTO:HadithTO)->dict:
        pass
    
    @abstractmethod
    def getProjectHadithsEmbedding(self, projectName:str) -> dict:
        pass

    @abstractmethod
    def createProject(self,name:str, currentDate: datetime)->bool:
        pass

    @abstractmethod
    def getProjects(self, project_id: int) -> List[ProjectTO]:
        pass
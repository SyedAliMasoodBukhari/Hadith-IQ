
from abc import ABC,abstractmethod
import datetime
from typing import Dict, List
from DataAccessLayer.Hadith import AbsHadithDAO
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
from TO.ProjectTO import ProjectTO
from TO.SanadTO import SanadTO
class AbsDALFascade(ABC):

    @abstractmethod
    def createProject(self,name:str, creationDate: str)->bool:
        pass

    @abstractmethod
    def getProjects(self) -> List[ProjectTO]:
        pass

    @abstractmethod
    def renameProject(self,currName:str,newName:str)->bool:
        pass

    @abstractmethod
    def deleteProject(self, projectName: str) -> bool:
        pass

    @abstractmethod
    def saveProjectState(self,name:str, stateData: List[str],query:str)->bool:
        pass
    
    @abstractmethod
    def getProjectState(self,name:str)->List[str]:
        pass

    @abstractmethod
    def getSingleProjectState(self,name:str,query:str)->List[str]:
      pass
    @abstractmethod
    def removeHadithFromState(self, matn: List[str], projectName: str, stateQuery: str) -> bool:
        pass

    @abstractmethod
    def mergeProjectState(self, projectname: str, query_names: List[str], queryname: str) -> bool:
        pass
    @abstractmethod
    def renameQueryOfState(self, project_name: str, old_query_name: str, new_query_name: str) -> bool:
        pass
    @abstractmethod
    def deleteState(self, project_name: str, query_name: str) -> bool:
        pass
    

    @abstractmethod
    def insertBook(self,bookName:str)->bool:
        pass

    @abstractmethod
    def deleteBook(self,bookName:str)->bool:
        pass
    @abstractmethod
    def getAllBooks(self)->List[str]:
        pass

    @abstractmethod
    def associate_book_with_project(self, book_name: str, project_name: str):
        pass
    
    @abstractmethod
    def getHadithFirstNarrator(self, hadith:str) -> str:
        pass
    @abstractmethod
    def importBook(self, filePath: str) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def insertHadith(self, hadithTO: HadithTO) -> bool:
        pass
    
    @abstractmethod
    def getHadithDetails(self,hadithTO:HadithTO)->dict:
        pass

    @abstractmethod
    def associate_hadiths_with_project(self, book_name: str, project_name: str):
        pass
    @abstractmethod
    def getAllHadithsOfProject(self, projectName: str,page:int) -> dict:
        pass
    @abstractmethod
    def getHadithDetails(self, matn: str) -> dict:
        pass
    
    @abstractmethod
    def getProjectHadithsEmbedding(self, projectName:str) -> dict:
        pass

    @abstractmethod
    def insertSanad(self, sanadTO: SanadTO) -> bool:
        pass
    
    @abstractmethod
    def getSanad(self,matn:str)->List[SanadTO]:
        pass

    @abstractmethod
    def associate_sanads_with_project_by_book(self,book_name: str, project_name: str):
        pass


    @abstractmethod
    def insertNarrator(self,sanad: str, narratorTO : NarratorTO)->bool:
        pass
    
    @abstractmethod
    def getAllNarrators(self)->List[NarratorTO]:
        pass
    
    @abstractmethod
    def getSimilarNarrator(self,NarratorTO:NarratorTO)->List[NarratorTO]:
        pass
    
    @abstractmethod
    def getNarratedHadith(self,NarratorTO:NarratorTO)->List[HadithTO]:
        pass

    @abstractmethod
    def getNarratorDetails(self,NarratorTO:NarratorTO)->Dict:
        pass
    @abstractmethod
    def getAllNarratorsOfProject(self, project_name: str,page:int) -> dict:
        pass
      
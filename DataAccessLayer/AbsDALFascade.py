from DataAccessLayer import AbsHadithDAO,AbsNarratorDAO,AbsProjectDAO,AbsSanadDAO,AbsOpinionDAO
from abc import ABC,abstractmethod
from typing import List,Dict
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
from TO.OpinionTO import OpinionTO
from TO.ProjectTO import ProjectTO
class AbsDALFascade(ABC):
    #ProjectDAO Abstract Function
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


    #HadithDAO Abstract Function
    #Donot Change Below
    @abstractmethod
    def insertHadith(self,hadithTO:HadithTO)->bool:
        pass
    
    @abstractmethod
    def insertHadithEmbeddings(self,matn:str,embeddings:List[float])->bool:
        pass

    @abstractmethod
    def getHadithEmbeddings(self,matn:str)->List[float]:
        pass

    @abstractmethod
    def getAllHadith(self) -> List[HadithTO]:
        pass

    @abstractmethod
    def insertHadithAuthenticity(self,hadithTO:HadithTO)->bool:
        pass

    @abstractmethod
    def getHadithDetails(self,hadithTO:HadithTO)->Dict[str,any]:
        pass

    #NarratorDAO Abstract Functions

    @abstractmethod
    def insertNarrator(self,narratorTO : NarratorTO)->bool:
        pass
    
    @abstractmethod 
    def getAllNarrators(self)->List[NarratorTO]:
        pass
    
    @abstractmethod
    def getsSimilarNarrator(self,NarratorTO:NarratorTO)->List[NarratorTO]:
        pass
    
    @abstractmethod
    def importNarratorOpinion(self,File:str)->bool:
        pass
    
    @abstractmethod
    def getNarratedHadith(self,NarratorTO:NarratorTO)->List[HadithTO]:
     pass

    @abstractmethod
    def getNarratorDetails(self,NarratorTO:NarratorTO)->Dict:
        pass


    #SanadDAO Abstract Functions
    @abstractmethod
    def insertSanad(self,HadithTO:HadithTO)->bool:
        pass

    @abstractmethod
    def getSanad(self,matn:str)->List[NarratorTO]:
        pass
    
    #OpinionDAO Abstract Functions
    @abstractmethod
    def insertOpinion(self,NarratorTO:NarratorTO,opinion:str)->bool:
        pass
    
    @abstractmethod
    def getOpinions(self,NarratorTO:NarratorTO)->List[OpinionTO]:
        pass
    

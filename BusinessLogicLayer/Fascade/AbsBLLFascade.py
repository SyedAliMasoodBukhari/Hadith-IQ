from BusinessLogicLayer.Project.AbsProjectBO import AbsProjectBO
from BusinessLogicLayer.Hadith.AbsHadithBO import AbsHadithBO
from BusinessLogicLayer.Narrator.AbsNarratorBO import AbsNarratorBO
from BusinessLogicLayer.Sanad.AbsSanadBO import AbsSanadBO
from TO.SanadTO import SanadTO
from TO.HadithTO import HadithTO
from TO.ProjectTO import ProjectTO
from TO.NarratorTO import NarratorTO
from typing import List,Dict
from abc import ABC,abstractmethod

class AbsBLLFascade(ABC):
    #AbsProjectBO functions
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
     def getProjects(self)->List[ProjectTO]:
      pass
     

    #AbsHadithBO Functions
    
     @abstractmethod
     def importedHadithFile(self,filePath:str)->bool:
        pass
    
     @abstractmethod
     def getAllHadith(self)->List[HadithTO]:
        pass
    
     @abstractmethod
     def semanticSearch(self, hadith: str,projectName:str) -> dict:
        pass

     @abstractmethod
     def getHadithData(self,HadithTO:HadithTO)->Dict:
        pass

     @abstractmethod
     def sortHadith(self,ByNarrator:bool,ByGrade:bool,GradeType:List[str])->List[HadithTO]:
        pass

     @abstractmethod
     def generateHadithFile(self,path:str,HadithTO:List[HadithTO])->bool:
        pass
    
     @abstractmethod
     def expandSearch(self,HadithTO:List[str],projectName: str)->dict:
       pass
     
     #AbsNarratorBO funtions
     @abstractmethod
     def getNarratedHadith(self,narratorTO:NarratorTO)->List[HadithTO]:
        pass

     @abstractmethod
     def getNarratorTeachers(self,narratorTO:NarratorTO)->List[NarratorTO]:
        pass

     @abstractmethod
     def getNarratorStudents(self,narratorTO:NarratorTO)->List[NarratorTO]:
        pass

     @abstractmethod
     def applySentimentAnalysis(self,narratorTO:NarratorTO)->str:
        pass

     @abstractmethod
     def NarratorSearch(self,narrator:str)->List[NarratorTO]:
        pass

     @abstractmethod
     def getNarratorAuthenticity(self,narratorTO:NarratorTO)->str:
        pass

     @abstractmethod
     def generateNarratorFile(self,path:str,narratorTOList:List[NarratorTO])->bool:
        pass

     @abstractmethod
     def getNarratorDetails(self,narratorTO:NarratorTO)->List[NarratorTO]:
        pass

     @abstractmethod
     def importNarratorOpinions(self,file:str)->bool:
        pass
     
     #AbsSanadBO function
     @abstractmethod
     def authenticateSanad(self,sanadTO:SanadTO)->str:
        pass

     @abstractmethod
     def insertOpinion(self,narratorTO:NarratorTO,opinion:str)->bool:
        pass

     @abstractmethod
     def getSanad(self,matn:str)->List[NarratorTO]:
        pass
     
     #AbsOpinionBo Functions
   #   @abstractmethod
   #   def getOpinions(self,narratorTO:NarratorTO)->List[OpinionTO]:
   #      pass
    

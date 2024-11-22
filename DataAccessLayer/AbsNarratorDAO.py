from abc import ABC,abstractmethod
from TO.NarratorTO import NarratorTO
from TO.HadithTO import HadithTO
from typing import List,Dict
class AbsNarratorDAO(ABC):
    
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

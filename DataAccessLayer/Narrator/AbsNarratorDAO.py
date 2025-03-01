from abc import ABC, abstractmethod
from typing import Dict, List

from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO


class AbsNarratorDAO(ABC):

    @abstractmethod
    def insertNarrator(self,sanad: str, narratorTO : NarratorTO)->bool:
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
    @abstractmethod
    def getAllNarratorsOfProject(self, project_name: str,page :int) ->dict:
        pass
      
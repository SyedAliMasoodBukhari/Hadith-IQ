from abc import ABC,abstractmethod
from typing import List
from TO.NarratorTO import NarratorTO
from TO.HadithTO import HadithTO
class AbsNarratorBO(ABC):
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

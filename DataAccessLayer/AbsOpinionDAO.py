from abc import ABC,abstractmethod
from TO.NarratorTO import NarratorTO
from TO.OpinionTO import OpinionTO
from typing import List
class AbsOpinionDAO(ABC):
    @abstractmethod
    def insertOpinion(self,NarratorTO:NarratorTO,opinion:str)->bool:
        pass
    
    @abstractmethod
    def getOpinions(self,NarratorTO:NarratorTO)->List[OpinionTO]:
        pass
    
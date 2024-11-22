from abc import ABC,abstractmethod
from TO.OpinionTO import OpinionTO
from typing import List
from TO.NarratorTO import NarratorTO
class AbsOpinionBO(ABC):
    @abstractmethod
    def getOpinions(self,narratorTO:NarratorTO)->List[OpinionTO]:
        pass
    
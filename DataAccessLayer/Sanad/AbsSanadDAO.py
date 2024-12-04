from abc import ABC, abstractmethod
from typing import List

from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO


class AbsSanadDAO(ABC):
    @abstractmethod
    def insertSanad(self,HadithTO:HadithTO)->bool:
        pass

    @abstractmethod
    def getSanad(self,matn:str)->List[NarratorTO]:
        pass
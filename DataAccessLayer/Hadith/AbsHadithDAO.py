from abc import ABC,abstractmethod
from typing import List,Dict,Any
from TO.HadithTO import HadithTO
class AbsHadithDAO(ABC):

    @abstractmethod
    def insertHadith(self,hadithTO:HadithTO)->bool:
        pass

    @abstractmethod
    def getHadithEmbeddings(self,matn:str)->str:
        pass

    @abstractmethod
    def getHadithDetails(self,hadithTO:HadithTO)->dict:
        pass
    
    @abstractmethod
    def getProjectHadithsEmbedding(self, projectName:str) -> dict:
        pass
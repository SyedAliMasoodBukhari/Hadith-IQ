from abc import ABC,abstractmethod
from typing import List,Dict,Any
from TO.HadithTO import HadithTO
class AbsHadithDAO(ABC):

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
    def getHadithDetails(self,hadithTO:HadithTO)->Dict[str,Any]:
        pass
    
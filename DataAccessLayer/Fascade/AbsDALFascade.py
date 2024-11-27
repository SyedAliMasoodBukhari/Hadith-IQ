
from abc import ABC,abstractmethod
from DataAccessLayer.Hadith import AbsHadithDAO
from TO.HadithTO import HadithTO
class AbsDALFascade(ABC):
 
    @abstractmethod
    def insertHadith(self,hadithTO:HadithTO)->bool:
        pass
    
    @abstractmethod
    def getHadithDetails(self,hadithTO:HadithTO)->dict:
        pass
    
    @abstractmethod
    def getProjectHadithsEmbedding(self, projectName:str) -> dict:
        pass
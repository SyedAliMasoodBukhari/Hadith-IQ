from abc import ABC,abstractmethod
from typing import List,Dict
from TO.HadithTO import HadithTO
class AbsHadithBO(ABC):

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

    @abstractmethod
    def insertHadith(self,HadithTO:List[HadithTO])->bool:
        pass
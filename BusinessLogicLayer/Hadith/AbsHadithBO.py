from abc import ABC,abstractmethod
from typing import List,Dict
from TO.HadithTO import HadithTO
class AbsHadithBO(ABC):

    @abstractmethod
    def importHadithFile(self, projectName: str, filePath: str) -> bool:
        pass
    
    @abstractmethod
    def getAllHadith(self)->List[HadithTO]:
        pass
    
    @abstractmethod
    def semanticSearch(self, hadith: str,projectName:str,threshold:float) -> dict:
        pass

    @abstractmethod
    def getHadithData(self,HadithTO:HadithTO)->Dict:
        pass

    @abstractmethod
    def sortHadith(self, byNarrator: bool, byGrade: bool, gradeType: str, hadithList: List[str]) -> List[dict]:
        pass

    @abstractmethod
    def generateHadithFile(self,path:str,HadithTO:List[HadithTO])->bool:
        pass
    
    @abstractmethod
    def expandSearch(self,HadithTO:List[str],projectName: str,threshold:float)->dict:
        pass
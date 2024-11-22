from AbsHadithBO import AbsHadithBO
from typing import List,Dict
from TO.HadithTO import HadithTO
class HadithBO(AbsHadithBO):
    
    def importedHadithFile(self,filePath:str)->bool:
        return None
    
    
    def getAllHadith(self)->List[HadithTO]:
        return None
    
    
    def semanticSearch(self,hadith:str)->List[HadithTO]:
        return None

    
    def getHadithData(self,HadithTO:HadithTO)->Dict:
        return None

    
    def sortHadith(self,ByNarrator:bool,ByGrade:bool,GradeType:List[str])->List[HadithTO]:
        return None

    
    def generateHadithFile(self,path:str,HadithTO:List[HadithTO])->bool:
        return None
    
    
    def expandSearch(self,HadithTO:List[HadithTO])->List[HadithTO]:
        return None
    
    def createAndStoreEmbeddings(self,hadithTOList:List[HadithTO])->bool:
        return None
    
    #def createSingleEmbedding(self,hadith:str)->
    def authenticateHadith(self,hadithTO:HadithTO)->bool:
         return None
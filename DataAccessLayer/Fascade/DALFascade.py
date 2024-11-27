from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from TO.HadithTO import HadithTO
from DataAccessLayer.Hadith.AbsHadithDAO import AbsHadithDAO
class DALFascade(AbsDALFascade):
    
    #ABSHadithDAO initializer
    def __init__(self,hadithDAO:AbsHadithDAO):
        self.__hadithDAO=hadithDAO
  
    
    def insertHadith(self,hadithTO:HadithTO)->bool:
        return self.__hadithDAO.insertHadith(hadithTO)
    
    
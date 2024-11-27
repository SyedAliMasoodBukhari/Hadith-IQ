from DataAccessLayer.Sanad.AbsSanadDAO import AbsSanadDAO
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
from typing import List

class SanadDAO(AbsSanadDAO):
    
    def insertSanad(self,HadithTO:HadithTO)->bool:
        return None

    
    def getSanad(self,matn:str)->List[NarratorTO]:
        return None
from DataAccessLayer.Narrator.AbsNarratorDAO import AbsNarratorDAO
from typing import List,Dict
from TO.NarratorTO import NarratorTO
from TO.HadithTO import HadithTO
from DataAccessLayer.DbConnection import DbConnection
from DataAccessLayer.UtilDAO import UtilDao
class NarratorDAO(AbsNarratorDAO):
  
    def __init__(self, db_connection: DbConnection,util :UtilDao):
        self.__db_connection = db_connection
        self.__util=util

    def insertNarrator(self,narratorTO : NarratorTO)->bool:
        return None
    
    
    def getAllNarrators(self)->List[NarratorTO]:
        return None
    
    
    def getsSimilarNarrator(self,NarratorTO:NarratorTO)->List[NarratorTO]:
        return None
    
    
    def importNarratorOpinion(self,File:str)->bool:
        return None
    
    
    def getNarratedHadith(self,NarratorTO:NarratorTO)->List[HadithTO]:
        return None

    def getNarratorDetails(self,NarratorTO:NarratorTO)->Dict:
        return None

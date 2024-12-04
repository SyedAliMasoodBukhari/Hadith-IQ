from DataAccessLayer.Sanad.AbsSanadDAO import AbsSanadDAO
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
from DataAccessLayer.UtilDAO import UtilDao
from DataAccessLayer.DbConnection import DbConnection
from typing import List

class SanadDAO(AbsSanadDAO):
    def __init__(self, db_connection: DbConnection,util :UtilDao):
        self.__db_connection = db_connection
        self.__util=util
    
    def insertSanad(self,HadithTO:HadithTO)->bool:
        return None

    
    def getSanad(self,matn:str)->List[NarratorTO]:
        return None
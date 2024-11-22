import mysql.connector
from mysql.connector import Error
from AbsHadithDAO import AbsHadithDAO
from typing import Any, Dict, List
from DbConnection import DbConnection
"""import sys
sys.path.append('../')"""
from TO.HadithTO import HadithTO

class HadithDAO(AbsHadithDAO):

    def __init__(self,db_connection : DbConnection):
        self.__db_Connection = db_connection
    
    def insertHadith(self,hadithTO : HadithTO) -> bool:
        cursor = self.__db_Connection.cursor()
        try : 
            query = "INSERT INTO hadiths (matn) VALUES (%s)"
            cursor.execute(query, (hadithTO.matn,))
            self.__db_Connection.commit()
            return True
        except Exception as e:
            return False
        
    def insertHadithEmbeddings(self, matn: str, embeddings: List[float]) -> bool:
        return False

    def getHadithEmbeddings(self, matn: str) -> List[float]:
        return None

    def getAllHadith(self) -> List[HadithTO]:
        return None
    
    def insertHadithAuthenticity(self, hadithTO: HadithTO) -> bool:
        return False

    def getHadithDetails(self, hadithTO: Any) -> Dict[str, Any]:
        return False
    

from DataAccessLayer.DataModels import Narrator, Sanad, narrator_sanad
from DataAccessLayer.Narrator.AbsNarratorDAO import AbsNarratorDAO
from typing import List,Dict
from TO.NarratorTO import NarratorTO
from TO.HadithTO import HadithTO
from DataAccessLayer.DbConnection import DbConnectionModel
from DataAccessLayer.UtilDAO import UtilDao
from sqlalchemy.orm import Session

class NarratorDAO(AbsNarratorDAO):
  
    def __init__(self, dbConnection: DbConnectionModel,util :UtilDao):
        self.__dbConnection = dbConnection
        self.__util=util
                
    def insertNarrator(self,sanad: str, narratorTO : NarratorTO)->bool:
        try:
            session: Session = self.__dbConnection.getSession()

            sanadObj = session.query(Sanad).filter(Sanad.Sanad == sanad).first()
            if not sanadObj:
                print(f"Sanad '{sanad}' not found.")
                return False
            
            _sanadID = sanadObj.SanadID

            # Check if the narrator already exists
            narratorObj = session.query(Narrator).filter(Narrator.NarratorName == narratorTO.narratorName).first()
            if not narratorObj:
                narratorObj = Narrator(
                    NarratorName=narratorTO.narratorName,
                    NarratorAuthenticity="Authentic"  # Default authenticity
                )
                session.add(narratorObj)
                session.flush()  # Ensures NarratorID is generated for the new record

            # Check if the narrator is already associated with the sanad
            existing_association = session.query(narrator_sanad).filter(
                narrator_sanad.c.NarratorID == narratorObj.NarratorID,
                narrator_sanad.c.SanadID == _sanadID
            ).first()

            if existing_association:
                print(f"Narrator '{narratorTO.narratorName}' is already associated with the sanad.")
                return False

            # Add the association to the narrator_sanad table
            session.execute(
                narrator_sanad.insert().values(
                    NarratorID=narratorObj.NarratorID,
                    SanadID=_sanadID,
                    Level=narratorTO.level
                )
            )
            
            session.commit()
            print(f"Narrator: '{narratorTO.narratorName}' added successfully.")
            return True

        except Exception as err:
            session.rollback()
            print(f"Error: {err}")
            return False
    
    
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

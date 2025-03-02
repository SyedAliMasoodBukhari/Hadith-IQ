from DataAccessLayer.DataModels import Narrator, Sanad, narrator_sanad,Project
from DataAccessLayer.Narrator.AbsNarratorDAO import AbsNarratorDAO
from typing import List,Dict
from TO.NarratorTO import NarratorTO
from TO.HadithTO import HadithTO
from DataAccessLayer.DbConnection import DbConnectionModel
from DataAccessLayer.UtilDAO import UtilDao
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func
class NarratorDAO(AbsNarratorDAO):
  
    def __init__(self, dbConnection: DbConnectionModel,util :UtilDao):
        self.__dbConnection = dbConnection
        self.__util=util
                
    def insertNarrator(self,sanad: str, narratorTO : NarratorTO)->bool:
        try:
            session: Session = self.__dbConnection.getSession()

            sanadObj = session.query(Sanad).filter(Sanad.sanad == sanad).first()
            if not sanadObj:
                print(f"Sanad '{sanad}' not found.")
                return False
            
            _sanadID = sanadObj.sanadid

            # Check if the narrator already exists
            narratorObj = session.query(Narrator).filter(Narrator.narratorname == narratorTO.narratorName).first()
            if not narratorObj:
                narratorObj = Narrator(
                    narratorname=narratorTO.narratorName,
                    narratorauthenticity="Authentic"  
                )
                session.add(narratorObj)
                session.flush() 
            existing_association = session.query(narrator_sanad).filter(
                narrator_sanad.c.narratorid == narratorObj.NarratorID,
                narrator_sanad.c.sanadid == _sanadID
            ).first()

            if existing_association:
                print(f"Narrator '{narratorTO.narratorName}' is already associated with the sanad.")
                return False

            # Add the association to the narrator_sanad table
            session.execute(
                narrator_sanad.insert().values(
                    narratorid=narratorObj.NarratorID,
                    sanadid=_sanadID,
                    level=narratorTO.level
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
    
    def getAllNarratorsOfProject(self, project_name: str, page: int) -> dict:
        try:
            session: Session = self.__dbConnection.getSession()
            
            project = (
                session.query(Project)
                .options(joinedload(Project.sanads).joinedload(Sanad.narrators))
                .filter_by(projectname=project_name)
                .first()
            )
            
            if not project:
                return {
                    "results": [],
                    "total_pages": 0,
                    "current_page": page,
                }
            sanads = project.sanads

            if not sanads:
                return {
                    "results": [],
                    "total_pages": 0,
                    "current_page": page,
                }

            narrator_names = []
            for sanad in sanads:
                for narrator in sanad.narrators:
                    narrator_names.append(narrator.narratorname)

            per_page = 100
            total_narrators = len(narrator_names)
            total_pages = (total_narrators + per_page - 1) // per_page  # Ceiling division

            # Validate the page number
            if page > total_pages:
                return {
                    "results": [],
                    "total_pages": total_pages,
                    "current_page": page,
                }

            # Get the names for the requested page
            start = (page - 1) * per_page
            end = start + per_page
            paginated_names = narrator_names[start:end]

            return {
                "results": paginated_names,
                "total_pages": total_pages,
                "current_page": page,
            }

        except Exception as e:
            session.rollback()
            print(f"Error retrieving narrators for project '{project_name}': {e}")
            return {
                "results": [],
                "total_pages": 0,
                "current_page": page,
            }
        finally:
            session.close()
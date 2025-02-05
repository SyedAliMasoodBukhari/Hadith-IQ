from DataAccessLayer.DataModels import Hadith, Project, Sanad, hadith_sanad
from DataAccessLayer.Sanad.AbsSanadDAO import AbsSanadDAO
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
from DataAccessLayer.UtilDAO import UtilDao
from DataAccessLayer.DbConnection import DbConnectionModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from TO.SanadTO import SanadTO


class SanadDAO(AbsSanadDAO):
    def __init__(self, db_connection: DbConnectionModel, util: UtilDao):
        self.__dbConnection = db_connection
        self.__util = util

    def insertSanad(self, projectName: str, sanadTO: SanadTO) -> bool:
        try:
            session: Session = self.__dbConnection.getSession()

            sanad = session.query(Sanad).filter(Sanad.Sanad == sanadTO.sanad).first()
            if not sanad:
                sanad = Sanad(Sanad=sanadTO.sanad, SanadAuthenticity=sanadTO.sanadAuthenticity)
                session.add(sanad)
                session.commit()

            if sanad.SanadID:
                print(f"Sanad inserted successfully: {sanadTO.sanad}")
                return self._insertSanadIntojunction(session, projectName, sanadTO)
            return False
        except SQLAlchemyError as e:
            print(f"Error inserting into sanad: {e}")
            session.rollback()
            return False

    def getSanad(self, matn: str) -> List[SanadTO]:
        try:
            session: Session = self.__dbConnection.getSession()
            results = (
                session.query(Sanad.SanadID, Sanad.Sanad, Sanad.SanadAuthenticity)
                .join(hadith_sanad, hadith_sanad.c.SanadID == Sanad.SanadID)
                .join(Hadith, hadith_sanad.c.HadithID == Hadith.HadithID)
                .filter(Hadith.Matn == matn)
                .all()
            )

            sanad_list = [
                SanadTO(
                    sanad_id=row[0],
                    sanad=row[1],
                    sanad_authenticity=row[2],
                    hadithTO=HadithTO(matn=matn)
                )
                for row in results
            ]

            return sanad_list

        except Exception as e:
            print(f"Error getting sanad: {e}")
            return []

    def _insertSanadIntojunction(self,session: Session, projectName: str, sanadTO: SanadTO) -> bool:
        try:
            sanad = session.query(Sanad).filter(Sanad.Sanad == sanadTO.sanad).first()
            hadith = session.query(Hadith).filter(Hadith.Matn == sanadTO.hadithTO.matn).first()
            project = session.query(Project).filter(Project.ProjectName == projectName).first()

            if not sanad or not hadith or not project:
                print(f"Sanad, Hadith, or Project not found.")
                return False
            
            # Associate Sanad with the Hadith
            if sanad not in hadith.sanads:
                hadith.sanads.append(sanad)

            # Associate Sanad with the Project
            if sanad not in project.sanads:
                project.sanads.append(sanad)

            session.commit()
            print(f"Sanad successfully associated.")
            return True
        except SQLAlchemyError as e:
            print(f"Error inserting into hadith_sanad or sanad_project: {e}")
            session.rollback()
            return False

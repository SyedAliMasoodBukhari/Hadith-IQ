from DataAccessLayer.DataModels import Hadith, Project, Sanad, hadith_sanad,Book
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

# Get all Sanads linked to a specific Hadith and their related Projects
    def associate_sanads_with_project_by_book(self,book_name: str, project_name: str):
        try:
            session: Session = self.__dbConnection.getSession()
            # Fetch the Book by its name
            book = session.query(Book).filter_by(BookName=book_name).first()
            
            if not book:
                print(f"Book '{book_name}' not found.")
                return False

            # Fetch the Project by its name
            project = session.query(Project).filter_by(ProjectName=project_name).first()
            
            if not project:
                print(f"Project '{project_name}' not found.")
                return False

            # Iterate over each Hadith in the Book
            for hadith in book.hadiths:
                # Iterate over each Sanad of the Hadith
                for sanad in hadith.sanads:
                    # If the Project is not already associated with the Sanad, associate it
                    if project not in sanad.projects:
                        sanad.projects.append(project)
                        print(f"Project '{project_name}' successfully linked to Sanad '{sanad.Sanad}' of Hadith '{hadith.HadithID}'.")
            
            session.commit()  # Commit the transaction to save the changes
            print(f"Sanads for all Hadiths in Book '{book_name}' successfully associated with Project '{project_name}'.")
            return True

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error: {e}")
            return False
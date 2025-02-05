from DataAccessLayer.DataModels import Book, Hadith, Project,Narrator, narrator_sanad
from DataAccessLayer.Hadith.AbsHadithDAO import AbsHadithDAO
from typing import List
from DataAccessLayer.DbConnection import DbConnectionModel
from TO.HadithTO import HadithTO
from DataAccessLayer.UtilDAO import UtilDao
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class HadithDAO(AbsHadithDAO):
    def __init__(self, dbConnection: DbConnectionModel,util :UtilDao):
        self.__dbConnection = dbConnection
        self.__util=util

    def insertHadith(self, projectName: str, hadithTO: HadithTO) -> bool:
        try:
            session: Session = self.__dbConnection.getSession()

            hadith = session.query(Hadith).filter_by(Matn=hadithTO.matn).first()
            if not hadith:
                hadith = Hadith(
                    Matn=hadithTO.matn,
                    embeddings=hadithTO.matnEmbedding,
                    cleanedMATN=hadithTO.cleanedMatn
                )
                session.add(hadith)
                session.commit()


            # Associate the Hadith with the Project and Book
            if hadith.HadithID: # if inserted
                print(f"Hadith inserted successfully: {hadithTO.matn}")
                return self._insertHadithIntoJunction(session, projectName, hadithTO)
            else:
                return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error inserting Hadith: {e}")
            return False



    def getHadithEmbeddings(self, id:int) -> str:
        raise NotImplementedError("Method not implemented yet.")
        
    def getHadithFirstNarrator(self, matn: str) -> str:
        try:
            session = self.__dbConnection.getSession()
            # Fetch the Hadith record by its Matn (text)
            hadith = session.query(Hadith).filter_by(Matn=matn).first()
            if not hadith:
                print(f"Hadith not found: {matn}")
                return ""

            # Get the first Sanad associated with this Hadith (if any)
            sanad_record = hadith.sanads[0] if hadith.sanads else None
            if not sanad_record:
                print(f"No Sanad found for Hadith: {hadith}")
                return ""

            # Query the narrator_sanad table to get narrators with Level 1 for this Sanad
            first_level_narrators = (
                session.query(Narrator)
                .join(narrator_sanad)  # Join with the narrator_sanad table
                .filter(narrator_sanad.c.SanadID == sanad_record.SanadID)  # Filter by the Sanad
                .filter(narrator_sanad.c.Level == 1)  # Filter by Level 1
                .all()
            )

            if not first_level_narrators:
                print(f"No Level 1 Narrators found for Sanad: {sanad_record.Sanad}")
                return ""

            # Assuming there is one narrator with Level 1, return their name
            narrator = first_level_narrators[0]
            return narrator.NarratorName

        except SQLAlchemyError as e:
            print(f"Error fetching Hadith first narrator: {e}")
            return ""




    
    def getProjectHadithsEmbedding(self, projectName: str) -> dict:
        try:
            session: Session = self.__dbConnection.getSession()

            project = session.query(Project).filter_by(ProjectName=projectName).first()
            if not project:
                raise ValueError(f"Project: '{projectName}' not found.")

            hadith_embeddings = {}

            for hadith in project.hadiths:
                hadith_embeddings[hadith.Matn] = hadith.embeddings

            if not hadith_embeddings:
                print(f"No Hadiths found for project: '{projectName}'.")
            else:
                print(f"Retrieved {len(hadith_embeddings)} Hadith embeddings for project '{projectName}'.")

            return hadith_embeddings

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error in getProjectHadithsEmbedding: {e}")
            return {}
    

    # def _getHadithDetails(self, hadith_id: int) -> dict:
    #     try:
    #         connection = self.__dbConnection.getConnection()
    #         cursor = connection.cursor()
    #         query = "SELECT matn, embeddings FROM hadiths WHERE HadithID= %s"
    #         cursor.execute(query, (hadith_id,))
    #         result = cursor.fetchone()
    #         if result:
    #             return {"matn": result[0], "embedding": result[1]}
    #         else:
    #             return {}
    #     except Exception as e:
    #         print(f"Error in getHadithDetails: {e}")
    #         return {}
    

    # def _getProjectHadithId(self, projectId:int ,hadithId:int) -> int:
    #     try:
    #         connection = self.__dbConnection.getConnection()
    #         cursor = connection.cursor()
    #         query = "SELECT HadithProjectID FROM hadith_project WHERE HadithID=%s AND ProjectID=%s LIMIT 1"
    #         cursor.execute(query, (hadithId,projectId))
    #         result = cursor.fetchone()
    #         if result:
    #             return result[0]  
    #         else:
    #             return -1

    #     except Exception as e: 
    #         print(f"Error fetching Hadith ID: {e}")
    #         return -1
        

    def _insertHadithIntoJunction(self, session: Session, projectName: str, hadithTO: HadithTO) -> bool:
        try:
            book = session.query(Book).filter_by(BookName=hadithTO.bookName).first()
            hadith = session.query(Hadith).filter_by(Matn=hadithTO.matn).first()
            project = session.query(Project).filter_by(ProjectName=projectName).first()

            if not book or not hadith or not project:
                print(f"Book, Hadith or Project not found")
                return False

            # Associate Hadith with the Book
            if book not in hadith.books:
                hadith.books.append(book)

            # Associate Hadith with the Project
            if hadith not in project.hadiths:
                project.hadiths.append(hadith)

            session.commit()
            print(f"Hadith successfully associated.")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error associating Hadith with book and project: {e}")
            return False
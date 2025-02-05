from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataAccessLayer.DataModels import Project, Book, Hadith, Narrator, Sanad
from DataAccessLayer.DbConnection import DbConnectionModel

class UtilDao:
    def __init__(self, db_connection: DbConnectionModel):
        self.__db_connection = db_connection

    def getHadithId(self, matn: str) -> int:
        try:
            session: Session = self.__db_connection.getSession()
            result = session.query(Hadith.HadithID).filter(Hadith.Matn == matn).first()
            if result:
                return result.HadithID
            return -1
        except SQLAlchemyError as e:
            print(f"Error fetching Hadith ID: {e}")
            return -1
        
    def getSanadId(self, sanad: str) -> int:
        try:
            session: Session = self.__db_connection.getSession()
            result = session.query(Sanad.SanadID).filter(Sanad.Sanad == sanad).first()
            if result:
                return result.SanadID
            return -1
        except SQLAlchemyError as e:
            print(f"Error fetching Sanad ID: {e}")
            return -1

    def getNarratorId(self, narrator_name: str) -> int:
        try:
            session: Session = self.__db_connection.getSession()
            result = session.query(Narrator.NarratorID).filter(Narrator.NarratorName == narrator_name).first()
            if result:
                return result.NarratorID
            return -1
        except SQLAlchemyError as e:
            print(f"Error fetching Narrator ID: {e}")
            return -1

    def getProjectId(self, project_name: str) -> int:
        try:
            session: Session = self.__db_connection.getSession()
            result = session.query(Project.ProjectID).filter(Project.ProjectName == project_name).first()
            if result:
                return result.ProjectID
            return -1
        except SQLAlchemyError as e:
            print(f"Error fetching Project ID: {e}")
            return -1
        
    # def getBookId(self, book_name: str) -> int:
    #     try:
    #         session: Session = self.__db_connection.getSession()
    #         result = session.query(Book.BookID).filter(Book.BookName == book_name).first()
    #         if result:
    #             return result.BookID
    #         return -1
    #     except SQLAlchemyError as e:
    #         print(f"Error fetching Hadith ID: {e}")
    #         return -1

    def getBookId(self, book_name: str) -> int:
        try:
            cursor = self.__db_connection.getConnection().cursor()
            query = "SELECT BookID FROM books WHERE BookName = %s LIMIT 1"
            cursor.execute(query, (book_name,))
            result = cursor.fetchone()
            return result[0] if result else -1
        except Exception as e:
            print(f"Error fetching Project ID: {e}")
            return -1

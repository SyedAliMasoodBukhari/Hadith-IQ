from typing import Dict, List
import pandas as pd
from DataAccessLayer.Book.AbsBookDAO import AbsBookDAO
from DataAccessLayer.DataModels import Book, Project
from DataAccessLayer.DbConnection import DbConnectionModel
from DataAccessLayer.UtilDAO import UtilDao
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class BookDAO(AbsBookDAO):
    def __init__(self, dbConnection: DbConnectionModel, util: UtilDao):
        self.__dbConnection = dbConnection
        self.__util = util

    def insertBook(self, projectName: str, bookName: str) -> bool:
        try:
            session: Session = self.__dbConnection.getSession()

            project = session.query(Project).filter_by(ProjectName=projectName).first()
            if not project:
                print(f"Project '{projectName}' does not exist.")
                return False
            
            book = session.query(Book).filter_by(BookName=bookName).first()
            if not book:
                book = Book(BookName=bookName)
                session.add(book)
                session.commit()

            if book in project.books: 
                print(f"Book '{bookName}' is already linked to project '{projectName}'.")
                return True

            project.books.append(book)
            session.commit()
            print(f"Book '{bookName}' added successfully to project '{projectName}'.")
            return True

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error: {e}")
            return False
        

    # def update_progress(self, task_id, progress):
    #     progress_record = self.session.query(Progress).filter_by(task_id=task_id).first()
    #     if progress_record:
    #         progress_record.progress = progress
    #     else:
    #         new_progress = Progress(task_id=task_id, progress=progress)
    #         self.session.add(new_progress)
    #     self.session.commit()

    def deleteBook(self, bookName: str) -> bool:
        return False

    def importBook(self, projectName: str, filePath: str) -> List[Dict[str, str]]:
        try:
            dataFrame = pd.read_csv(filePath,nrows=1000)
            
            _projectID = self.__util.getProjectId(projectName)

            # If project ID is valid, proceed with processing
            if _projectID != -1:
                result_data = []

                if not dataFrame.isnull().values.any():
                    for index, row in dataFrame.iterrows():
                        _book = row["Book"]

                        # Only process rows where "Book" is not empty
                        if _book is not None and _book != "":
                            _sanad = row["Sanad"]
                            _matn = row["Matn"]

                            sanad_dict = {
                                "matn": _matn,
                                "bookname": _book,
                                "sanad": _sanad
                            }

                            result_data.append(sanad_dict)

                return result_data

            return []

        except Exception as e:
            print("Exception", e)
            return []


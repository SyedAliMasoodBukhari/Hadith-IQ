from DataAccessLayer.DataModels import Book, Hadith, Project,Narrator, narrator_sanad,Sanad,hadith_sanad
from DataAccessLayer.Hadith.AbsHadithDAO import AbsHadithDAO
from typing import List
from DataAccessLayer.DbConnection import DbConnectionModel
from TO.HadithTO import HadithTO
from DataAccessLayer.UtilDAO import UtilDao
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import SQLAlchemyError


class HadithDAO(AbsHadithDAO):
    def __init__(self, dbConnection: DbConnectionModel,util :UtilDao):
        self.__dbConnection = dbConnection
        self.__util=util

    def insertHadith(self, hadithTO: HadithTO) -> bool:
        try:
            session: Session = self.__dbConnection.getSession()

            hadith = session.query(Hadith).filter_by(matn=hadithTO.matn).first()
            if not hadith:
                hadith = Hadith(
                    matn=hadithTO.matn,
                    embeddings=hadithTO.matnEmbedding,
                    cleanedmatn=hadithTO.cleanedMatn
                )
                session.add(hadith)
                session.commit()

            if hadith.hadithid:
                print(f"Hadith inserted successfully: {hadithTO.matn}")
                return self._insertHadithIntoJunction(session, hadithTO)
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
            hadith = session.query(Hadith).filter_by(matn=matn).first()
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
                .filter(narrator_sanad.c.sanadid == sanad_record.sanadid)  # Filter by the Sanad
                .filter(narrator_sanad.c.level == 1)  # Filter by Level 1
                .all()
            )

            if not first_level_narrators:
                print(f"No Level 1 Narrators found for Sanad: {sanad_record.sanad}")
                return ""
            narrator = first_level_narrators[0]
            return narrator.narratorname

        except SQLAlchemyError as e:
            print(f"Error fetching Hadith first narrator: {e}")
            return ""




    
    def getProjectHadithsEmbedding(self, projectName: str) -> dict:
        try:
            session: Session = self.__dbConnection.getSession()

            project = session.query(Project).filter_by(projectname=projectName).first()
            if not project:
                raise ValueError(f"Project: '{projectName}' not found.")

            hadith_embeddings = {}

            for hadith in project.hadiths:
                hadith_embeddings[hadith.matn] = hadith.embeddings

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
        

    def _insertHadithIntoJunction(self, session: Session, hadithTO: HadithTO) -> bool:
        try:
            book = session.query(Book).filter_by(bookname=hadithTO.bookName).first()
            hadith = session.query(Hadith).filter_by(matn=hadithTO.matn).first()

            if not book or not hadith :
                print(f"Book, Hadith not found")
                return False
            if book not in hadith.books:
                hadith.books.append(book)

            session.commit()
            print(f"Hadith successfully associated.")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error associating Hadith with book and project: {e}")
            return False
        
    def associate_hadiths_with_project(self, book_name: str, project_name: str):
        try:
            session: Session = self.__dbConnection.getSession()
            # Fetch the Book by its name
            book = session.query(Book).filter_by(bookname=book_name).first()
            if not book:
                print(f"No book found with name '{book_name}'")
                return False

            hadiths = book.hadiths
            if not hadiths:
                print(f"No hadiths found for book '{book_name}'")
                return False

            # Fetch the Project by its name
            project = session.query(Project).filter_by(projectname=project_name).first()
            if not project:
                print(f"No project found with name '{project_name}'")
                return False

            # Associate Hadiths with the Project
            for hadith in hadiths:
                if hadith not in project.hadiths:
                    project.hadiths.append(hadith)

            session.commit()
            print(f"Successfully associated {len(hadiths)} Hadiths from Book '{book_name}' to Project '{project_name}'.")
            return True

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error: {e}")
            return False
    
    def getAllHadithsOfProject(self, project_name: str, page: int) -> dict:
        try:
            session: Session = self.__dbConnection.getSession()
            project = session.query(Project).filter_by(projectname=project_name).first()
            print("here")
            if not project:
                return {
                    "results": [],
                    "total_pages": 0,
                    "current_page": page,
                }
            hadiths = project.hadiths
            print("got hadith")
            if not hadiths:
                return {
                    "results": [],
                    "total_pages": 0,
                    "current_page": page,
                }

            hadiths_list = [{"id": hadith.hadithid, "matn": hadith.matn} for hadith in hadiths]
            per_page = 100
            total_hadiths = len(hadiths_list)
            total_pages = (total_hadiths + per_page - 1) // per_page  
            if page > total_pages:
                return {
                    "results": [],
                    "total_pages": total_pages,
                    "current_page": page,
                }
            start = (page - 1) * per_page
            end = start + per_page
            paginated_hadiths = hadiths_list[start:end]

            return {
                "results": paginated_hadiths,
                "total_pages": total_pages,
                "current_page": page,
            }

        except Exception as e:
            session.rollback()
            print(f"Error retrieving Hadiths for project '{project_name}': {e}")
            return {
                "results": [],
                "total_pages": 0,
                "current_page": page,
            }
        finally:
            session.close()
    
    def getAllHadiths(self, page: int) -> dict:
        try:
            session: Session = self.__dbConnection.getSession()
            
            per_page = 100
            total_hadiths = session.query(Hadith).count()
            total_pages = (total_hadiths + per_page - 1) // per_page  

            if page > total_pages:
                return {
                    "results": [],
                    "total_pages": total_pages,
                    "current_page": page,
                }

            hadiths = session.query(Hadith).offset((page - 1) * per_page).limit(per_page).all()

            hadiths_list = [{"id": hadith.hadithid, "matn": hadith.matn} for hadith in hadiths]

            return {
                "results": hadiths_list,
                "total_pages": total_pages,
                "current_page": page,
            }

        except Exception as e:
            session.rollback()
            print(f"Error retrieving Hadiths: {e}")
            return {
                "results": [],
                "total_pages": 0,
                "current_page": page,
            }
        finally:
            session.close()

    
    def getHadithDetails(self, matn:str) -> dict:
        try:
            session: Session = self.__dbConnection.getSession()
            
            hadith = session.query(Hadith).filter_by(matn=matn).first()
            if not hadith:
                print(f"Hadith not found with matn: {matn}")
                return {}

            sanad_details = []
            for sanad in hadith.sanads: 
                narrators_details = (
                    session.query(Narrator.narratorname, narrator_sanad.c.level)
                    .join(narrator_sanad, Narrator.narratorid == narrator_sanad.c.narratorid)
                    .filter(narrator_sanad.c.sanadid == sanad.sanadid)
                    .order_by(narrator_sanad.c.level)
                    .all()
                )

                narrators_list = [
                    {"narrator_name": narrator, "level": level} 
                    for narrator, level in narrators_details
                ]

                sanad_details.append({
                    "authenticity": sanad.sanadauthenticity,
                    "narrators": narrators_list
                })

            book_names = [book.bookname for book in hadith.books]

            hadith_details = {
                "matn": hadith.matn,
                "sanads": sanad_details,
                "books": book_names
            }

            return hadith_details

        except SQLAlchemyError as e:
            print(f"Error fetching Hadith details: {e}")
            return {}
        finally:
            session.close()

    def searchHadithByNarrator(self, project_name: str, narrator_name: str, page: int) -> dict:
        session: Session = None
        try:
            session = self.__dbConnection.getSession()

            per_page = 100
            query = (
                session.query(Hadith)
                .join(hadith_sanad, hadith_sanad.c.hadithid == Hadith.hadithid)
                .join(Sanad, Sanad.sanadid == hadith_sanad.c.sanadid)
                .join(narrator_sanad, narrator_sanad.c.sanadid == Sanad.sanadid)
                .join(Narrator, Narrator.narratorid == narrator_sanad.c.narratorid)
                .filter(Narrator.narratorname.like(f"%{narrator_name}%"))
            )

            total_hadiths = query.count() 
            total_pages = (total_hadiths + per_page - 1) // per_page

            if page > total_pages:
                return {
                    "results": [],
                    "total_pages": total_pages,
                    "current_page": page,
                }

            hadiths = query.offset((page - 1) * per_page).limit(per_page).all()
            results = [hadith.matn for hadith in hadiths]

            return {
                "results": results,
                "total_pages": total_pages,
                "current_page": page,
            }

        except Exception as e:
            print(f"Error searching Hadith by narrator '{narrator_name}' in project '{project_name}': {e}")
            return {
                "results": [],
                "total_pages": 0,
                "current_page": page,
            }
        finally:
            if session:
                session.close()
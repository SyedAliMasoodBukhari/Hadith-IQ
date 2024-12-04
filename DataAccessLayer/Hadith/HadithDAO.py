from DataAccessLayer.Hadith.AbsHadithDAO import AbsHadithDAO
from typing import List
from DataAccessLayer.DbConnection import DbConnection
from TO.HadithTO import HadithTO
from DataAccessLayer.UtilDAO import UtilDao


class HadithDAO(AbsHadithDAO):

   def __init__(self, db_connection: DbConnection,util :UtilDao):
        self.__db_connection = db_connection
        self.__util=util

   def insertHadith(self, hadithTO: HadithTO) -> bool:
    """Inserts a Hadith record into the database."""
    try:
        connection = self.__db_connection.getConnection()
        cursor = connection.cursor()
        query = """
        INSERT INTO hadiths (matn, embeddings, cleanedMATN) 
        VALUES (%s, %s, %s)
        """
        print(hadithTO.matnEmbedding)
        cursor.execute(query, (hadithTO.matn, hadithTO.matnEmbedding, hadithTO.cleanedMatn))
        connection.commit()
        print(f"Hadith inserted successfully: {hadithTO.matn}")
        return True

    except Exception as e:
        print(f"Error inserting Hadith: {e}")
        return False


   def getHadithEmbeddings(self, id:int) -> str:
        """Placeholder for retrieving Hadith embeddings."""
        raise NotImplementedError("Method not implemented yet.")

   def getProjectHadithsEmbedding(self, projectName: str) -> dict:
    """
    Retrieves a dictionary of Hadiths' matn and their embeddings for a given project.

    :param projectName: The name of the project.
    :return: A dictionary where keys are Hadith matn and values are embeddings.
    """
    try:
        project_id = self.__util.getProjectId(projectName)
        if project_id == -1:
            raise ValueError(f"Project with name '{projectName}' not found.")
        connection = self.__db_connection.getConnection()
        cursor = connection.cursor()
        query = "SELECT HadithID FROM hadith_project WHERE ProjectID = %s"
        cursor.execute(query, (project_id,))
        hadith_ids = cursor.fetchall() 

        if not hadith_ids:
           print(f"No Hadiths found for project '{projectName}'.")
        
        hadith_embeddings = {}

        for (hadith_id,) in hadith_ids:
            hadith_detail = self.getHadithDetails(hadith_id)  
            if hadith_detail:
                hadith_embeddings[hadith_detail["matn"]] = hadith_detail["embedding"]

        return hadith_embeddings

    except Exception as e:
        print(f"Error in getProjectHadithsEmbedding: {e}")
        return {}

   def getHadithDetails(self, hadith_id: int) -> dict:
    """
    Retrieves Hadith details (matn and embedding) based on hadith_id.
    
    :param hadith_id: ID of the Hadith.
    :return: A dictionary with matn and embedding.
    """
    try:
        connection = self.__db_connection.getConnection()
        cursor = connection.cursor()
        query = "SELECT matn, embeddings FROM hadiths WHERE HadithID= %s"
        cursor.execute(query, (hadith_id,))
        result = cursor.fetchone()
        if result:
            return {"matn": result[0], "embedding": result[1]}
        else:
            return {}
    except Exception as e:
        print(f"Error in getHadithDetails: {e}")
        return {}


   def getProjectHadithId(self, projectId:int ,hadithId:int) -> int:
    try:
        connection = self.__db_connection.getConnection()
        cursor = connection.cursor()
        query = "SELECT HadithProjectID FROM hadithproject WHERE HadithID=%s AND ProjectID=%s LIMIT 1"
        cursor.execute(query, (hadithId,projectId))
        result = cursor.fetchone()
        if result:
            return result[0]  
        else:
            return -1

    except Exception as e: 
        print(f"Error fetching Hadith ID: {e}")
        return -1
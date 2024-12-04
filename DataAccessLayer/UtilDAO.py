
class UtilDao:
    def __init__(self, db_connection):
        """
        Initialize the UtilDao with a database connection.
        :param db_connection: The database connection object.
        """
        self.__db_connection = db_connection

    def getHadithId(self, matn: str) -> int:
        """
        Fetches the ID of a Hadith based on the provided matn (text).
        :param matn: The Hadith text (matn) to search for.
        :return: The ID of the Hadith if found, or -1 if not found.
        """
        try:
            cursor = self.__db_connection.getConnection().cursor()
            query = "SELECT HadithID FROM hadiths WHERE matn = %s LIMIT 1"
            cursor.execute(query, (matn,))
            result = cursor.fetchone()
            return result[0] if result else -1
        except Exception as e:
            print(f"Error fetching Hadith ID: {e}")
            return -1

    def getNarratorId(self, narrator_name: str) -> int:
        """
        Fetches the ID of a narrator based on the provided name.
        :param narrator_name: The name of the narrator to search for.
        :return: The ID of the narrator if found, or -1 if not found.
        """
        try:
            cursor = self.__db_connection.getConnection().cursor()
            query = "SELECT NarratorID FROM narrators WHERE NarratorName= %s LIMIT 1"
            cursor.execute(query, (narrator_name,))
            result = cursor.fetchone()
            return result[0] if result else -1
        except Exception as e:
            print(f"Error fetching Narrator ID: {e}")
            return -1

    def getProjectId(self, project_name: str) -> int:
        """
        Fetches the ID of a project based on the provided name.
        :param project_name: The name of the project to search for.
        :return: The ID of the project if found, or -1 if not found.
        """
        try:
            cursor = self.__db_connection.getConnection().cursor()
            query = "SELECT ProjectID FROM projects WHERE ProjectName = %s LIMIT 1"
            cursor.execute(query, (project_name,))
            result = cursor.fetchone()
            return result[0] if result else -1
        except Exception as e:
            print(f"Error fetching Project ID: {e}")
            return -1

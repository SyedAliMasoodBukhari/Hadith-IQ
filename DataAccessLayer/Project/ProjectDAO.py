from DataAccessLayer.DbConnection import DbConnection
from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from DataAccessLayer.UtilDAO import UtilDao
from TO.ProjectTO import ProjectTO
from typing import List


class ProjectDAO(AbsProjectDAO):

    def __init__(self, db_connection: DbConnection, util: UtilDao):
        self.__db_connection = db_connection
        self.__util = util

    def createProject(self, name: str, currentDate: str) -> bool:
        try:
            connection = self.__db_connection.getConnection()

            if connection.is_connected():
                cursor = connection.cursor()
                insert_query = """INSERT INTO projects (name, creation_date) 
                                  VALUES (%s, %s)"""
                cursor.execute(insert_query, (name, currentDate))

                # Commit the transaction
                connection.commit()

                print("Project added successfully.")
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return False

    def saveProject() -> bool:
        return None

    def openExistingProject() -> bool:
        return None

    def renameProject(self, currName: str, newName: str) -> bool:
        return None

    def getProjects(self) -> List[ProjectTO]:
        """
        Retrieves project details based on project_id.
        :param project_id: ID of the Project.
        :return: A list of ProjectTO objects.
        """
        projects = []
        try:
            connection = self.__db_connection.getConnection()
            cursor = connection.cursor()
            query = "SELECT * FROM project"
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                project = ProjectTO(
                    project_id=row[0],
                    project_name=row[1],
                    last_updated=row[2],
                    created_at=row[3]
                )
                projects.append(project)

            return projects
        except Exception as e:
            print(f"Error in getProject: {e}")
            return []

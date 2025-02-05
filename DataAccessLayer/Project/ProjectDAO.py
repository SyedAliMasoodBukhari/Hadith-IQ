from DataAccessLayer.DbConnection import DbConnectionModel
from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from DataAccessLayer.UtilDAO import UtilDao
from TO.ProjectTO import ProjectTO
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataAccessLayer.DataModels import Project
from typing import List


class ProjectDAO(AbsProjectDAO):

    def __init__(self, dbConnection: DbConnectionModel, util: UtilDao):
        self.__dbConnection = dbConnection
        self.__util = util

    def createProject(self, name: str, creationDate: str) -> bool:
        try:
            newProject = Project(ProjectName=name)

            session: Session = self.__dbConnection.getSession()
            session.add(newProject)
            session.commit()

            # If commit successful
            if newProject.ProjectID:
                print("Project added successfully.")
                return True
            else:
                print("Project not inserted.")
                return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error: {e}")
            return False
        finally:
            session.close()

    def saveProject() -> bool:
        return None

    def renameProject(self, currName: str, newName: str) -> bool:
        try:
            session: Session = self.__dbConnection.getSession()
            project = session.query(Project).filter_by(ProjectName=currName).first()
            if not project:
                print(f"Project with name '{currName}' not found.")
                return False
            if project.ProjectName != currName:
                print(f"Project with name '{currName}' is not same as '{project.ProjectName}'.")
                return False
            
            project.ProjectName = newName
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error renaming project: {e}")
            return False

        finally:
            session.close()

    def getProjects(self) -> List[ProjectTO]:
        try:
            projects = []
            session: Session = self.__dbConnection.getSession()
            results = session.query(Project).all()
            for project in results:
                projectTO = ProjectTO(
                    project.ProjectID,
                    project.ProjectName,
                    project.LastUpdated.strftime("%d-%m-%Y") if project.LastUpdated else None,
                    project.CreatedAt.strftime("%d-%m-%Y") if project.CreatedAt else None,
                )
                projects.append(projectTO)
            return projects
        except Exception as e:
            print(f"Error in getProjects: {e}")
            return []
        finally:
            session.close()


    def deleteProject(self, projectName: str) -> bool:
        try:
            session: Session = self.__dbConnection.getSession()
            project = session.query(Project).filter_by(ProjectName=projectName).first()
            
            if not project:
                print(f"Project with name '{projectName}' not found.")
                return False
            
            session.delete(project)
            session.commit()
            return True

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting project: {e}")
            return False

        finally:
            session.close()

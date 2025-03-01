from DataAccessLayer.DbConnection import DbConnectionModel
from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from DataAccessLayer.UtilDAO import UtilDao
from TO.ProjectTO import ProjectTO
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataAccessLayer.DataModels import Project,ProjectState
from typing import List
import json
from datetime import datetime,timezone


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

##################################################################ProjectState

    def saveProjectState(self, projectName: str, stateData: dict,query :str) -> bool:
        session = None
        try:
            projectId = self.__util.getProjectId(projectName)
            if projectId == -1:
                print(f"Project with name '{projectName}' not found.")
                return False

            session: Session = self.__dbConnection.getSession()
            
            # Fetch the existing project state
            state_entry = session.query(ProjectState).filter(
                        ProjectState.ProjectID == projectId,
                        ProjectState.Query == query
                    ).first()
            if state_entry:
                existing_state = json.loads(state_entry.StateData) if state_entry.StateData else {}
                
                # Append new hadiths while preventing duplicates
                existing_hadiths = set(existing_state.get("hadiths", []))  # Convert to set to remove duplicates
                new_hadiths = set(stateData.get("hadiths", []))
                
                combined_hadiths = list(existing_hadiths.union(new_hadiths))  # Merge without duplicates
                
                # Update state data
                existing_state["hadiths"] = combined_hadiths
                state_entry.StateData = json.dumps(existing_state)
            else:
                # If no existing entry, create a new one
                new_state = ProjectState(ProjectID=projectId, Query=query,StateData=json.dumps(stateData))
                session.add(new_state)

            # Update the last updated time in the Projects table
            project_entry = session.query(Project).filter_by(ProjectID=projectId).first()
            if project_entry:
                project_entry.LastUpdated = datetime.now(timezone.utc)

            session.commit()
            print("Project state saved successfully, and LastUpdated time updated.")
            return True
        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(f"Error saving project state: {e}")
            return False
        finally:
            if session:
                session.close()

    def getProjectState(self, projectName: str) -> list:
        session = None
        try:
            projectId = self.__util.getProjectId(projectName)
            if projectId == -1:
                print(f"Project with name '{projectName}' not found.")
                return []

            session: Session = self.__dbConnection.getSession()
            
            # Fetch all Query and StateData records for the project
            state_entries = session.query(ProjectState.Query, ProjectState.StateData).filter(
                ProjectState.ProjectID == projectId
            ).all()
            
            if not state_entries:
                print(f"No project state found for '{projectName}'.")
                return []

            # Convert the result into a list of dictionaries
            result = [{"Query": entry.Query, "StateData": json.loads(entry.StateData)} for entry in state_entries]
            
            return result

        except SQLAlchemyError as e:
            print(f"Error fetching project state: {e}")
            return None
        finally:
            if session:
                session.close()

    def getSingleProjectState(self, name: str, query: str) -> dict:
        session = None
        try:
            projectId = self.__util.getProjectId(name)
            if projectId == -1:
                print(f"Project with name '{name}' not found.")
                return {}

            session: Session = self.__dbConnection.getSession()
            
            # Fetch the specific state entry for the given project and query
            state_entry = session.query(ProjectState.StateData).filter(
                ProjectState.ProjectID == projectId,
                ProjectState.Query == query
            ).first()
            
            if not state_entry:
                print(f"No project state found for '{name}' with query '{query}'.")
                return {}

            # Parse and return the state data as a dictionary
            return json.loads(state_entry.StateData)

        except SQLAlchemyError as e:
            print(f"Error fetching project state: {e}")
            return None
        finally:
            if session:
                session.close()
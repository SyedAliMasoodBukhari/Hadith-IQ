from DataAccessLayer.DbConnection import DbConnectionModel
from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from DataAccessLayer.UtilDAO import UtilDao
from TO.ProjectTO import ProjectTO
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataAccessLayer.DataModels import Hadith, Project,ProjectState
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
            if newProject.projectid:
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
            project = session.query(Project).filter_by(projectname=currName).first()
            if not project:
                print(f"Project with name '{currName}' not found.")
                return False
            if project.projectname != currName:
                print(f"Project with name '{currName}' is not same as '{project.projectname}'.")
                return False
            
            project.projectname = newName
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
            project = session.query(Project).filter_by(projectname=projectName).first()
            
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


    def saveProjectState(self, projectName: str, stateData: List[str], query: str) -> bool:
        session = None
        try:
            projectId = self.__util.getProjectId(projectName)
            if projectId == -1:
                print(f"Project with name '{projectName}' not found.")
                return False

            session: Session = self.__dbConnection.getSession()
            hadith_ids = []
            for matn in stateData:
                hadith_id = self.__util.getHadithId(matn)
                if hadith_id != -1:
                    hadith_ids.append(hadith_id)
                else:
                    print(f"Hadith with matn '{matn}' not found.")

            state_json = {
                "query": query,
                "hadith": hadith_ids
            }

            state_entry = session.query(ProjectState).filter(
                ProjectState.projectid == projectId,
                ProjectState.query == query
            ).first()

            if state_entry:
                # Parse JSON safely
                if isinstance(state_entry.statedata, str):  
                    try:
                        existing_state = json.loads(state_entry.statedata)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        existing_state = {}  # Default to an empty dictionary
                else:
                    existing_state = {}

                print(f"Parsed statedata: {existing_state}, Type: {type(existing_state)}")

                existing_hadiths = set(existing_state.get("hadith", []))  
                new_hadiths = set(hadith_ids)  
                combined_hadiths = list(existing_hadiths.union(new_hadiths))  
                existing_state["hadith"] = combined_hadiths  
                state_entry.statedata = json.dumps(existing_state)  
            else:
                new_state = ProjectState(
                    projectid=projectId,
                    query=query,
                    statedata=json.dumps(state_json)  
                )
                session.add(new_state)

            # Update project's lastupdated timestamp
            project_entry = session.query(Project).filter_by(projectid=projectId).first()
            if project_entry:
                project_entry.lastupdated = datetime.now(timezone.utc)

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


    def getProjectState(self, projectName: str) -> List[str]:
        session = None
        try:
            projectId = self.__util.getProjectId(projectName)
            if projectId == -1:
                print(f"Project with name '{projectName}' not found.")
                return []

            session: Session = self.__dbConnection.getSession()
            state_entries = session.query(ProjectState.query).filter(
                ProjectState.projectid == projectId
            ).all()
            
            if not state_entries:
                print(f"No project state found for '{projectName}'.")
                return []
            
            result = [entry.query for entry in state_entries]
            
            return result

        except SQLAlchemyError as e:
            print(f"Error fetching project state: {e}")
            return []
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
            state_entry = session.query(ProjectState).filter(
                ProjectState.projectid == projectId,
                ProjectState.query == query
            ).first()

            if not state_entry:
                print(f"No project state found for '{name}' with query '{query}'.")
                return {}
            if isinstance(state_entry.statedata, str):
                try:
                    state_data = json.loads(state_entry.statedata)
                    if isinstance(state_data, str): 
                        state_data = json.loads(state_data)
                except json.JSONDecodeError as e:
                    state_data = {}  
            else:
                state_data = state_entry.statedata or {}

            hadith_ids = set(state_data.get("hadith", []))  
            hadith_matn_list = []
            
            for hadith_id in hadith_ids:
                hadith = session.query(Hadith.matn).filter_by(hadithid=hadith_id).first()
                if hadith:
                    hadith_matn_list.append(hadith.matn)
            
            return {
                "query": query,
                "matn": hadith_matn_list
            }

        except json.JSONDecodeError as e: 
            print(f"Error parsing JSON from statedata: {e}")
            return {}

        except Exception as e:
            print(f"Error fetching project state: {e}")
            return {}

        finally:
            if session:
                session.close()


    def mergeProjectState(self, projectname: str, query_names: List[str], queryname: str) -> bool:
        session = None
        try:
            projectId = self.__util.getProjectId(projectname)
            if projectId == -1:
                print(f"Project with name '{projectname}' not found.")
                return False
            print("1")

            session: Session = self.__dbConnection.getSession()
            existing_state = session.query(ProjectState).filter(
                ProjectState.projectid == projectId,
                ProjectState.query == queryname
            ).first()

            if existing_state:
                print(f"Error: Query name '{queryname}' already exists in the database.")
                return False  
            print("here i am getting states")

            states = []
            for query in query_names:
                state = session.query(ProjectState).filter(
                    ProjectState.projectid == projectId,
                    ProjectState.query == query
                ).first()
                if state:
                    states.append(state)

            if not states:
                print(f"No state data found for queries '{', '.join(query_names)}'.")
                return False
            
            merged_state_data = []
            for state in states:
                if state and state.statedata:
                    merged_state_data.append(state.statedata)  

            new_state_data_str = json.dumps(merged_state_data)
            print("new state=merge")
            new_state = ProjectState(
                projectid=projectId,
                query=queryname,
                statedata=new_state_data_str  
            )
            print("here")
            session.add(new_state)

            delete_query = session.query(ProjectState).filter(
                ProjectState.projectid == projectId,
                ProjectState.query.in_(query_names)
            )

            project_entry = session.query(Project).filter_by(projectid=projectId).first()
            if project_entry:
                project_entry.lastupdated = datetime.now(timezone.utc)

            session.commit()
            delete_query.delete(synchronize_session=False)
            session.commit()
            print(f"Merged state saved as '{queryname}', and old states for '{', '.join(query_names)}' deleted.")
            return True

        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(f"Error merging project state: {e}")
            return False
        finally:
            if session:
                session.close()
    
    def renameQueryOfState(self, project_name: str, old_query_name: str, new_query_name: str) -> bool:
        session = None
        try:
            project_id = self.__util.getProjectId(project_name)
            if project_id == -1:
                print(f"Project with name '{project_name}' not found.")
                return False

            session: Session = self.__dbConnection.getSession()
            existing_state = session.query(ProjectState).filter(
                ProjectState.projectid == project_id,
                ProjectState.query == new_query_name
            ).first()

            if existing_state:
                print(f"Error: Query name '{new_query_name}' already exists in the database.")
                return False
            old_states = session.query(ProjectState).filter(
                ProjectState.projectid == project_id,
                ProjectState.query == old_query_name
            )
            count = old_states.count() 
            print(f"Found {count} rows matching '{old_query_name}'.")

            if count == 0:
                print(f"No states found for query '{old_query_name}'.")
                return False
            old_states.update({ProjectState.query: new_query_name}, synchronize_session=False)

            project_entry = session.query(Project).filter_by(projectid=project_id).first()
            if project_entry:
                project_entry.lastupdated = datetime.now(timezone.utc)

            session.commit()
            print(f"Query '{old_query_name}' renamed to '{new_query_name}' and states updated.")
            return True

        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(f"Error renaming query: {e}")
            return False
        finally:
            if session:
                session.close()
    def deleteState(self, project_name: str, query_name: str) -> bool:
        session = None
        try:
            project_id = self.__util.getProjectId(project_name)
            if project_id == -1:
                print(f"Project with name '{project_name}' not found.")
                return False
            session: Session = self.__dbConnection.getSession()
            states_to_delete = session.query(ProjectState).filter(
                ProjectState.projectid == project_id,
                ProjectState.query == query_name
            )
            count = states_to_delete.count()
            if count == 0:
                print(f"No states found for query '{query_name}' in project '{project_name}'.")
                return False
            states_to_delete.delete(synchronize_session=False)
            project_entry = session.query(Project).filter_by(projectid=project_id).first()
            if project_entry:
                project_entry.lastupdated = datetime.now(timezone.utc)
            session.commit()
            print(f"Deleted {count} states for query '{query_name}' in project '{project_name}'.")
            return True

        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(f"Error deleting state: {e}")
            return False
        finally:
            if session:
                session.close()
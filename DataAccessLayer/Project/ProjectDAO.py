import re
from DataAccessLayer.DbConnection import DbConnectionModel
from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from DataAccessLayer.UtilDAO import UtilDao
from TO.ProjectTO import ProjectTO
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataAccessLayer.DataModels import Hadith, Project,ProjectState
from typing import List, Dict,Set
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

    def saveProjectState(self, projectName: str, stateData: list, query: str) -> bool:
        session = None
        try:
            projectId = self.__util.getProjectId(projectName)
            if projectId == -1:
                print(f"Project with name '{projectName}' not found.")
                return False

            session: Session = self.__dbConnection.getSession()
            hadith_ids = []

            # Retrieve Hadith IDs
            for matn in stateData:
                hadith_id = self.__util.getHadithId(matn)
                if hadith_id != -1:
                    hadith_ids.append(hadith_id)
                else:
                    print(f"Hadith with matn '{matn}' not found.")

            # Convert Hadith IDs to a comma-separated string
            new_state_str = ",".join(map(str, hadith_ids))

            # Query the existing state entry
            state_entry = session.query(ProjectState).filter(
                ProjectState.projectid == projectId,
                ProjectState.query == query
            ).first()

            if state_entry:
                # Update the existing state entry
                stored_data = state_entry.statedata.strip('"') if isinstance(state_entry.statedata, str) else ""
                existing_hadiths = set(map(int, stored_data.split(","))) if stored_data else set()
                combined_hadiths = sorted(existing_hadiths.union(set(hadith_ids)))
                updated_state_str = ",".join(map(str, combined_hadiths))

                # Use synchronize_session='fetch' to ensure session consistency
                session.query(ProjectState).filter(
                    ProjectState.projectid == projectId,
                    ProjectState.query == query
                ).update(
                    {"statedata": updated_state_str},
                    synchronize_session='fetch'
                )
            else:
                # Create a new state entry
                new_state = ProjectState(
                    projectid=projectId,
                    query=query,
                    statedata=new_state_str
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


    

    def get_matn_for_hadith_ids(self,hadith_ids: List[str], session) -> Dict[str, str]:
        matn_dict = {}
        for hadith_id in hadith_ids:
            hadith = session.query(Hadith).filter(Hadith.hadithid == hadith_id).first()
            if hadith:
                matn_dict[hadith_id] = hadith.matn
        return matn_dict


    def clean_hadith_id(self,hadith_id: str) -> str:
        """
        Cleans the hadith_id by removing extra quotes and invalid characters.
        """
        # Remove any non-digit characters
        cleaned_id = re.sub(r"[^\d]", "", hadith_id)
        return cleaned_id


    def parse_statedata(self,statedata: str) -> Set[str]:
        """
        Extracts unique hadith_ids from the statedata string.
        """
        unique_hadith_ids = set()
        # Use regex to split the string by commas that are outside of query:hadith_ids pairs
        entries = re.split(r",(?=\w+:\d)", statedata)

        for entry in entries:
            if ":" in entry:
                # Split into query and hadith_ids
                _, hadith_ids_str = entry.split(":", 1)
                # Split hadith_ids into a list and clean each hadith_id
                hadith_ids = [self.clean_hadith_id(hid) for hid in hadith_ids_str.split(",")]
                unique_hadith_ids.update(hadith_ids)
            else:
                # Handle cases where the entry is just a hadith_id (no query)
                if re.match(r"^\d+$", entry):
                    cleaned_id = self.clean_hadith_id(entry)
                    unique_hadith_ids.add(cleaned_id)

        return unique_hadith_ids


    def getSingleProjectState(self, projectName: str, query_names: str) -> List[str]:
        project_id = self.__util.getProjectId(projectName)
        if project_id == -1:
            print(f"Project with name '{projectName}' not found.")
            return []

        session: Session = self.__dbConnection.getSession()
        try:
            # Fetch the state for the given query
            state = session.query(ProjectState).filter(
                ProjectState.projectid == project_id,
                ProjectState.query == query_names
            ).first()

            if state and state.statedata:
                hadith_ids = state.statedata.strip('"').split(",") if state.statedata else []
                print("Hadith IDs:", hadith_ids)
                matn_list = []
                for hadith_id in hadith_ids:
                    cleaned_id = self.clean_hadith_id(hadith_id)
                    if cleaned_id:
                        hadith = session.query(Hadith).filter(Hadith.hadithid == int(cleaned_id)).first()
                        if hadith:
                            matn_list.append(hadith.matn)

                return matn_list
            else:
                print(f"No state data found for query '{query_names}'.")
                return []
        finally:
            session.close()

    def mergeProjectState(self, projectname: str, query_names: List[str], queryname: str) -> bool:
        session = None
        try:
            projectId = self.__util.getProjectId(projectname)
            if projectId == -1:
                print(f"Project with name '{projectname}' not found.")
                return False

            session: Session = self.__dbConnection.getSession()
            existing_state = session.query(ProjectState).filter(
                ProjectState.projectid == projectId,
                ProjectState.query == queryname
            ).first()

            if existing_state:
                print(f"Error: Query name '{queryname}' already exists in the database.")
                return False
            merged_hadith_ids = set() 
            for query in query_names:
                state = session.query(ProjectState).filter(
                    ProjectState.projectid == projectId,
                    ProjectState.query == query
                ).first()

                if state and state.statedata:
                    cleaned_data = state.statedata.strip('"')
                    hadith_ids = cleaned_data.split(",") if cleaned_data else []
                    for hadith_id in hadith_ids:
                        if hadith_id.strip().isdigit():
                            merged_hadith_ids.add(hadith_id.strip())

            if not merged_hadith_ids:
                print(f"No valid state data found for queries '{', '.join(query_names)}'.")
                return False
            new_state_data_str = ",".join(sorted(merged_hadith_ids))  
            print(f"Merged state data: {new_state_data_str}")
            new_state = ProjectState(
                projectid=projectId,
                query=queryname,
                statedata=new_state_data_str
            )
            session.add(new_state)
            project_entry = session.query(Project).filter_by(projectid=projectId).first()
            if project_entry:
                project_entry.lastupdated = datetime.now(timezone.utc)

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

    def removeHadithFromState(self, matn_list: List[str], projectName: str, stateQuery: str) -> bool:
        session = None
        try:
            session: Session = self.__dbConnection.getSession()
            project_id = self.__util.getProjectId(projectName)
            if project_id == -1:
                print(f"Project with name '{projectName}' not found.")
                return False

            existing_state = session.query(ProjectState).filter(
                ProjectState.projectid == project_id,
                ProjectState.query == stateQuery
            ).first()

            if not existing_state:
                print(f"No state found for project ID '{project_id}' and query '{stateQuery}'.")
                return False

            existing_state_query = existing_state.statedata  # Direct string handling
            updated_state_query = existing_state_query

            for matn in matn_list:
                hadith_id = self.__util.getHadithId(matn)
                if not hadith_id:
                    print(f"No hadith_id found for matn: '{matn}'.")
                    continue  
                if str(hadith_id) not in updated_state_query:
                    print(f"Hadith ID '{hadith_id}' not found in stateQuery for matn: '{matn}'.")
                    continue  
                updated_state_query = self.remove_hadith_id_from_state_query(updated_state_query, str(hadith_id))
                print(f"Hadith ID '{hadith_id}' successfully removed from stateQuery for matn: '{matn}'.")
                updated_state_query = updated_state_query.strip(",") 
                updated_state_query = updated_state_query.strip('"')  
            
            session.query(ProjectState).filter(
                ProjectState.projectid == project_id,
                ProjectState.query == stateQuery
            ).update(
                {"statedata": updated_state_query},  # Direct string update
                synchronize_session='fetch'
            )
            session.commit()
            print("State updated successfully.")
            return True

        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(f"Error deleting state: {e}")
            return False
        finally:
            if session:
                session.close()

    def remove_hadith_id_from_state_query(self, stateQuery: str, hadith_id: str) -> str:
        updated_state_query = stateQuery.replace(f",{hadith_id},", ",")
        updated_state_query = updated_state_query.replace(f"{hadith_id},", "")
        updated_state_query = updated_state_query.replace(f",{hadith_id}", "")
        updated_state_query = updated_state_query.replace(f"{hadith_id}", "")
        return updated_state_query.strip(",")

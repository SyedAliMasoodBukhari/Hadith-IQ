import datetime
from BusinessLogicLayer.Project.AbsProjectBO import AbsProjectBO
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from typing import List
from TO.ProjectTO import ProjectTO

class ProjectBO(AbsProjectBO):
    
    def __init__(self, dalFascade: AbsDALFascade):
        self.__dalFascade = dalFascade

    @property
    def dalFascade(self) -> AbsDALFascade:
        return self.__dalFascade

    @dalFascade.setter
    def dalFascade(self, value):
        self.__dalFascade = value

    def _getCurrentDate(self) -> str:
        return datetime.now().strftime("%d-%m-%Y")

    def createProject(self, name: str) -> bool:
        currentDate = self._getCurrentDate()
        if not self.dalFascade.createProject(name, currentDate):  # If createProject returns False
            print(f"Failed to create Project: {name}")
            return False  
        return True 
    
    def getProjects(self)->List[str]:
        try:
            projects = self.dalFascade.getProjects()
            return projects
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []
        

    def saveProject(self)->bool:
        return None
 
    def openExistingProject(self)->bool:
        return None
 
    def renamepProject(self,currName:str,newName:str)->bool:
        return None


# # Main Function
# def main():
#     # Create an instance of AbsDALFascade (replace with your actual implementation)
#     dbconnection = DbConnection()
#     utilDAO= UtilDao(dbconnection)
#     hadithDAO= HadithDAO(dbconnection,utilDAO)
#     narratorDAO= NarratorDAO(dbconnection,utilDAO)
#     projectDAO= ProjectDAO(dbconnection,utilDAO)
#     sanadDAO= SanadDAO(dbconnection,utilDAO)
#     dalFascade= DALFascade(hadithDAO,sanadDAO,projectDAO,narratorDAO) # Replace with a concrete implementation of AbsDALFascade
#     # Create an instance of HadithBO
#     hadithBO= HadithBO(dalFascade)
#     narratorBO= NarratorBO(dalFascade)
#     projectBO= ProjectBO(dalFascade)
#     sanadBO= SanadBO(dalFascade)
#     bllFascade= BLLFascade(hadithBO,sanadBO,projectBO,narratorBO)
#      # Example of Hadith text (Matn)
#     print(projectBO.getProjects())

# if __name__ == "__main__":
#     main()
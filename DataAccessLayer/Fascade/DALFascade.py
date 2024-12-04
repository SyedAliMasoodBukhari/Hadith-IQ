import datetime
from typing import List
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from DataAccessLayer.Narrator.AbsNarratorDAO import AbsNarratorDAO
from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from DataAccessLayer.Sanad.AbsSanadDAO import AbsSanadDAO
from TO.HadithTO import HadithTO
from DataAccessLayer.Hadith.AbsHadithDAO import AbsHadithDAO
from TO.ProjectTO import ProjectTO
class DALFascade(AbsDALFascade):
    
    #ABSHadithDAO initializer
    def __init__(self,hadithDAO:AbsHadithDAO, sanadDAO:AbsSanadDAO, projectDAO:AbsProjectDAO, narratorDAO:AbsNarratorDAO):
        self.__hadithDAO=hadithDAO
        self.__projectDAO=projectDAO
        self.__sanadDAO=sanadDAO
        self.__narratorDAO=narratorDAO
  
    
    def insertHadith(self,hadithTO:HadithTO)->bool:
        return self.__hadithDAO.insertHadith(hadithTO)
    
    def createProject(self,name:str, currentDate: datetime)->bool:
        return self.__projectDAO.createProject(name, currentDate)
    
    def getProjects(self, project_id: int) -> List[ProjectTO]:
        return self.__projectDAO.getProjects(project_id)

    def getHadithDetails(self,hadithTO:HadithTO)->dict:
        return self.__hadithDAO.getHadithDetails(hadithTO)
    
    def getProjectHadithsEmbedding(self, projectName:str) -> dict:
        return self.__hadithDAO.getProjectHadithsEmbedding(projectName)
    
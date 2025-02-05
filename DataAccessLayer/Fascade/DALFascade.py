import datetime
from typing import Dict, List
from DataAccessLayer.Book.AbsBookDAO import AbsBookDAO
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from DataAccessLayer.Narrator.AbsNarratorDAO import AbsNarratorDAO
from DataAccessLayer.Project.AbsProjectDAO import AbsProjectDAO
from DataAccessLayer.Sanad.AbsSanadDAO import AbsSanadDAO
from TO.HadithTO import HadithTO
from DataAccessLayer.Hadith.AbsHadithDAO import AbsHadithDAO
from TO.NarratorTO import NarratorTO
from TO.ProjectTO import ProjectTO
from TO.SanadTO import SanadTO
class DALFascade(AbsDALFascade):
    
    #ABSHadithDAO initializer
    def __init__(self,projectDAO:AbsProjectDAO, bookDAO: AbsBookDAO, hadithDAO:AbsHadithDAO, sanadDAO:AbsSanadDAO,  narratorDAO:AbsNarratorDAO):     
        self.__projectDAO=projectDAO
        self.__bookDAO = bookDAO
        self.__hadithDAO=hadithDAO
        self.__sanadDAO=sanadDAO
        self.__narratorDAO=narratorDAO
  
    #AbsProject Functions

    def createProject(self,name:str, creationDate: str)->bool:
        return self.__projectDAO.createProject(name, creationDate)
    
    def renameProject(self,currName:str,newName:str)->bool:
        return self.__projectDAO.renameProject(currName, newName)
    
    def getProjects(self) -> List[ProjectTO]:
        return self.__projectDAO.getProjects()
    
    def deleteProject(self, projectName: str) -> bool:
        return self.__projectDAO.deleteProject(projectName)
    
    #AbsBook Functions

    def insertBook(self,projectName:str,bookName:str)->bool:
        return self.__bookDAO.insertBook(projectName,bookName)

    def deleteBook(self,bookName:str)->bool:
        return self.__bookDAO.deleteBook(bookName)
    
    def importBook(self, projectName: str, filePath: str) -> List[Dict[str, str]]:
        return self.__bookDAO.importBook(projectName, filePath)
    
    #AbsHadith Functions
    
    def insertHadith(self, projectName: str, hadithTO: HadithTO) -> bool:
        return self.__hadithDAO.insertHadith(projectName, hadithTO)

    def getHadithDetails(self,hadithTO:HadithTO)->dict:
        return self.__hadithDAO._getHadithDetails(hadithTO)
    
    def getProjectHadithsEmbedding(self, projectName:str) -> dict:
        return self.__hadithDAO.getProjectHadithsEmbedding(projectName)
    
    def getHadithFirstNarrator(self, hadith:str) -> str:
        return self.__hadithDAO.getHadithFirstNarrator(hadith)
    #AbsSanad Function
    
    def insertSanad(self, projectName: str, sanadTO: SanadTO) -> bool:
        return self.__sanadDAO.insertSanad(projectName, sanadTO)

    def getSanad(self,matn:str)->List[SanadTO]:
        return self.__sanadDAO.getSanad(matn)

    #AbsNarrator Function
    def insertNarrator(self,sanad: str, narratorTO : NarratorTO)->bool:
        return self.__narratorDAO.insertNarrator(sanad, narratorTO)
    
    def getAllNarrators(self)->List[NarratorTO]:
        return self.__narratorDAO.getAllNarrators()
    
    def getSimilarNarrator(self,NarratorTO:NarratorTO)->List[NarratorTO]:
        return self.__narratorDAO.getsSimilarNarrator(NarratorTO)
    
    def getNarratedHadith(self,NarratorTO:NarratorTO)->List[HadithTO]:
        return self.__narratorDAO.getNarratedHadith(NarratorTO)

    def getNarratorDetails(self,NarratorTO:NarratorTO)->Dict:
        return self.__narratorDAO.getNarratorDetails(NarratorTO)
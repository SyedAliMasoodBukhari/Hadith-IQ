from AbsDALFascade import AbsDALFascade
from typing import List,Dict
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
from TO.OpinionTO import OpinionTO
from TO.SanadTO import SanadTO
from TO.ProjectTO import ProjectTO
from AbsProjectDAO import AbsProjectDAO
from AbsHadithDAO import AbsHadithDAO
from AbsSanadDAO import AbsSanadDAO
from AbsOpinionDAO import AbsOpinionDAO
from AbsNarratorDAO import AbsNarratorDAO
class DALFascade(AbsDALFascade):
    #ProjectDAO initializer
    def __init__(self,projectDAO:AbsProjectDAO):
        self.__projectDAO=projectDAO
    
    #ABSHadithDAO initializer
    def __init__(self,hadithDAO:AbsHadithDAO):
        self.__hadithDAO=hadithDAO
    
    #SanadDAO initializer
    def __init__(self,sanadDAO:AbsSanadDAO):
        self.__sanadDAO=sanadDAO
    
    #AbsNarratorDAO initializer
    def __init__(self,narratorDAO:AbsNarratorDAO):
        self.__narratorDAO=narratorDAO
    
    #OpinionDAO initializer
    def __init__(self,opinionDAO:AbsOpinionDAO):
        self.__opinioDAO=opinionDAO
    

    #ProjectDAO Functions
    
    def createProject(self,name:str)->bool:
        return self.__projectDAO.createProject(name)
    
    
    def saveProject(self)->bool:
        return self.__projectDAO.saveProject()
    
    
    def openExistingProject(self)->bool:
        return self.__projectDAO.openExistingProject()
    
    def renameProject(self,currName:str,newName:str)->bool:
        return self.__projectDAO.renameProject(currName,newName)

    
    def getProjects(self)->List[ProjectTO]:
        return self.__projectDAO.getProjects()

    #HadithDAO Function
    #Donot Change Below
    
    def insertHadith(self,hadithTO:HadithTO)->bool:
        return self.__hadithDAO.insertHadith(hadithTO)
    
    
    def insertHadithEmbeddings(self,matn:str,embeddings:List[float])->bool:
        return self.__hadithDAO.insertHadithEmbeddings(matn,embeddings)


    def getHadithEmbeddings(self,matn:str)->List[float]:
        return self.__hadithDAO.getHadithEmbeddings(matn)

    
    def getAllHadith(self) -> List[HadithTO]:
        return self.__hadithDAO.getAllHadith()

    
    def insertHadithAuthenticity(self,hadithTO:HadithTO)->bool:
        return self.__hadithDAO.insertHadithAuthenticity(hadithTO)

    
    def getHadithDetails(self,hadithTO:HadithTO)->Dict[str,any]:
        return self.__hadithDAO.getHadithDetails(hadithTO)

    #NarratorDAO Functions


    def insertNarrator(self,narratorTO : NarratorTO)->bool:
        return self.__narratorDAO.insertNarrator(narratorTO)
    
    
    def getAllNarrators(self)->List[NarratorTO]:
        return self.__narratorDAO.getAllNarrators()
    
    
    def getsSimilarNarrator(self,NarratorTO:NarratorTO)->List[NarratorTO]:
        return self.__narratorDAO.getsSimilarNarrator(NarratorTO)
    
    
    def importNarratorOpinion(self,File:str)->bool:
        return self.__narratorDAO.importNarratorOpinion(File)
    
    
    def getNarratedHadith(self,NarratorTO:NarratorTO)->List[HadithTO]:
     return self.__narratorDAO.getNarratedHadith(NarratorTO)

    
    def getNarratorDetails(self,NarratorTO:NarratorTO)->Dict:
        return self.__narratorDAO.getNarratorDetails(NarratorTO)


    #SanadDAO Functions
    
    def insertSanad(self,HadithTO:HadithTO)->bool:
        return self.__sanadDAO.insertSanad(HadithTO)

    
    def getSanad(self,matn:str)->List[NarratorTO]:
        return self.__sanadDAO.getSanad(matn)
    
    #OpinionDAO Functions
    
    def insertOpinion(self,NarratorTO:NarratorTO,opinion:str)->bool:
        return self.__opinioDAO.insertOpinion(NarratorTO,opinion)
    
    
    def getOpinions(self,NarratorTO:NarratorTO)->List[OpinionTO]:
        return self.__opinioDAO.getOpinions(NarratorTO)
    
    

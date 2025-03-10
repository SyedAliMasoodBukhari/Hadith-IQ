from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.Hadith.AbsHadithBO import AbsHadithBO
from BusinessLogicLayer.Narrator.AbsNarratorBO import AbsNarratorBO
from BusinessLogicLayer.Sanad.AbsSanadBO import AbsSanadBO
from BusinessLogicLayer.Project.AbsProjectBO import AbsProjectBO
from BusinessLogicLayer.Book.AbsBookBO import AbsBookBO
from TO.SanadTO import SanadTO
from TO.HadithTO import HadithTO
from TO.ProjectTO import ProjectTO
from TO.NarratorTO import NarratorTO
from typing import List, Dict


class BLLFascade(AbsBLLFascade):

    def __init__(
        self,
        hadithBO: AbsHadithBO,
        sanadBO: AbsSanadBO,
        projectBO: AbsProjectBO,
        narratorBO: AbsNarratorBO,
        bookBO:AbsBookBO,
    ):
        self.__hadithBO = hadithBO
        self.__narratorBO = narratorBO
        self.__projectBO = projectBO
        self.__sanadBO = sanadBO
        self.__bookBO=bookBO

    # projectBo functions

    def createProject(self, name: str) -> bool:
        return self.__projectBO.createProject(name)

    def saveProject(self) -> bool:
        return self.__projectBO.saveProject()

    def deleteProject(self, name: str) -> bool:
        return self.__projectBO.deleteProject(name)

    def renameProject(self, currName: str, newName: str) -> bool:
        return self.__projectBO.renameProject(currName, newName)

    def getProjects(self) -> List[ProjectTO]:
        return self.__projectBO.getProjects()
    
    def saveProjectState(self,name:str, stateData: List[str],query:str)->bool:
        return self.__projectBO.saveProjectState(name,stateData,query)
    
    def getProjectState(self,name:str)->List[str]:
        return  self.__projectBO.getProjectState(name)

    def getSingleProjectState(self,name:str,query:str)->List[str]:
      return self.__projectBO.getSingleProjectState(name,query)
    def removeHadithFromState(self, matn: List[str], projectName: str, stateQuery: str) -> bool:
        return self.__projectBO.removeHadithFromState(matn,projectName,stateQuery)
    
    def mergeProjectState(self, projectname: str, query_names: List[str], queryname: str) -> bool:
        return self.__projectBO.mergeProjectState(projectname,query_names,queryname)
    def renameQueryOfState(self, project_name: str, old_query_name: str, new_query_name: str) -> bool:
        return self.__projectBO.renameQueryOfState(project_name,old_query_name,new_query_name)
    def deleteState(self, project_name: str, query_name: str) -> bool:
        return self.__projectBO.deleteState(project_name,query_name)
    # AbsHadithBo Functions

    def importHadithFile(self, projectName: str, filePath: str) -> bool:
        return self.__hadithBO.importHadithFile(projectName, filePath)
    
    def importHadithFileCSV(self, filePath: str) -> bool:
        return self.__hadithBO.importHadithFileCSV(filePath)
    def getAllBooks(self):
        return self.__bookBO.getAllBooks()

    
    def getAllHadiths(self, page: int) -> dict:
        return self.__hadithBO.getAllHadiths(page)

    def semanticSearch(self, hadith: str, projectName: str, threshold: float) -> dict:
        return self.__hadithBO.semanticSearch(hadith, projectName, threshold)

    def getHadithData(self, HadithTO: HadithTO) -> Dict:
        return self.__hadithBO.getHadithData(HadithTO)
    
    def getAllHadithsOfProject(self, projectName: str,page:int) -> dict:
        return self.__hadithBO.getAllHadithsOfProject(projectName,page)

    def sortHadith(
        self, byNarrator: bool, byGrade: bool, gradeType: str, hadithList: List[str]
    ) -> List[dict]:
        return self.__hadithBO.sortHadith(byNarrator, byGrade, gradeType, hadithList)
    
    def generateHadithFile(self, path: str, HadithTO: List[HadithTO]) -> bool:
        return self.__hadithBO.generateHadithFile(path, HadithTO)

    def expandSearch(
        self, HadithTO: List[str], projectName: str, threshold: float
    ) -> dict:
        return self.__hadithBO.expandSearch(HadithTO, projectName, threshold)
    def getHadithDetails(self, matn: str) -> dict:
        return self.__hadithBO.getHadithDetails(matn)
    def searchHadithByNarrator(self, project_name: str, narrator_name: str, page: int) -> dict:
        return self.__hadithBO.searchHadithByNarrator(project_name,narrator_name,page)

    # NarratorBO Functions
    ##
    def getNarratedHadith(self, narratorTO: NarratorTO) -> List[HadithTO]:
        return self.__narratorBO.getNarratedHadith(narratorTO)

    ##
    def getNarratorTeachers(self, narratorTO: NarratorTO) -> List[NarratorTO]:
        return self.__narratorBO.getNarratorTeachers(narratorTO)

    ##
    def getNarratorStudents(self, narratorTO: NarratorTO) -> List[NarratorTO]:
        return self.__narratorBO.getNarratorStudents(narratorTO)

    ##
    def applySentimentAnalysis(self, narratorTO: NarratorTO) -> str:
        return self.__narratorBO.applySentimentAnalysis(narratorTO)

    ##
    def NarratorSearch(self, narrator: str) -> List[NarratorTO]:
        return self.__narratorBO.NarratorSearch(narrator)

    ##
    def getNarratorAuthenticity(self, narratorTO: NarratorTO) -> str:
        return self.__narratorBO.getNarratorAuthenticity(narratorTO)

    ##
    def generateNarratorFile(self, path: str, narratorTOList: List[NarratorTO]) -> bool:
        return self.__narratorBO.generateNarratorFile(path, narratorTOList)

    ##
    def getNarratorDetails(self, narratorTO: NarratorTO) -> List[NarratorTO]:
        return self.__narratorBO.getNarratorDetails(narratorTO)
    def convertHtmlToText(self,html_file: str) -> dict:
        return self.__narratorBO.convertHtmlToText(html_file)
    def filter_and_append(self, input_file, arabic_count)->dict:
        return self.__narratorBO.filter_and_append(input_file,arabic_count)

    ##
    def importNarratorOpinions(self, file: str) -> bool:
        return self.__narratorBO.importNarratorOpinions(file)
    def getAllNarratorsOfProject(self, project_name: str,page :int) -> dict:
        return self.__narratorBO.getAllNarratorsOfProject(project_name,page)
    def fetch_narrator_data(self,file_path:str,arabic_count:str)->dict:
        return self.__narratorBO.fetch_narrator_data(file_path,arabic_count)
    def getAllNarrators(self, page: int) -> dict:
        return self.__narratorBO.getAllNarrators(page)
      

    # SanadBO Functions
    def authenticateSanad(self, sanadTO: SanadTO) -> str:
        return self.__sanadBO.authenticateSanad(sanadTO)

    def insertOpinion(self, narratorTO: NarratorTO, opinion: str) -> bool:
        return self.__sanadBO.insertOpinion(narratorTO, opinion)

    def getSanad(self, matn: str) -> List[NarratorTO]:
        return self.__sanadBO.getSanad(matn)


# OpinionBo Functions
# def getOpinions(self,narratorTO:NarratorTO)->List[OpinionTO]:
#     return self.__opinionBO.getOpinions(narratorTO)

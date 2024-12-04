from BusinessLogicLayer.Fascade.AbsBLLFascade import AbsBLLFascade
from BusinessLogicLayer.Hadith.AbsHadithBO import AbsHadithBO
from BusinessLogicLayer.Narrator.AbsNarratorBO import AbsNarratorBO
from BusinessLogicLayer.Sanad.AbsSanadBO import AbsSanadBO
from BusinessLogicLayer.Project.AbsProjectBO import AbsProjectBO
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
    ):
        self.__hadithBO = hadithBO
        self.__narratorBO = narratorBO
        self.__projectBO = projectBO
        self.__sanadBO = sanadBO

    # projectBo functions

    def createProject(self, name: str) -> bool:
        return self.__projectBO.createProject(name)

    def saveProject(self) -> bool:
        return self.__projectBO.saveProject()

    def openExistingProject(self) -> bool:
        return self.__projectBO.openExistingProject()

    def renamepProject(self, currName: str, newName: str) -> bool:
        return self.__projectBO.renamepProject(currName, newName)

    def getProjects(self) -> List[ProjectTO]:
        return self.__projectBO.getProjects()

    # AbsHadithBo Functions

    #
    def importedHadithFile(self, filePath: str) -> bool:
        return self.__hadithBO.importedHadithFile(filePath)

    #
    def getAllHadith(self) -> List[HadithTO]:
        return self.__hadithBO.getAllHadith()

    #
    def semanticSearch(self, hadith: str, projectName: str) -> dict:
        return self.__hadithBO.semanticSearch(hadith, projectName)

    #
    def getHadithData(self, HadithTO: HadithTO) -> Dict:
        return self.__hadithBO.getHadithData(HadithTO)

    #
    def sortHadith(
        self, ByNarrator: bool, ByGrade: bool, GradeType: List[str]
    ) -> List[HadithTO]:
        return self.__hadithBO.sortHadith(ByNarrator, ByGrade, GradeType)

    #
    def generateHadithFile(self, path: str, HadithTO: List[HadithTO]) -> bool:
        return self.__hadithBO.generateHadithFile(path, HadithTO)

    #
    def expandSearch(self, HadithTO: List[str], projectName: str) -> dict:
        return self.__hadithBO.expandSearch(HadithTO, projectName)


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

    ##
    def importNarratorOpinions(self, file: str) -> bool:
        return self.__narratorBO.importNarratorOpinions(file)

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

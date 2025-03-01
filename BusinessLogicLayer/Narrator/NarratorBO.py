from typing import List
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from BusinessLogicLayer.Narrator.AbsNarratorBO import AbsNarratorBO
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO


class NarratorBO(AbsNarratorBO):

    def __init__(self, dalFascade: AbsDALFascade):
        self.__dalFascade = dalFascade

    @property
    def dalFascade(self) -> AbsDALFascade:
        return self.__dalFascade

    @dalFascade.setter
    def dalFascade(self, value):
        self.__dalFascade = value
    
    def getNarratedHadith(self,narratorTO:NarratorTO)->List[HadithTO]:
        return None

    
    def getNarratorTeachers(self,narratorTO:NarratorTO)->List[NarratorTO]:
        return None

    
    def getNarratorStudents(self,narratorTO:NarratorTO)->List[NarratorTO]:
        return None

    
    def applySentimentAnalysis(self,narratorTO:NarratorTO)->str:
        return None

    
    def NarratorSearch(self,narrator:str)->List[NarratorTO]:
        return None

    
    def getNarratorAuthenticity(self,narratorTO:NarratorTO)->str:
        return None

    
    def generateNarratorFile(self,path:str,narratorTOList:List[NarratorTO])->bool:
        return None

    
    def getNarratorDetails(self,narratorTO:NarratorTO)->List[NarratorTO]:
        return None

    
    def importNarratorOpinions(self,file:str)->bool:
        return None
    def getAllNarratorsOfProject(self, project_name: str,page :int) -> dict:
        return self.__dalFascade.getAllNarratorsOfProject(project_name,page)
      
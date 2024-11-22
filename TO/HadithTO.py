from typing import List
class HadithTO:
    def __init__(self,hadithID:int,matn:str,matnEmbedding: list,hadithAuthenticity: str):
        self.__hadithId = hadithID
        self.__matn = matn
        self.__matnEmbedding = matnEmbedding
        self.__hadithAuthenticity = hadithAuthenticity
    
    @property
    def hadithId(self)->int:
        return self.__hadithId
    @hadithId.setter
    def hadithId(self,value:int):
        self.__hadithId=value
    
    @property
    def matn(self)->str:
        return self.__matn
    @matn.setter
    def matn(self,value:str):
        self.__matn = value

    @property
    def matnEmbedding(self)->list:
        return self.matnEmbeddings
    @matnEmbedding.setter
    def matnEmbedding(self,value:list):
        self.__matnEmbedding = value
    
    @property
    def hadithAuthenticity(self)->str:
        return self.__hadithAuthencitiy
    @hadithAuthenticity.setter
    def hadithAuthenticity(self,value:str):
        self.__hadithAuthenticity=value
    
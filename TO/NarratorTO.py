class NarratorTO:
    def __init__(self,narratorID:int,narratorName:str,narratorAuthenticity:str):
        self.__narratorID = narratorID
        self.__narratorName = narratorName
        self.__narratorAuthenticity = narratorAuthenticity
    
    @property
    def narratorID(self)->int:
        return self.__narratorID
    @narratorID.setter
    def narratorID(self,value:int):
        self.__narratorID=value
    
    @property
    def narratorName(self)->str:
        return self.__narratorName
    @narratorName.setter
    def narratorName(self,value:str):
        self.__narratorName = value
    
    @property
    def narratorAuthenticity(self)->str:
        return self.__narratorAuthenticity
    @narratorAuthenticity.setter
    def narratorAuthenticity(self,value:str):
        self.__narratorAuthenticity = value
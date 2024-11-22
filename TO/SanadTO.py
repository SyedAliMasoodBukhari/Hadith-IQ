from NarratorTO import NarratorTO

class SanadTO:
    def __init__(self,sanadID : int,sanad : str,narratorTO:NarratorTO):
        self.__sanadID = sanadID
        self.__sanad = sanad
        self.__narratorTO = narratorTO
    
    @property
    def sanadID(self)->int:
        return self.__sanadID
    @sanadID.setter
    def sanadID(self,value:int):
        self.__sanadID = value
     
    @property
    def sanad(self)->str:
        return self.__sanad
    @sanad.setter
    def sanad(self,value:str):
        self.__sanad= value
    
    @property
    def narratorTO(self)->NarratorTO:
        return self.__narratorTO
    @sanadID.setter
    def narratorTO(self,value:NarratorTO):
        self.__narratorTO = value
    
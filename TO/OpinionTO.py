from abc import ABC

class OpinionTO:
 def __init__(self,opinionId : int, opinion : str):
    self.__opinionId = opinionId
    self.__opinion = opinion

 @property
 def opinionId(self)-> int: 
    return self.__opinionId
 @opinionId.setter
 def OpinionId(self,value:int):
    self.__opinionId = value

 @property
 def opinion(self)->str: 
    return self.__opinion
 @opinionId.setter
 def opinion(self,value:str):
    self.__opinion = value
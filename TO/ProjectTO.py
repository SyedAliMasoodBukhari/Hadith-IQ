class ProjectTO:
    def __init__(self,projectId:int,projectName:str,creationTimeStamp:str):
        self.__projectId = projectId
        self.__projectName = projectName
        self.__creationTimeStamp = creationTimeStamp
    
    @property
    def projectId(self)->int:
        return self.__projectId
    @projectId.setter
    def projectId(self,value:int):
        self.__projectId = value
    
    @property
    def projectName(self)->str:
        return self.__projectName
    @projectName.setter
    def projectName(self,value:str):
        self.__projectName = value
    
    @property
    def creationTimeStamp(self)->str:
        return self.creationTimeStamp
    @creationTimeStamp.setter
    def creationTimeStamp(self,value:str):
        self.creationTimeStamp = value
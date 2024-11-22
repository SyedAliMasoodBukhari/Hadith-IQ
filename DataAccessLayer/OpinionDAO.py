from AbsOpinionDAO import AbsOpinionDAO
from TO.NarratorTO import NarratorTO
from TO.OpinionTO import OpinionTO
from typing import List

class OpinionDAO(AbsOpinionDAO):
     
    def insertOpinion(self,NarratorTO:NarratorTO,opinion:str)->bool:
        return None
    
    
    def getOpinions(self,NarratorTO:NarratorTO)->List[OpinionTO]:
        return None
    
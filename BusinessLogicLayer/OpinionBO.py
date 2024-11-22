from AbsOpinionBO import AbsOpinionBO
from TO.OpinionTO import OpinionTO
from typing import List
from TO.NarratorTO import NarratorTO
class OpinionBO(AbsOpinionBO):
    
    def getOpinions(self,narratorTO:NarratorTO)->List[OpinionTO]:
        return None
    
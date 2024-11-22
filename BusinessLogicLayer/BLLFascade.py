from AbsBLLFascade import AbsBLLFascade
from AbsHadithBO import AbsHadithBO
from AbsNarratorBO import AbsNarratorBO
from AbsSanadBO import AbsSanadBO
class BLLFascade(AbsBLLFascade):
    def __init__(self,hadithBO:AbsHadithBO):
        self.__hadithBO=hadithBO
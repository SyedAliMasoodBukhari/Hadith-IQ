from BusinessLogicLayer.Hadith.AbsHadithBO import AbsHadithBO
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from typing import List, Dict
import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from TO.HadithTO import HadithTO
from DataAccessLayer.Fascade.DALFascade import DALFascade
from DataAccessLayer.Hadith.HadithDAO import HadithDAO
from DataAccessLayer.DbConnection import DbConnection

class HadithBO(AbsHadithBO):
    
    def __init__(self, dalFascade: AbsDALFascade):
        self.__dalFascade = dalFascade
        self.labse_model = SentenceTransformer('sentence-transformers/LaBSE')

    @property
    def dalFascade(self) -> AbsDALFascade:
        return self.__dalFascade

    @dalFascade.setter
    def dalFascade(self, value):
        self.__dalFascade = value

    def importedHadithFile(self, filePath: str) -> bool:
        return None
    
    def getAllHadith(self) -> List[HadithTO]:
        return None
    
    def semanticSearch(self, hadith: str,projectName:str) -> dict:
        query=self.cleanHadithMatn()
        queryEmbedding=self.generateEmbeddings(query)
        hadithDict=self.dalFascade.getProjectHadithsEmbedding(projectName)
        result=self.cosinesimilarity(queryEmbedding,hadithDict)
        return result



    def cosinesimilarity(self, queryEmbedding: str, hadith_embeddings: dict) -> dict:
     try:
        queryEmbedding = np.array(eval(queryEmbedding)).reshape(1, -1)  # Convert to 2D array for sklearn
        similarities = []
        for matn, embedding in hadith_embeddings.items():
            matnEmbedding = np.array(embedding).reshape(1, -1)
            similarity = cosine_similarity(queryEmbedding, matnEmbedding)[0][0]
            similarities.append({"matn": matn, "embedding": embedding, "similarity": similarity})

        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:10]

     except Exception as e:
        print(f"Error calculating cosine similarity: {e}")
        return []  
    
    def getHadithData(self, HadithTO: HadithTO) -> Dict:
        return None

    def sortHadith(self, ByNarrator: bool, ByGrade: bool, GradeType: List[str]) -> List[HadithTO]:
        return None

    def generateHadithFile(self, path: str, HadithTO: List[HadithTO]) -> bool:
        return None

    def expandSearch(self, HadithTO: List[HadithTO]) -> List[HadithTO]:
        return None

    def createAndStoreEmbeddings(self, hadithTOList: List[HadithTO]) -> bool:
        return None

    def authenticateHadith(self, hadithTO: HadithTO) -> bool:
        return None

    def cleanHadithMatn(self, matn: str) -> str:
        """Normalize the Hadith text (Matn) by removing diacritics and unwanted characters."""
        cleaned_text = re.sub(r'[إأٱآ]', 'ا', matn)  # Normalize Alif variations
        cleaned_text = re.sub(r'ة', 'ه', cleaned_text)  # Replace Taa Marbuta with Ha
        cleaned_text = re.sub(r'ى', 'ي', cleaned_text)  # Replace Alif Maqsura with Ya
        cleaned_text = re.sub(r'[،؟:.]', '', cleaned_text)  # Remove punctuation
        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove unwanted chars
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Normalize spaces
        cleaned_text = re.sub(r'(\s+)(و)\1', r' \2', cleaned_text)  # Remove extra spaces between "و"
        return cleaned_text

    def generateEmbeddings(self, matn: str) -> str:
        """
        Generates embeddings for the given text (matn) using the LaBSE model,
        converts the embedding into a JSON string, and returns it.
        """
        embedding = self.labse_model.encode([matn])[0]  # Use the instance variable `labse_model`
        # Convert the NumPy array (embedding) into a Python list (JSON serializable)
        embedding_list = embedding.tolist()
        # Convert the list into a JSON string with pretty print (indentation)
        embedding_json = json.dumps(embedding_list, indent=4, separators=(',', ': '))
        return embedding_json
    
    def insertHadith(self, HadithTO: List[HadithTO]) -> bool:
     for hadith in HadithTO:
        print(hadith.matn) 
        cleanMatn=self.cleanHadithMatn(hadith.matn)
        embedding = self.generateEmbeddings(cleanMatn) 
        hadith.cleanedMatn=cleanMatn
        hadith.matnEmbedding=embedding
     if not self.dalFascade.insertHadith(hadith):  # If insertHadith returns False
            print(f"Failed to insert Hadith: {hadith.matn}")
            return False  
     return True 


# Main Function
def main():
    # Create an instance of AbsDALFascade (replace with your actual implementation)
    db=DbConnection()
    hadithdao=HadithDAO(db)
    dalFascade = DALFascade(hadithdao) # Replace with a concrete implementation of AbsDALFascade
    # Create an instance of HadithBO
    hadith_bo = HadithBO(dalFascade)
     # Example of Hadith text (Matn)
    matn = "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ"
    hadTO = HadithTO (0,matn,"","","","")
    hadithlist=[hadTO]

    hadith_bo.insertHadith(hadithlist)

if __name__ == "__main__":
    main()
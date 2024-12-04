import ast
from BusinessLogicLayer.Hadith.AbsHadithBO import AbsHadithBO
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from typing import List, Dict
import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from TO.HadithTO import HadithTO

class HadithBO(AbsHadithBO):
    
    def __init__(self, dalFascade: AbsDALFascade):
        self.__dalFascade = dalFascade
        self.labse_model = SentenceTransformer('sentence-transformers/LaBSE')
        self.labse_model.eval()  # For PyTorch-based SentenceTransformer models


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
    
    def create_batches(self, data_dict: dict, batch_size: int) -> List[dict]:
     items = list(data_dict.items())
     return [
        dict(items[i:i + batch_size]) for i in range(0, len(items), batch_size)
     ]
    
    def expandSearch(self, hadith_list: List[str], projectName: str) -> dict:
     try:
        expanded_results = {}
        for hadith in hadith_list:
            cleaned_hadith = self._cleanHadithMatn(hadith)  # Clean the Hadith text
            queryEmbedding = self._generateEmbeddings(cleaned_hadith)  # Generate embeddings for the cleaned text
            hadithDict = self.dalFascade.getProjectHadithsEmbedding(projectName)  # Get the embeddings for the project
            
            batch_size = 100
            batched_results = []
            hadith_batches = self.create_batches(hadithDict, batch_size)  # Create batches of Hadith data
            
            for batch in hadith_batches:
                batch_result = self._cosineSimilarity(queryEmbedding, batch)  # Get cosine similarity for each batch
                batched_results.extend(batch_result)  # Collect all batch results
             
            batched_results = [result for result in batched_results if result["matn"] != hadith]
            batched_results.sort(key=lambda x: x["similarity"], reverse=True)
            top_results = batched_results[:20]
            expanded_results = [{"matn": result["matn"],"similarity": result["similarity"]} for result in top_results]

        return expanded_results

     except Exception as e:
        print(f"Error in expandSearch: {e}")
        return {}

    def semanticSearch(self, hadith: str,projectName:str) -> dict:
        query=self._cleanHadithMatn(hadith)
        queryEmbedding=self._generateEmbeddings(query)
        hadithDict=self.dalFascade.getProjectHadithsEmbedding(projectName)
        # Process the Hadith dictionary in batches
        batch_size = 100
        batched_results = []
        hadith_batches = self.create_batches(hadithDict, batch_size)
    
        for batch in hadith_batches:
           batch_result = self._cosineSimilarity(queryEmbedding, batch)
           batched_results.extend(batch_result)
        batched_results.sort(key=lambda x: x["similarity"], reverse=True)
        simplified_results = [{"matn": result["matn"], "similarity": result["similarity"]} for result in batched_results]
        return simplified_results[:10]



    def _cosineSimilarity(self, queryEmbedding: str, hadith_embeddings: dict) -> dict:
     try:
        queryEmbedding = np.array(ast.literal_eval(queryEmbedding)).reshape(1, -1)  # Convert to 2D array for sklearn
        similarities = []
        for matn, embedding in hadith_embeddings.items():
            matnEmbedding = np.array(ast.literal_eval(embedding)).reshape(1, -1)
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

    def createAndStoreEmbeddings(self, hadithTOList: List[HadithTO]) -> bool:
        return None

    def authenticateHadith(self, hadithTO: HadithTO) -> bool:
        return None

    def _cleanHadithMatn(self, matn: str) -> str:
       """Normalize the Hadith text (Matn) by removing diacritics, dashes, and unwanted characters."""
       cleaned_text = re.sub(r'[إأٱآ]', 'ا', matn)  # Normalize Alif variations
       cleaned_text = re.sub(r'ة', 'ه', cleaned_text)  # Replace Taa Marbuta with Ha
       cleaned_text = re.sub(r'ى', 'ي', cleaned_text)  # Replace Alif Maqsura with Ya
       cleaned_text = re.sub(r'[،؟:.]', '', cleaned_text)  # Remove punctuation
       cleaned_text = re.sub(r'-', '', cleaned_text)  # Remove dashes
       cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove unwanted chars
       cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Normalize spaces
       cleaned_text = re.sub(r'(\s+)(و)\1', r' \2', cleaned_text)  # Remove extra spaces between "و"
       return cleaned_text


    def _generateEmbeddings(self, matn: str) -> str:
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
        cleanMatn=self._cleanHadithMatn(hadith.matn)
        embedding = self._generateEmbeddings(cleanMatn) 
        hadith.cleanedMatn=cleanMatn
        hadith.matnEmbedding=embedding
     if not self.dalFascade.insertHadith(hadith):  # If insertHadith returns False
            print(f"Failed to insert Hadith: {hadith.matn}")
            return False  
     return True
    
from multiprocessing.shared_memory import SharedMemory
import ast
import logging
from BusinessLogicLayer.Hadith.AbsHadithBO import AbsHadithBO
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from typing import List, Dict
import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
from TO.SanadTO import SanadTO
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.utils.dediac import dediac_ar
from camel_tools.tokenizers.word import simple_word_tokenize
from multiprocessing import Pool, cpu_count
import os
from functools import partial
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Manager
import math
import pickle
import time


class HadithBO(AbsHadithBO):    
    def __init__(self, dalFascade: AbsDALFascade):
        self.__dalFascade = dalFascade
        self.labse_model = SentenceTransformer("sentence-transformers/LaBSE")
        self.labse_model.eval()  # For PyTorch-based SentenceTransformer models
        self.morphology_db = MorphologyDB.builtin_db()
        

    @property
    def dalFascade(self) -> AbsDALFascade:
        return self.__dalFascade

    @dalFascade.setter
    def dalFascade(self, value):
        self.__dalFascade = value

    def importHadithFile(self, projectName: str, filePath: str) -> bool:
        
        bookData = self.dalFascade.importBook(projectName, filePath)
        if not bookData:
          print("No book data found.")
          
          return False
    # Number of CPU cores available
        ##self.logger.info("Started Multiprocessing and multiThreading ")
        num_cores = cpu_count()
        chunk_size = math.ceil(len(bookData) / num_cores)
    
    # Helper function for threading within each process

    # Process all data in parallel
        ##self.logger.info("Created MultiProcesses")
        process_entry_decoupled = partial(
        HadithBO.process_entry,
        HadithBO._getActualMatn,
        HadithBO._clean_text,
        HadithBO._cleanHadithMatn,
        partial(HadithBO._lemmatize_arabic_sentence, morphology_db=self.morphology_db),
        partial(HadithBO._generateEmbeddings, labse_model=self.labse_model),
        )

        # Decouple process_chunk
        process_chunk_decoupled = partial(HadithBO.process_chunk, process_entry=process_entry_decoupled)

        # Process data in parallel
        processed_data = self.process_data_in_parallel(bookData, num_cores, chunk_size, process_chunk_decoupled)
        ##self.logger.info("Multiprocessing and Multithreadig in done starting Inserting")

    # Insertion Logic
        finalResult = False
        for hadith in processed_data:
         _matn = hadith["matn"]
         _matnEmbedding = hadith["matnEmbedding"]
         _bookName = hadith.get("bookname")
         _sanad = hadith.get("sanad")
         if _matn and _bookName and _sanad:
            # Insert Book record
            if self.__dalFascade.insertBook(projectName, _bookName):
                _hadithTO = HadithTO(
                    0, _matn, _matnEmbedding, "Authentic", _bookName, _matn
                )
                _hadithResult = self.__dalFascade.insertHadith(projectName, _hadithTO)
                if _hadithResult:
                    if _sanad != "No SANAD":
                        sanadTO = SanadTO(_sanad, "Authentic", _hadithTO)
                        _resultSanad = self.__dalFascade.insertSanad(
                            projectName, sanadTO
                        )

                    if _resultSanad:
                        _listNarrators = self._transformSanad(_sanad)
                        if _listNarrators:
                            finalResult = self._insertHadithNarrators(_sanad, _listNarrators)
         
         
        return finalResult
    
    def process_entry(getActualMatn, clean_text, cleanHadithMatn, lemmatize, generateEmbeddings, hadith):
        _matn = hadith.get("matn")
        _matnClean = getActualMatn(_matn)
        _matn = clean_text(_matn)
        _cleanedMatn = cleanHadithMatn(lemmatize(cleanHadithMatn(_matnClean)))
        _matnEmbedding = generateEmbeddings(_cleanedMatn)
        hadith["matn"] = _cleanedMatn
        hadith["matnEmbedding"] = _matnEmbedding
        print(hadith)
        return hadith
    
    @staticmethod
    def process_chunk(chunk, process_entry):
        num_threads = cpu_count()
        chunk_size = max(1, len(chunk) // num_threads)
        sub_chunks = [chunk[i * chunk_size:(i + 1) * chunk_size] for i in range(num_threads)]

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = list(executor.map(lambda sub_chunk: [process_entry(entry) for entry in sub_chunk], sub_chunks))

        processed_chunk = [entry for sublist in results for entry in sublist]
        return processed_chunk
      # Flatten the processed results from all threads
      #self.logger.info("Merging Results from Each Thread")
    
    
    # Function to divide data among processes
    @staticmethod
    def process_data_in_parallel(data, num_processes, chunk_size, process_chunk):
        chunks = [data[i * chunk_size:(i + 1) * chunk_size] for i in range(num_processes)]

        with Pool(processes=num_processes) as pool:
            results = pool.map(process_chunk, chunks)
        
        processed_data = [entry for chunk in results for entry in chunk]
        return processed_data
    
    def getAllHadith(self) -> List[HadithTO]:
        return None
    
    def semanticSearch(self, hadith: str, projectName: str, threshold: float) -> dict:
        _query = self._getActualMatn(hadith)
        _query=self._cleanHadithMatn(self._lemmatize_arabic_sentence(self._cleanHadithMatn(_query),self.morphology_db))
        # _query = self._cleanHadithMatn(_query)
        _queryEmbedding = self._generateEmbeddings(_query,self.labse_model)
        #Returns Dictionary of Hadith Embedding 
        _hadithDict = self.dalFascade.getProjectHadithsEmbedding(projectName)
        num_cores = cpu_count()
        # Processing the Hadith dictionary in batches
        #_test = self._createBatchestest(_hadithDict)
        #_hadith_batches = self._createBatches(_hadithDict, num_cores)

        #makes _hadith_batches available to all the process via shared memory 
        manager = Manager()
        _hadith_batches = manager.list(self._createBatches(_hadithDict, num_cores))

        cosine_similarity_fn = partial(self._cosineSimilarity, _queryEmbedding)
        process_chunk_fn = partial(self.process_chunk_similarity, cosine_similarity_fn)
        #process_batch_partial = partial(self.process_batch, process_chunk_fn, num_cores)
        process_batch_partial = partial(self.process_batch,cosine_similarity_fn)
        """
        try:
            with Pool(processes=num_cores) as pool:
                results = pool.map(process_batch_partial, _hadith_batches)
        except Exception as e:
            print(f"Error during multiprocessing: {e}")
            return []
        """
        #for batches in _hadith_batches:
        print(f"\n Hadith Batches : {[range(len(_hadith_batches))]}")
        try:
           with Pool(processes=num_cores) as pool:
            #results = pool.starmap(process_batch_partial,_hadith_batches)
            #results = pool.map(process_batch_partial,range(len(_hadith_batches)))
             results = pool.starmap(process_batch_partial, [(index, _hadith_batches) for index in range(len(_hadith_batches))])
            #results = pool.map(lambda i: process_batch_partial(_hadith_batches[i]), range(len(_hadith_batches)))
        except Exception as e:
          print(f"Error during multiprocessing: {e}")
          return []
        all_results = [item for sublist in results for item in sublist]
        all_results = [item for sublist in all_results for item in sublist]
        all_results.sort(key=lambda x: x["similarity"], reverse=True)
        _filtered_results = [
        {"matn": result["matn"], "similarity": result["similarity"]}
        for result in all_results
        if result["similarity"] >= threshold
         ]
        return _filtered_results
    

    @staticmethod
    def process_batch(cosine_similarity_fn, index, _hadith_batches): #accepting List[List[Dict]]
        # Calculate chunk sizes more robustly
        if not isinstance(index, int):  
         raise ValueError(f"got index as int {index}")
        batch_local =_hadith_batches[index]
        print(f"Going towards threading : {index}")
        print(f"Printing Batch : {batch_local}")
        results = cosine_similarity_fn(batch_local)
        results = [results]
        # Collect results from each future
        return results
    
    """
    @staticmethod
    def process_batch(process_chunk_fn, batch, num_cores): #accepting List[List[Dict]]
        # Calculate chunk sizes more robustly
        if not isinstance(batch, list):  
         raise ValueError(f"Expected batch to be a list, got {type(batch)}")

    # Handle case where batch items (chunks) might be dictionaries
        #if isinstance(batch[0], dict):  
         #batch = [batch]  # Wrap it into a list for uniform processing

    # Calculate chunk size robustly
        #chunk_size = max(1, len(batch) // num_cores)
        #chunks = [batch[i: i + chunk_size] for i in range(0, len(batch), chunk_size)]
        #chunk_size = max(1, len(batch) // num_cores)
        #chunks = [batch[i: i + chunk_size] for i in range(0, len(batch), chunk_size)]
        results = []
        print(f"Going towards threading : {os.getpid}")
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
        # Submit each chunk to the executor
         print(f"within ThreadPool")
         futures = [executor.submit(process_chunk_fn, chunk) for chunk in batch]
        
        # Collect results from each future
         for future in futures:
            # The result for each future is a List[Dict], so wrap the result into a List
            result = future.result()
            results.append(result)  # Append the List[Dict] to the results list
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(process_chunk_fn, chunk) for chunk in batch] #Passing List[Dict]
            for future in futures:
                results.extend(future.result())
        return results
    """
    """
    def process_batch(process_chunk_fn, batch, num_cores):
    # This function divides the batch into smaller chunks and processes each chunk with threads.
     results = []
     chunk_size = len(batch) // num_cores  # Divide the batch into chunks for each thread
    
    # Ensure all chunks have roughly the same size
     for i in range(num_cores):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i != num_cores - 1 else len(batch)
        
        # Create a sublist (chunk) for this thread to process
        chunk = batch[start_idx:end_idx]
        
        # Use ThreadPoolExecutor to process the chunk
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(process_chunk_fn,entry) for entry in chunk]
            
            # Gather results from threads
            for future in futures:
                results.extend(future.result())  # Flatten results from all threads
    
     return results
    """
    @staticmethod
    def process_chunk_similarity(cosine_similarity_fn, chunk):
        if not isinstance(chunk, list):
         raise ValueError(f"Expected chunk to be a list, got {type(chunk)}")
        if not all(isinstance(entry, dict) for entry in chunk):
         raise ValueError("Each item in the chunk should be a dictionary.")
    
     # Process each dictionary (entry) in the chunk and collect results
         # Convert List[Dict] to a single Dict (e.g., merge all dictionaries)
        """
        print(f"chunk:{chunk}")
        merged_dict = {k: v for d in chunk for k, v in d.items()}
        print(f"merged_dict : {merged_dict}")
        """
        results = cosine_similarity_fn(chunk)
        print(f"resultantChunk:{results}")
        results = [results]
        return results
    """
    @staticmethod
    def process_batch(cosine_similarity_fn,batch,num_cores):
            results = []
            with ThreadPoolExecutor(max_workers=num_cores) as executor:
                futures = [executor.submit(cosine_similarity_fn, [entry]) for entry in batch]
                for future in futures:
                    results.extend(future.result())
            return results
    """
            
    """
        for batch in _hadith_batches:
            _batch_result = self._cosineSimilarity(_queryEmbedding, batch)
            _batched_results.extend(_batch_result)
        _batched_results.sort(key=lambda x: x["similarity"], reverse=True)
        _threshold = threshold
        _filtered_results = [
            {"matn": result["matn"], "similarity": result["similarity"]}
            for result in _batched_results
            if result["similarity"] >= _threshold
        ]
        return _filtered_results
    """

    def getHadithData(self, HadithTO: HadithTO) -> Dict:
        return None

    def sortHadith(
        self, byNarrator: bool, byGrade: bool, gradeType: str, hadithList: List[str]
    ) -> List[dict]:
        resultant_hadith_list = []
        narrator_count = {}
        hadiths = []
        matn_pattern = r"matn:\s*(.*?),"
        similarity_pattern = r"similarity:\s*(\d+\.\d+)"
        # Loop through each string in the list
        for h in hadithList:
            hadith = {}
            # Extracting matn and similarity
            matn_match = re.search(matn_pattern, h)
            similarity_match = re.search(similarity_pattern, h)

            # Assign values to the hadith dictionary if found
            if matn_match:
                hadith["matn"] = matn_match.group(1).strip()

            if similarity_match:
                hadith["similarity"] = float(similarity_match.group(1))

            # Append the dictionary to the list
            hadiths.append(hadith)
        if byNarrator:
            for h in hadiths:
                _matn = h.get("matn", "")
                if not isinstance(_matn, str):
                    raise ValueError(
                        f"Invalid 'matn' value: expected string, got {type(_matn).__name__}"
                    )
                _similarity = h.get("similarity", None)
                if _similarity is None:
                    raise ValueError("Similarity not found in the dictionary.")
                # If similarity exists and is not a float, raise an error
                if not isinstance(_similarity, float):
                    raise ValueError(
                        f"Invalid 'similarity' value: expected float, got {type(_similarity).__name__}"
                    )
                narrator_name = self.__dalFascade.getHadithFirstNarrator(_matn)
                if not narrator_name:
                    continue

                hadith_entry = {
                    "matn": _matn,
                    "narratorName": narrator_name,
                    "similarity": _similarity,
                }
                resultant_hadith_list.append(hadith_entry)
                if narrator_name in narrator_count:
                    narrator_count[narrator_name] += 1
                else:
                    narrator_count[narrator_name] = 1
                print(resultant_hadith_list)

            resultant_hadith_list.sort(
                key=lambda x: (-narrator_count[x["narratorName"]], x["narratorName"])
            )

        return resultant_hadith_list

    def generateHadithFile(self, path: str, HadithTO: List[HadithTO]) -> bool:
        return None
    

    def expandSearch(self, hadith_list: List[str], projectName: str, threshold: float) -> List[dict]:
     try:
        # Extract hadiths as dictionaries from hadith_list
        hadiths = []
        matn_pattern = r'matn:\s*(.*?),'
        similarity_pattern = r'similarity:\s*(\d+\.\d+)'
        for h in hadith_list:
            hadith = {}
            matn_match = re.search(matn_pattern, h)
            similarity_match = re.search(similarity_pattern, h)
            if matn_match:
                hadith["matn"] = matn_match.group(1).strip()
            if similarity_match:
                hadith["similarity"] = float(similarity_match.group(1))
            hadiths.append(hadith)
        
        num_cores = cpu_count()
        # Function to process a chunk of hadiths
        _hadithDict = self.dalFascade.getProjectHadithsEmbedding(projectName)
        _hadith_batches = self._createBatches(_hadithDict,1)
        #with Manager() as manager:
            #shared_hadithDict = manager.dict(_hadithDict)  # Shared dictionary
            #shared_hadith_batches = manager.list(_hadith_batches)  # Shared list

        hadith_dict_bytes = pickle.dumps(_hadithDict)  # Serialize dictionary
        hadith_batches_bytes = pickle.dumps(_hadith_batches)  # Serialize list

        hadith_dict_shm = SharedMemory(create=True, size=len(hadith_dict_bytes))
        hadith_batches_shm = SharedMemory(create=True, size=len(hadith_batches_bytes))

        hadith_dict_shm.buf[:len(hadith_dict_bytes)] = hadith_dict_bytes
        hadith_batches_shm.buf[:len(hadith_batches_bytes)] = hadith_batches_bytes
        
        
        
        # Split hadiths into sublists for multiprocessing
        hadith_chunks = self._distributeHadithListAmongProcesses(hadiths,num_cores)

        hadithCleaning_Partials = partial(
        HadithBO._gethadithCleaning,
        HadithBO._cleanHadithMatn,
        HadithBO._getActualMatn,
        partial(HadithBO._generateEmbeddings,labse_model=self.labse_model),
        partial(HadithBO._lemmatize_arabic_sentence,morphology_db=self.morphology_db)
        )
        processExpandSearchInMultiProcessing = partial(
            HadithBO.process_ExpandSearch_chunk,
            partial(HadithBO._cosineSimilarity),
            hadithCleaning_Partials,
            #shared_hadithDict,shared_hadith_batches,
            hadith_dict_shm.name,  # Pass shared memory name instead of dict
            hadith_batches_shm.name,  # Pass shared memory name instead of list
            threshold
        )
        num_cores_handled = len(hadith_chunks)  # Use only non-empty chunks
        # Use multiprocessing to process each chunk
        with Pool(processes=num_cores_handled) as pool:
            results = pool.map(processExpandSearchInMultiProcessing, hadith_chunks)

        # Combine results from all processes
        _expanded_results = [item for sublist in results for item in sublist]

        # Remove duplicates by keeping the one with the highest similarity for each matn
        seen_mats = {}
        for result in _expanded_results:
            matn = result['matn']
            similarity = result['similarity']
            if matn not in seen_mats or seen_mats[matn].get("similarity", 0) < similarity:
             seen_mats[matn] = result
            #if matn not in seen_mats or seen_mats[matn]['similarity'] < similarity:
                #seen_mats[matn] = result

        # Collect unique results
        _expanded_results = list(seen_mats.values())

        _expanded_results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return _expanded_results

     except Exception as e:
        print(f"Error in expandSearch: {e}")
        return []
     
    def expandSearchtest(self, hadith_list: List[str], projectName: str,threshold:float) -> List[dict]:
        try:
            print(hadith_list)
            num_cores = cpu_count()
            hadiths = []
            # Regular expressions to extract matn and similarity
            matn_pattern = r'matn:\s*(.*?),'
            similarity_pattern = r'similarity:\s*(\d+\.\d+)'
            # Loop through each string in the list
            for h in hadith_list:
                hadith = {}
                # Extracting matn and similarity
                matn_match = re.search(matn_pattern, h)
                similarity_match = re.search(similarity_pattern, h)

                # Assign values to the hadith dictionary if found
                if matn_match:
                    hadith["matn"] = matn_match.group(1).strip()

                if similarity_match:
                    hadith["similarity"] = float(similarity_match.group(1))

                # Append the dictionary to the list
                hadiths.append(hadith)
                #print(hadiths)
            _expanded_results = []

            #Applying MultiProcessing and Multithreading to the below functionalities
            for hadith in hadiths:
                _matn = hadith.get("matn", "")
                if not isinstance(_matn, str):
                    raise ValueError(f"Invalid 'matn' value: expected string, got {type(_matn).__name__}")

                _cleaned_hadith = self._cleanHadithMatn(self._lemmatize_arabic_sentence(self._cleanHadithMatn(self._getActualMatn(_matn)),self.morphology_db))
                #print(_cleaned_hadith)
                _queryEmbedding = self._generateEmbeddings(_cleaned_hadith,self.labse_model)
                _hadithDict = self.dalFascade.getProjectHadithsEmbedding(projectName)

                if not _hadithDict:
                   return []
                
                _batched_results = []
                _hadith_batches = self._createBatches(_hadithDict, num_cores)

                for batch in _hadith_batches:
                    _batch_result = self._cosineSimilarity(_queryEmbedding, batch)
                    _batched_results.extend(_batch_result)

                _filtered_results = [
                    {"matn": result["matn"], "similarity": result["similarity"]}
                    for result in _batched_results if result.get("similarity", 0) >= threshold
                ]
                _filtered_results.sort(key=lambda x: x["similarity"], reverse=True)
                _top_results = _filtered_results
                print(_top_results)
                _expanded_results.extend(_top_results)

            # Remove duplicates by keeping only the one with the highest similarity for each matn
            seen_mats = {}
            for result in _expanded_results:
                matn = result['matn']
                similarity = result['similarity']

                # If matn not seen or higher similarity, update
                if matn not in seen_mats or seen_mats[matn]['similarity'] < similarity:
                    seen_mats[matn] = result

            # Collect unique results
            _expanded_results = list(seen_mats.values())

            _expanded_results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
            return _expanded_results

        except Exception as e:
            print(f"Error in expandSearch: {e}")
            return []
    

    # Private Funtions ---------------------------------------------------
    def _distributeHadithListAmongProcesses(self,hadithList,num_cores)->List[List]:
        num_chunks = min(num_cores, len(hadithList))  # Prevent creating empty lists
        chunk_size = math.ceil(len(hadithList) / num_chunks)  # Distribute elements evenly

        hadith_chunks = [
        hadithList[i * chunk_size : (i + 1) * chunk_size] for i in range(num_chunks)
        ]
        return hadith_chunks
        
    @staticmethod
    def _gethadithCleaning(_cleanHadithMatn,_getActualMatn,_generateEmbeddings,_lemmatize_arabic_sentence,_matn)->dict:
         #needed all the given functions partials
                _cleaned_hadith = _cleanHadithMatn(
                    _lemmatize_arabic_sentence(
                        _cleanHadithMatn(_getActualMatn(_matn)),
                    )
                )
                #needed _generateEmbeddings Partials
                _queryEmbedding = _generateEmbeddings(_cleaned_hadith)
                return {"matn": _cleaned_hadith, "queryEmbedding": _queryEmbedding}

    @staticmethod
    def process_ExpandSearch_chunk(_cosineSimilarity,_gethadithCleaning,_hadithDictname,_hadith_batchesname,threshold,chunk):
        try:
            _expanded_results = []
             # Open shared memory
            hadith_dict_shm = SharedMemory(name=_hadithDictname)
            hadith_batches_shm = SharedMemory(name=_hadith_batchesname)

    # Deserialize data
            _hadithDict = pickle.loads(hadith_dict_shm.buf)
            _hadith_batches = pickle.loads(hadith_batches_shm.buf)
            #print(f"\n hadithBatch : {_hadith_batches}")
            for hadith in chunk:
                _matn = hadith.get("matn", "")
                if not isinstance(_matn, str):
                    raise ValueError(f"Invalid 'matn' value: expected string, got {type(_matn).__name__}")
                
                #Needed to call this function
                cleaned_hadith_dict =_gethadithCleaning(hadith.get("matn", ""))
                _queryEmbedding = cleaned_hadith_dict.get("queryEmbedding")
                _matn=cleaned_hadith_dict.get("matn")
                #print(f"Value of Cleaned_hadith_dict : {_matn} {_queryEmbedding}")
                #still needed to extract value from cleaned_hadith_dict into 2 variables {matn:queryEmbeddings}

                #needed _hadithDict
                if not _hadithDict:
                    continue

                _batched_results = []

                #_hadithBatches and partial of cosineSimilarity
                for batch in _hadith_batches:
                    _batch_result = _cosineSimilarity(_queryEmbedding, batch)
                    _batched_results.extend(_batch_result)
                
                #needed Threshold
                _filtered_results = [
                    {"matn": result["matn"], "similarity": result["similarity"]}
                    for result in _batched_results if result.get("similarity", 0) >= threshold
                ]
                _filtered_results.sort(key=lambda x: x["similarity"], reverse=True)
                _expanded_results.extend(_filtered_results)
            print(f"\n Subprocess makes this result in expanded search : {_expanded_results}")
            return _expanded_results
        except Exception as e:
            print(f"Error during processing chunk in MultiProcessing : {e} ")
    

    @staticmethod
    def _createBatchestest(data_dict: dict, batch_size: int) -> List[List[dict]]:
     items = list(data_dict.items())
    
    # Step 1: Convert dictionary items into List[Dict]
     dict_list = [dict([item]) for item in items]  # Each key-value pair as a separate dict
    
    # Step 2: Split dict_list into List[List[Dict]] based on batch_size
     result = [dict_list[i: i + batch_size] for i in range(0, len(dict_list), batch_size)]
    
     return result

    @staticmethod
    def _createBatches(data_dict: dict, num_batches: int) -> List[List[dict]]:
     items = list(data_dict.items())
     total_items = len(items)
    
     if num_batches <= 0:
        raise ValueError("num_batches must be greater than zero.")
    
     batch_size = total_items // num_batches
     remainder = total_items % num_batches

     batches = []
     start_index = 0
     """
     for i in range(num_batches):
        # Calculate the end index for the batch
        end_index = start_index + batch_size + (1 if i < remainder else 0)
        sublist = dict(items[start_index:end_index])  # List of dicts
        
        # Now divide the sublist into num_cores parts
        sublist_items = list(sublist.items())  # Convert the sublist into a list of items
        chunk_size = len(sublist_items) // num_batches
        remainder = len(sublist_items) % num_batches
        
        sub_batches = []
        sub_start = 0
        
        for j in range(num_batches):
            # Calculate the end index for each chunk (adding 1 if there's a remainder)
            sub_end = sub_start + chunk_size + (1 if j < remainder else 0)
            sub_chunk = dict(sublist_items[sub_start:sub_end])  # List of dicts in each chunk
            sub_batches.append(sub_chunk)
            sub_start = sub_end
        
        batches.append(sub_batches)  # Add the sub_batches to the final batches
        start_index = end_index  # Update the start_index for the next batch
     """
     
     for i in range(num_batches):
        end_index = start_index + batch_size + (1 if i < remainder else 0)
        sublist = dict(items[start_index:end_index])  # List of dicts
        batches.append(sublist)
        start_index = end_index
    

     print(f"Created {len(batches)} batches: {batches}")
     return batches

    """
    def _createBatches(self, data_dict: dict, num_batches: int) -> List[List[dict]]:
     items = list(data_dict.items())
     total_items = len(items)
    
     if num_batches <= 0:  # Prevent division by zero
        raise ValueError("num_batches must be greater than zero.")
    
     batch_size = total_items // num_batches
     remainder = total_items % num_batches

     batches = []
     start_index = 0

     for i in range(num_batches):
        # Calculate the end index, accounting for remainder distribution
        end_index = start_index + batch_size + (1 if i < remainder else 0)

        # Instead of creating one-item dictionaries, just append a list of dicts
        sublist = [dict(items[start_index:end_index])]  # Convert key-value pairs into a dict
        
        batches.append(sublist)
        start_index = end_index

     return batches
    """
    """
    def _createBatches(self, data_dict: dict, num_batches: int) -> List[dict]:
    
     items = list(data_dict.items())
     total_items = len(items)
     batch_size = total_items // num_batches
     remainder = total_items % num_batches

     batches = []
     start_index = 0

     for i in range(num_batches):
        # Calculate the end index, accounting for the remainder
        end_index = start_index + batch_size + (1 if i < remainder else 0)
        batches.append(dict(items[start_index:end_index]))
        start_index = end_index

     return batches
    """
    """
    def _createBatchestest(self,data_dict: dict,batch_size:int) -> List[dict]:
        items = list(data_dict.items())
        result = [
            dict(items[i : i + batch_size]) for i in range(0, len(items), batch_size)
        ]
        return result
    """
    
    """
    def _createBatches(self, data_dict: dict, num_batches: int) -> List[List[dict]]:
    
     items = list(data_dict.items())
     total_items = len(items)
     batch_size = total_items // num_batches
     remainder = total_items % num_batches

     batches = []
     start_index = 0

     for i in range(num_batches):
        # Calculate the end index, accounting for the remainder
        end_index = start_index + batch_size + (1 if i < remainder else 0)
        sublist = [dict([item]) for item in items[start_index:end_index]]
        batches.append(sublist)
        start_index = end_index

     return batches
    """
    
    @staticmethod
    def _cleanHadithMatn(matn: str) -> str:
        cleaned_text = re.sub(r"[إأٱآ]", "ا", matn)  # Normalize Alif variations
        cleaned_text = re.sub(r"ة", "ه", cleaned_text)  # Replace Taa Marbuta with Ha
        cleaned_text = re.sub(r"ى", "ي", cleaned_text)  # Replace Alif Maqsura with Ya
        cleaned_text = re.sub(r"[،؟:.]", "", cleaned_text)  # Remove punctuation
        cleaned_text = re.sub(
            r"[\u0617-\u061A\u064B-\u0652\u0670]", "", cleaned_text
        )  # Remove diacritics
        cleaned_text = re.sub(r"-", "", cleaned_text)  # Remove dashes
        cleaned_text = re.sub(r"\d+", "", cleaned_text)  # Remove numbers
        cleaned_text = re.sub(r"[^\w\s]", "", cleaned_text)  # Remove unwanted chars
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()  # Normalize spaces
        cleaned_text = re.sub(
            r"(\s+)(و)\1", r" \2", cleaned_text
        )  # Remove extra spaces between "و"
        # List of phrases to remove
        phrases_to_remove = [
            r"قَالَ رَسُولُ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ",
            r"عَنِ النَّبِيِّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ",
            r"صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ",
            r"عَنِ رَسُولِ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ",
        ]
        # Remove each phrase from the cleaned text
        for phrase in phrases_to_remove:
            cleaned_text = re.sub(phrase, "", cleaned_text).strip()

        return cleaned_text
    
    
    @staticmethod
    def _cosineSimilarity(queryEmbedding: str, hadith_embeddings: dict) -> dict:
        try:
            queryEmbedding = np.array(ast.literal_eval(queryEmbedding)).reshape(
                1, -1
            )  # Convert to 2D array for sklearn
            similarities = []
            for matn, embedding in hadith_embeddings.items():
                matnEmbedding = np.array(ast.literal_eval(embedding)).reshape(1, -1)
                similarity = cosine_similarity(queryEmbedding, matnEmbedding)[0][0]
                similarities.append(
                    {"matn": matn, "embedding": embedding, "similarity": similarity}
                )

            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            return similarities[:10]

        except Exception as e:
            print(f"Error calculating cosine similarity: {e}")
            return []
    
    
    @staticmethod
    def _lemmatize_arabic_sentence(sentence: str, morphology_db: MorphologyDB) -> str:
        try:
            analyzer = Analyzer(morphology_db)
            cleaned_sentence = dediac_ar(sentence)
            words = simple_word_tokenize(cleaned_sentence)
            lemmatized_words = []

            for word in words:
                try:
                    analyses = analyzer.analyze(word)
                    if analyses:
                        lemmatized_words.append(analyses[0].get("lex", word))
                    else:
                        lemmatized_words.append(word)
                except Exception:
                    lemmatized_words.append(word)

            lemmatized_sentence = " ".join(lemmatized_words)
            return lemmatized_sentence
        except Exception as e:
            print(f"Error in lemmatizing sentence: {e}")
            return sentence
        
    @staticmethod
    def _generateEmbeddings(matn: str,labse_model) -> str:
        embedding = labse_model.encode([matn])[
            0
        ]  # Use the instance variable `labse_model`
        # Convert the NumPy array (embedding) into a Python list (JSON serializable)
        embedding_list = embedding.tolist()
        # Convert the list into a JSON string with pretty print (indentation)
        embedding_json = json.dumps(embedding_list, indent=4, separators=(",", ": "))
        return embedding_json

    def _generateEmbeddingsBatch(self, matn_list: List[str]) -> List[str]:
        try:
            # Generate embeddings for the entire batch
            embeddings = self.labse_model.encode(
                matn_list, batch_size=32
            )  # Adjust batch_size based on hardware
            # Convert each NumPy embedding array to JSON-serializable string
            embedding_json_list = [
                json.dumps(embedding.tolist(), indent=4, separators=(",", ": "))
                for embedding in embeddings
            ]
            return embedding_json_list
        except Exception as e:
            print(f"Error generating embeddings for batch: {e}")
            return []

    def _transformSanad(self, sanad: str) -> List[NarratorTO]:
        try:
            if sanad == "No SANAD":
                return []
            cleanedSanad = re.sub(r"</?IDF>", "", sanad)
            tokens = cleanedSanad.strip("[]").replace("'", "").split(",")

            narrators = []
            level = 0
            for token in tokens:
                level += 1
                narrator_name = token.strip()

                if narrator_name:
                    narrator = NarratorTO(0, narrator_name, level)
                    narrators.append(narrator)
            return narrators
        except Exception as e:
            print("Error transforming sanad:", e)
            return []

    def _insertHadithNarrators(self, sanad: str, narrators: List[NarratorTO]) -> bool:
        for narrator in narrators:
            success = self.dalFascade.insertNarrator(sanad, narrator)

            if not success:
                print(f"Failed to insert narrator: {narrator.narratorName}")
                return False

        print("All narrators inserted successfully.")
        return True
    
    @staticmethod
    def _clean_text(input_str: str) -> str:
        chars_to_remove = [",", "،", ".", '"', "“", "”"]
        for char in chars_to_remove:
            input_str = input_str.replace(char, "")
        input_str = " ".join(input_str.split())
        return input_str
    
    @staticmethod
    def _getActualMatn(input_str: str) -> str:
        # Regular expression to match text within quotation marks
        match = re.search(r'["“](.*?)["”]', input_str)
        if match:
            result = match.group(1).strip()  # Extract text inside quotation marks
        elif ":" in input_str:
            # Get text after the first colon
            result = input_str.split(":", 1)[-1].strip()
        else:
            # Return the original string if no colon or quotation marks are found
            result = input_str

        return result
        


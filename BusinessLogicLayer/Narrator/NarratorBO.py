from typing import List
from DataAccessLayer.Fascade.AbsDALFascade import AbsDALFascade
from BusinessLogicLayer.Narrator.AbsNarratorBO import AbsNarratorBO
from TO.HadithTO import HadithTO
from TO.NarratorTO import NarratorTO
import re
import os
import html2text
import requests
import configparser
import json
import re



class NarratorBO(AbsNarratorBO):
    

    def __init__(self, dalFascade: AbsDALFascade):
        self.__dalFascade = dalFascade
        config = configparser.ConfigParser()
        config.read("config.properties")
        self.API_URL = config.get("API", "API_URL")
        self.API_KEY = config.get("API", "API_KEY")
        self.DIACRITICS_PATTERN = re.compile(r"[\u064B-\u065F\u0617-\u061A]")

    @property
    def dalFascade(self) -> AbsDALFascade:
        return self.__dalFascade

    @dalFascade.setter
    def dalFascade(self, value):
        self.__dalFascade = value
    
    def getNarratedHadith(self,narratorTO:NarratorTO)->List[HadithTO]:
        return None

    
    def getNarratorTeachers(self,narratorTO:NarratorTO)->List[NarratorTO]:
        return None

    
    def getNarratorStudents(self,narratorTO:NarratorTO)->List[NarratorTO]:
        return None

    
    def applySentimentAnalysis(self,narratorTO:NarratorTO)->str:
        return None

    
    def NarratorSearch(self,narrator:str)->List[NarratorTO]:
        return None

    
    def getNarratorAuthenticity(self,narratorTO:NarratorTO)->str:
        return None

    
    def generateNarratorFile(self,path:str,narratorTOList:List[NarratorTO])->bool:
        return None

    
    def getNarratorDetails(self,narratorTO:NarratorTO)->List[NarratorTO]:
        return None

    
    def importNarratorOpinions(self,file:str)->bool:
        return None
    def getAllNarratorsOfProject(self, project_name: str,page :int) -> dict:
        return self.__dalFascade.getAllNarratorsOfProject(project_name,page)
    def convertHtmlToText(self, html_file: str) -> dict:
        try:
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            text = text_maker.handle(html_content)
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            base_filename = os.path.splitext(os.path.basename(html_file))[0]  
            save_path = os.path.join(downloads_folder, f"{base_filename}.txt")
            count = 1
            while os.path.exists(save_path):
                save_path = os.path.join(downloads_folder, f"{base_filename}_{count}.txt")
                count += 1
            with open(save_path, 'w', encoding='utf-8') as output_file:
                output_file.write(text)

            print(f"File saved at: {save_path}")
            return {"success": True, "filePath": save_path}
        except Exception as e:
            print(f"Error converting HTML to text: {e}")
            return False  

    def remove_diacritics(self, text):
        """Remove diacritics (Tashkeel) from Arabic text."""
        return self.DIACRITICS_PATTERN.sub("", text)
    
    def arabic_to_int(self, arabic_num):
        """Convert Arabic numerals to an integer."""
        arabic_digits = "٠١٢٣٤٥٦٧٨٩"
        return int("".join(str(arabic_digits.index(digit)) for digit in arabic_num))

    def int_to_arabic(self, number):
        """Convert an integer to Arabic numerals."""
        arabic_digits = "٠١٢٣٤٥٦٧٨٩"
        return "".join(arabic_digits[int(digit)] for digit in str(number))

    def increment_arabic_number(self, arabic_num):
        num = self.arabic_to_int(arabic_num)
        num += 1
        return self.int_to_arabic(num)

    def filter_and_append(self, input_file, arabic_count)->dict:
        jildNum = 0
        jildOneStart = False
        c = 0
        skipping = False
        bookStart = False
        nameCategory = []

        # Get Downloads directory
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Extract input filename without extension
        base_filename = os.path.splitext(os.path.basename(input_file))[0]
        output_filename = f"{base_filename}_structured.txt"
        output_path = os.path.join(downloads_dir, output_filename)

        # Ensure unique filename
        counter = 1
        while os.path.exists(output_path):
            output_filename = f"{base_filename}_structured_{counter}.txt"
            output_path = os.path.join(downloads_dir, output_filename)
            counter += 1

        with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_path, 'a', encoding='utf-8') as outfile:
            for line in infile:
                cleanLine = self.remove_diacritics(line)

                if 'تهذيب الكمال في أسماء الرجال' in line and not bookStart:
                    for _ in range(2):
                        for _ in range(2):
                            line = next(infile, None)
                        if 'القسم:' in line:
                            skipping = True
                            bookStart = True
                            print("Start of Jild")
                            continue

                if 'تهذيب الكمال في أسماء الرجال - جـ 1' in line and bookStart and not jildOneStart:
                    match = re.search(r"جـ (\d+)", line)
                    jildNum = int(match.group(1)) if match else 0
                    for _ in range(4):
                        line = next(infile, None)
                    if '‌باب الألف' in line:
                        jildOneStart = True
                        skipping = False
                        continue

                if '* * *' in line and bookStart:
                    skipping = True
                    continue

                if 'تهذيب الكمال في أسماء الرجال - جـ 1' in line and jildOneStart:
                    for _ in range(2):
                        line = next(infile, None)
                    if '* * *' in line:
                        skipping = False
                        continue
                elif 'تهذيب الكمال في أسماء الرجال - جـ' in line and jildNum != 1:
                    for _ in range(2):
                        line = next(infile, None)
                    if '* * *' in line:
                        skipping = False
                        continue

                if not skipping and (bool(re.search(r'\bمن اسمه\b', cleanLine)) or bool(re.search(r'\bمن اسمه\b', line))):
                    line = line.replace('من اسمه', "").strip().replace("\u200c", "")
                    nameCategory.append(line.strip())
                    outfile.write(f'\n+++++==================== من اسمه {nameCategory[-1]} ====================+++++\n')
                    continue

                if not skipping:
                    if line:
                        if jildNum == 1 and (arabic_count + "-") in line:
                            outfile.write(f'++-------------------- {arabic_count} --------------------++\n')
                            arabic_count = self.increment_arabic_number(arabic_count)
                            c += 1
                        elif jildNum != 1 and arabic_count in line:
                            outfile.write(f'++-------------------- {arabic_count} --------------------++\n')
                            arabic_count = self.increment_arabic_number(arabic_count)
                        outfile.write(line.strip() + '\n')

            print(jildNum, nameCategory, len(nameCategory))
        return {"success": True, "filePath": output_path}
    
    

    def extract_json(self,response_text):
        
        # Find JSON content using regex
        match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
        
        if match:
            json_content = match.group(1)  # Extract JSON part
            try:
                return json.loads(json_content)  # Convert to dictionary
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
                return None
        else:
            print("No valid JSON found in response.")
            return None
    
    def extract_section(self,file_path, arabic_count)->str:
        try:
            # Open and read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Convert the Arabic count to Arabic numerals
            arabic_count_str = self.int_to_arabic(arabic_count)
            next_arabic_count_str = self.increment_arabic_number(arabic_count_str)

            # Define the start and end markers based on the Arabic count
            start_marker = f"++-------------------- {arabic_count_str} --------------------++"
            end_marker = f"++-------------------- {next_arabic_count_str} --------------------++"

            # Find the start and end positions
            start_index = content.find(start_marker)
            end_index = content.find(end_marker)

            # If the start or end marker is not found, return an appropriate message
            if start_index == -1:
                return f"Start marker '{start_marker}' not found."
            if end_index == -1:
                return f"End marker '{end_marker}' not found."

            # Extract the section between the markers
            section = content[start_index:end_index].strip()

            return section

        except FileNotFoundError:
            return f"File '{file_path}' not found."
        except Exception as e:
            return f"An error occurred: {e}"
    
    def fetch_narrator_datasssss(self,file_path:str,arabic_count:str)->dict:
        # Define headers for the API request
        input_text=self.extract_section(file_path,arabic_count)
        headers = {"Authorization": f"Bearer {self.API_KEY}", "Content-Type": "application/json"}
        prompt = f'''
        create json string of 'learned from' and 'learned to' from the following text.
        Narrator Name (the main subject of the entry)
        Learned From ("\u0631\u064E\u0648\u064E\u0649 \u0639\u064E\u0646") or ("رَوَى عَن") or ("عَن")
        Learned To ("\u0631\u064E\u0648\u064E\u0649 \u0639\u064E\u0646\u0647") or ("رَوَى عَنه") or ("عَنه")
        Here is the input text:
        {input_text}
        '''
        
        # Defining request payload
        data = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [{"role": "user", "content": prompt}],
        }
        
        response = requests.post(self.API_URL, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            answer = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            text=self.extract_json(answer)
            return text
        else:
            return f"Failed to fetch data from API. Status Code: {response.status_code}"
   

    def fetch_narrator_data(self, file_path: str, arabic_count: str) -> dict:
        # Extract the relevant section from the file
        input_text = self.extract_section(file_path, arabic_count)
        
        # Define headers for the API request
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }
        
        # First prompt: Extract 'learned from' and 'learned to'
        prompt_1 = f'''
        Create a JSON structure with 'narrator_name', 'learned_from' and 'learned_to' from the following text:
        - Narrator Name (the main subject of the entry)
        - Learned From: ("\u0631\u064E\u0648\u064E\u0649 \u0639\u064E\u0646") or ("رَوَى عَن") or ("عَن")
        - Learned To: ("\u0631\u064E\u0648\u064E\u0649 \u0639\u064E\u0646\u0647") or ("رَوَى عَنه") or ("عَنه")
        
        Here is the input text:
        {input_text}
        '''
        
        # First API call
        data_1 = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [{"role": "user", "content": prompt_1}],
        }
        
        response_1 = requests.post(self.API_URL, json=data_1, headers=headers)
        
        if response_1.status_code == 200:
            response_data_1 = response_1.json()
            answer_1 = response_data_1.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            
            # Extract structured JSON from response
            structured_data_1 = self.extract_json(answer_1)
            
            # Second prompt: Extract scholars' opinions about the narrator
            prompt_2 = f'''
            Create a JSON structure of all scholarly opinions about the narrator from the following text.
            The JSON should contain:
            - "narrator_name"
            - "opinions": List of objects with:
            - "scholar_name" (the scholar giving the opinion)
            - "opinion" (the scholar's opinion about the narrator)
            
            Here is the input text:
            {input_text}
            '''
            
            # Second API call
            data_2 = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": prompt_2}],
            }
            
            response_2 = requests.post(self.API_URL, json=data_2, headers=headers)
            
            if response_2.status_code == 200:
                response_data_2 = response_2.json()
                answer_2 = response_data_2.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                
                # Extract structured JSON from response
                structured_data_2 = self.extract_json(answer_2)
                
                # Combine both responses into one dictionary
                final_response = {
                    "response_1": structured_data_1,
                    "response_2": structured_data_2
                }
                
                return final_response
            else:
                return f"Failed to fetch scholars' opinions. Status Code: {response_2.status_code}"
        
        else:
            return f"Failed to fetch data from API. Status Code: {response_1.status_code}"
    
    def getAllNarrators(self, page: int) -> dict:
        return self.__dalFascade.getAllNarrators(page)


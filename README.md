# 📚 Hadith IQ

Hadith IQ is an intelligent platform designed for Islamic researchers and scholars to semantically search, classify, and analyze Hadith data using NLP/ML techniques. This system aims to provide authenticated Hadith retrieval, narrator reliability evaluation, and detailed isnad analysis with a user-friendly interface.


## 🧠 Features

- 🔍 **Semantic Search,Root Based Search and Keyword Based Search** for Hadith using advanced NLP
- 🧵 **Isnad Analysis And Visulaisation**
- 🧑‍🏫 **Narrator Sentiment Evaluation**
- 🛡️ **Managing Project State** 
- 📁 **Paginated Hadith Dataset Display**
- 🔄 **Import & Export** of Hadith and Narrator data with structured formatting, cleaning, and preprocessing



## ⚙️ Tech Stack

| Layer        | Technology                                        |
|--------------|---------------------------------------------------|
| Frontend     | Flutter Web/Desktop                               |
| Backend      | Python (FastAPI)                                  |
| Database     | PostgreSQL                                        |
| NLP/ML       | HuggingFace Transformers,ISRIStemmer, Camel Tools |
| ORM          | SQLAlchemy                                        |



## 🚀 Getting Started

### 📂 Clone the Repository

```bash
git clone https://github.com/SyedAliMasoodBukhari/Hadith-IQ.git
```

### 🔧 Backend Setup (Python)

> Add your config.properties with following details
```bash
        [database]
        DB_URL = yoururl
        DB_PORT = yourport
        DB_USER = dbuser
        DB_PASSWORD = dbpassword
        DATABASE = yourdn
        [API]
        API_KEY = yourAPIKey
        API_URL = yourAPIUrl
```
> Run your backend

```bash
cd FYP/FYP
uvicorn BusinessLogicLayer.server:app --host 127.0.0.1 --port 8000 --workers 4
```


### 💻 Frontend Setup (React or Flutter Web/Desktop)

```bash
cd hadith_iq/hadith_iq
flutter clean
flutter upgrade
flutter pub get
flutter run -d chrome
```

## 🖼️ Screenshots

> Folowing are the screen shots of the Application
### 📚 Main Page
![Main Page Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/e7d0720d8b4e0dac453c0035015b1b78c71c9d3b/Screenshots/hadith_iq%20(1).png)

### 🔍 Search Hadiths and Hadith Details Page

![Search Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/ceb8c08599a2ed609208b2103e007a4a59a0ecd0/Screenshots/hadith_iq%20(11).png)

![Search Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/ceb8c08599a2ed609208b2103e007a4a59a0ecd0/Screenshots/hadith_iq%20(12).png)

![Search Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/ceb8c08599a2ed609208b2103e007a4a59a0ecd0/Screenshots/hadith_iq%20(13).png)

![Search Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/ceb8c08599a2ed609208b2103e007a4a59a0ecd0/Screenshots/hadith_iq%20(16).png)


### 👤 Narrators and Narrator Details Page 

![Narrators Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq(19).png)

![Narrators Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/ceb8c08599a2ed609208b2103e007a4a59a0ecd0/Screenshots/hadith_iq%20(18).png)

![Narrators Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(3).png)


### 🔄 Import/Export Interface

![IE Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(7).png)

![IE Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(8).png)

![IE Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(9).png)

![IE Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(10).png)


### 🧩 Project Management

![IE Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(6).png)

### 📈 Project State Managenment

![IE Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(14).png)

![IE Screeshot](https://github.com/SyedAliMasoodBukhari/Hadith-IQ/blob/a02d576b603f94f5f244d61fe71fa06e6692c20b/Screenshots/hadith_iq%20(15).png)


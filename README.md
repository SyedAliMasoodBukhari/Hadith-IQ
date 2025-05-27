# 📚 Hadith IQ

Hadith IQ is an intelligent platform designed for Islamic researchers and scholars to semantically search, classify, and analyze Hadith data using NLP/ML techniques. This system aims to provide authenticated Hadith retrieval, narrator reliability evaluation, and detailed isnad analysis with a user-friendly interface.


## 🧠 Features

- 🔍 **Semantic Search,Root Based Search and Keyword Based Search** for Hadith using advanced NLP
- 🧵 **Isnad Analysis And Visulaisation**
- 🧑‍🏫 **Narrator Sentiment Evaluation**
- 🛡️ **Managing Project State** 
- 📁 **Paginated Hadith Dataset Display**


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
        [database]
        DB_URL = yoururl
        DB_PORT = yourport
        DB_USER = dbuser
        DB_PASSWORD = dbpassword
        DATABASE = yourdn
        [API]
        API_KEY = yourAPIKey
        API_URL = yourAPIUrl
> Run your backend

```bash
cd FYP/FYP
uvicorn BusinessLogicLayer.server:app --host 127.0.0.1 --port 8000 --reload
```


### 💻 Frontend Setup (React or Flutter Web/Desktop)

```bash
cd hadith_iq
flutter clean
flutter upgrade
flutter pub get
flutter run -d chrome
```

import mysql.connector
from mysql.connector import Error
from threading import Lock
import configparser
import os

class DbConnection:
    __instance = None
    __lock = Lock()  # for thread-safe singleton initialization

    def __new__(cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super(DbConnection, cls).__new__(cls)
                cls.__instance.__initialize()
            return cls.__instance

    def __initialize(self):
        self.__DB_URL = None
        self.__dbConnection = None
        self.__DB_USER = None
        self.__DB_PASSWORD = None
        self.__DATABASE = None
        self.__loadConfig()

    def __loadConfig(self):
        config = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(__file__), '..','config.properties')
        config.read(config_file_path)

        if 'database' in config:
            self.__DB_URL = config['database'].get('DB_URL')
            self.__DB_USER = config['database'].get('DB_USER')
            self.__DB_PASSWORD = config['database'].get('DB_PASSWORD')
            self.__DATABASE = config['database'].get('DATABASE')

    def getConnection(self):
        if self.__dbConnection is None:
            try:
                self.__dbConnection = mysql.connector.connect(
                    host=self.__DB_URL,
                    user=self.__DB_USER,
                    password=self.__DB_PASSWORD,
                    database=self.__DATABASE
                )
                if self.__dbConnection.is_connected():
                    print("Connected to the database")
            except Error as e:
                print(f"Failed to connect to database: {e}")
                self.__dbConnection = None
        return self.__dbConnection


"""import mysql.connector
from mysql.connector import Error
import configparser
import os

# Global variable to hold the database connection
__dbConnection = None

def __loadConfig():
    #Load database configuration from the config.properties file.
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.properties')
    config.read(config_file_path)

    if 'database' in config:
        db_config = {
            "host": config['database'].get('DB_URL'),
            "user": config['database'].get('DB_USER'),
            "password": config['database'].get('DB_PASSWORD'),
            "database": config['database'].get('DATABASE')
        }
        return db_config
    else:
        raise FileNotFoundError("Database configuration not found in config.properties.")

def getConnection():
    #Get or create a database connection.
    global __dbConnection
    if __dbConnection is None:
        try:
            db_config = __loadConfig()
            __dbConnection = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"]
            )
            if __dbConnection.is_connected():
                print("Connected to the database")
        except Error as e:
            print(f"Failed to connect to database: {e}")
            __dbConnection = None
    return __dbConnection

def closeConnection():
    #Close the database connection if it exists.
    global __dbConnection
    if __dbConnection and __dbConnection.is_connected():
        __dbConnection.close()
        print("Database connection closed")
        __dbConnection = None
"""
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
        config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.properties')
        if not os.path.exists(config_file_path):
            raise FileNotFoundError("Configuration file 'config.properties' not found.")
        
        config.read(config_file_path)

        if 'database' in config:
            self.__DB_URL = config['database'].get('DB_URL')
            self.__DB_USER = config['database'].get('DB_USER')
            self.__DB_PASSWORD =""
            self.__DATABASE = config['database'].get('DATABASE')
           

    def getConnection(self):
        with self.__lock:
            if self.__dbConnection is None or not self.__dbConnection.is_connected():
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

    def closeConnection(self):
        if self.__dbConnection and self.__dbConnection.is_connected():
            self.__dbConnection.close()
            print("Database connection closed")
            self.__dbConnection = None

    def getCursor(self):
        conn = self.getConnection()
        if conn:
            return conn.cursor()
        else:
            raise ConnectionError("Database connection is not established.")

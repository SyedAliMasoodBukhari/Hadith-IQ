from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import mysql.connector
from mysql.connector import Error
from threading import Lock
import configparser
import os


class DbConnectionModel:
    __instance = None
    __lock = Lock()  # for thread-safe singleton initialization

    def __new__(cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super(DbConnectionModel, cls).__new__(cls)
                cls.__instance.__initialize()
            return cls.__instance

    def __initialize(self):
        self.__DB_URL = None
        self.__DB_USER = None
        self.__DB_PASSWORD = None
        self.__DATABASE = None
        self.__engine = None
        self.__SessionFactory = None
        self.__dbConnection = None
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
            self.__DB_PASSWORD = config['database'].get('DB_PASSWORD')
            self.__DATABASE = config['database'].get('DATABASE')

        if not all([self.__DB_URL, self.__DB_USER, self.__DATABASE]):
            raise ValueError("Database configuration is incomplete in 'config.properties'.")

        # SQLAlchemy connection string
        connection_string = f"mysql+mysqlconnector://{self.__DB_USER}:{self.__DB_PASSWORD}@{self.__DB_URL}/{self.__DATABASE}"
        
        # Create SQLAlchemy engine and session factory
        self.__engine = create_engine(connection_string, pool_pre_ping=True)
        self.__SessionFactory = scoped_session(sessionmaker(bind=self.__engine))

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

    def getConnectionUrl(self):
        return self.__DB_URL

    def getCursor(self):
        conn = self.getConnection()
        if conn:
            return conn.cursor()
        else:
            raise ConnectionError("Database connection is not established.")

    def getSession(self):
        if not self.__SessionFactory:
            raise ConnectionError("Session factory is not initialized. Check your database configuration.")
        return self.__SessionFactory()

    def closeSession(self):
        self.__SessionFactory.remove()

    def getEngine(self):
        if not self.__engine:
            raise ConnectionError("Engine is not initialized. Check your database configuration.")
        return self.__engine

    def closeEngine(self):
        if self.__engine:
            self.__engine.dispose()
            print("Database engine disposed.")

    def testConnection(self):
        try:
            with self.__engine.connect() as connection:
                connection.execute("SELECT 1")
                print("Database connection test successful.")
        except Exception as e:
            print(f"Failed to test database connection: {e}")
            raise
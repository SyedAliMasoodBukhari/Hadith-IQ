from BusinessLogicLayer.Fascade.BLLFascade import BLLFascade
from BusinessLogicLayer.Hadith.HadithBO import HadithBO
from BusinessLogicLayer.Narrator.NarratorBO import NarratorBO
from BusinessLogicLayer.Project.ProjectBO import ProjectBO
from BusinessLogicLayer.Sanad.SanadBO import SanadBO
from DataAccessLayer.Fascade.DALFascade import DALFascade
from DataAccessLayer.DbConnection import DbConnection
from DataAccessLayer.Hadith.HadithDAO import HadithDAO
from DataAccessLayer.Narrator.NarratorDAO import NarratorDAO
from DataAccessLayer.Project.ProjectDAO import ProjectDAO
from DataAccessLayer.Sanad.SanadDAO import SanadDAO
from DataAccessLayer.UtilDAO import UtilDao

def main():
    #Initiallizing DAL
    dbconnection = DbConnection()
    utilDAO= UtilDao(dbconnection)
    hadithDAO= HadithDAO(dbconnection,utilDAO)
    narratorDAO= NarratorDAO(dbconnection,utilDAO)
    projectDAO= ProjectDAO(dbconnection,utilDAO)
    sanadDAO= SanadDAO(dbconnection,utilDAO)
    dalFascade= DALFascade(hadithDAO,sanadDAO,projectDAO,narratorDAO)

    # Initializing BLL
    hadithBO= HadithBO(dalFascade)
    narratorBO= NarratorBO(dalFascade)
    projectBO= ProjectBO(dalFascade)
    sanadBO= SanadBO(dalFascade)
    bllFascade= BLLFascade(hadithBO,sanadBO,projectBO,narratorBO)

    # Sample input data for the search
    sample_hadith = "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ"
    project_name = "Temp"
    print(type(sample_hadith))  # This should be <class 'list'>
    print(type(project_name))  # This should be <class 'str'>


    # Call the semantic search function
    try:
        results = bllFascade.semanticSearch(sample_hadith,project_name)
        print("Semantic Search Results:")
        print(results)
    except Exception as e:
        print(f"Error during semantic search: {e}")

# Run the main function
if __name__ == "__main__":
    main()
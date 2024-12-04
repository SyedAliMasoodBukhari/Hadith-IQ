from fastapi import FastAPI
from BusinessLogicLayer.Fascade.BLLFascade import BLLFascade
from BusinessLogicLayer.Hadith.HadithBO import HadithBO
from BusinessLogicLayer.Narrator.NarratorBO import NarratorBO
from BusinessLogicLayer.Project.ProjectBO import ProjectBO
from BusinessLogicLayer.Sanad.SanadBO import SanadBO
from BusinessLogicLayer.api.HadithApi import hadith_router
from BusinessLogicLayer.api.HadithApi import test_router
from DataAccessLayer.Fascade.DALFascade import DALFascade
from DataAccessLayer.DbConnection import DbConnection
from DataAccessLayer.Hadith.HadithDAO import HadithDAO
from DataAccessLayer.Narrator.NarratorDAO import NarratorDAO
from DataAccessLayer.Project.ProjectDAO import ProjectDAO
from DataAccessLayer.Sanad.SanadDAO import SanadDAO
from DataAccessLayer.UtilDAO import UtilDao


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

# Initialize FastAPI app
app = FastAPI(
    title="Hadith IQ Server",
    description="API for Hadith IQ Project",
    version="1.0.0",
)

# Included routers and pass facade to them
app.include_router(hadith_router(bllFascade), prefix="/api/hadith")
app.include_router(test_router(), prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Command to run server: uvicorn BusinessLogicLayer.server:app --host 127.0.0.1 --port 8000 --reload
# call this command in the root directory of the project
# if error came for no module found bll although its there then make the pyhton to editer mode
# it will work the, run 'pip install -e .'   if its not work and give some error then: pip install --user -e .

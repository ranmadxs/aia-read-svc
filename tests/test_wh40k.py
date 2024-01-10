from dotenv import load_dotenv
load_dotenv()
from aia_read_svc.wh40kSvc import Warhammer40KService
import logging
import logging.config
import os
import yaml
import json

currentPath = os.getcwd()
with open(currentPath+"/resources/log_cfg.yaml", 'rt') as f:
    configLog = yaml.safe_load(f.read())
    logging.config.dictConfig(configLog)
logger = logging.getLogger(__name__)

def getSemanticGraph(jsonFile: str):
    logger.debug("Read message from file:")
    
    f = open(jsonFile)
    logger.debug(jsonFile)
    data = json.load(f)
    logger.debug(data)
    return data

#poetry run pytest tests/test_wh40k.py::test_getFactionsKeywords -s
def test_getFactionsKeywords():
    print("test_get_factions")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    #wh40kSvc.getFactionsKeywords("wh40k9ed") 
    wh40kSvc.getFactionsKeywords("wh40k10ed")

#poetry run pytest tests/test_wh40k.py::test_get_listKeys -s
def test_get_listKeys():
    print("test_get_listKeys")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    logger.debug(wh40kSvc.getUnitListKeywords("space-marines", "wh40k10ed"))

#poetry run pytest tests/test_wh40k.py::test_get_factions_attr -s
def test_get_factions_attr():
    print("test_get_factions")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], "test", os.getenv("WH40K_IMG_FILES_PATH"))
    unit = wh40kSvc.getUnitFactionAttr("space-marines", "Tactical-Squad") 
    #logger.debug(unit)

#poetry run pytest tests/test_wh40k.py::test_process -s
def test_process():
    print("test_process")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    #testFile = currentPath + "/resources/test/semanticGraphWH40k.json"
    testFile = currentPath + "/resources/test/sgWH40K_tactical.json"
    wh40kSvc.process(getSemanticGraph(testFile))

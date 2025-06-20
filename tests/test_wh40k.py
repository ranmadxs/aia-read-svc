import pytest
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
load_dotenv()
from aia_read_svc.wh40kSvc import Warhammer40KService
import logging
import logging.config
import os
import yaml
import json
from aia_read_svc.model.wh40k_model import WH40K_Unit, WH40K_Characteristic, WH40K_Unit_Images
from aia_read_svc.model.read_model import Speech
from aia_read_svc.model.wh40k_enum import WH40K_PROFILES
from aia_read_svc.repositories.aiaWh40kRepo import AIAWH40KRepository
from aia_read_svc.repositories.aiaRepo import AIAMessageRepository

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
    result = wh40kSvc.getUnitListKeywords("space-marines", "wh40k10ed")
    assert isinstance(result, dict)
    assert "faction" in result
    assert "edition" in result
    assert "tokens_factions" in result
    assert isinstance(result["tokens_factions"], list)
    assert result["faction"] == "space-marines"
    logger.debug(wh40kSvc.getUnitListKeywords("space-marines", "wh40k10ed"))

#poetry run pytest tests/test_wh40k.py::test_get_factions_attr -s
def test_get_factions_attr():
    print("test_get_factions")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], "test", os.getenv("WH40K_IMG_FILES_PATH"))
    unit, unitImage = wh40kSvc.getUnitFactionAttr("space-marines", "Tactical-Squad")
    #if(unitImage is not None):
        #wh40kSvc.sendImgToDev(unitImage)
    #logger.debug(unit)
	

#poetry run pytest tests/test_wh40k.py::test_process5 -s
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process5(mock_send_msg):
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "hablame de las habilidades del space marine guilliman"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process4(mock_send_msg):
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "dame las estadìsticas del arma Hand of Dominion del space marine calgar"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process3(mock_send_msg):
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "dame las estadìsticas básicas del space marine calgar"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()
    
    # Validar que el mensaje enviado contiene msg y language
    sent_message = mock_send_msg.call_args[0][0][0]  # Obtener el primer mensaje enviado
    assert 'msg' in sent_message, "El mensaje debe contener el campo 'msg'"
    assert 'language' in sent_message, "El mensaje debe contener el campo 'language'"
    assert sent_message['language'] == 'es', "El idioma debe ser 'es'"

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process_orks(mock_send_msg):
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "dame las estadìsticas de OC de los orkos de Ghazghkull"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process_orks2(mock_send_msg):
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "dame un listado de todas las armas de los orkos de Ghazghkull"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process6(mock_send_msg):
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "dame las estadìsticas un teniente de los marines espaciales"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process2(mock_send_msg):
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "dame las estadìsticas del bolter de los marines espaciales tàcticos"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()

#poetry run pytest tests/test_wh40k.py::test_process -s
@pytest.mark.skip(reason="esta pensando para funcionar con colas en ambiente local")
def test_process():
    print("test_process")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    #testFile = currentPath + "/resources/test/semanticGraphWH40k.json"
    testFile = currentPath + "/resources/test/wh40k_ancient.json"
    wh40kSvc.process(getSemanticGraph(testFile))

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
def test_get_unit_information():
    print("test_get_unit_information")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    prompt = "me puedes dar las estadísticas base para "
    # Test case: Get information for Lieutenant Titus
    unit_info = wh40kSvc.getUnitInformation("Lieutenant-Titus", "space-marines", "wh40k10ed", prompt)
    print("\nUnit Information:")
    print(unit_info)
    assert unit_info is not None
    assert isinstance(unit_info, str)

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
def test_getKeyUnitFromMsg():
    print("test_getKeyUnitFromMsg")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    list_units = ["Tactical Squad", "Lieutenant Titus", "Ancient"]
    msg = "Lieutenant Titus"
    result = wh40kSvc.getKeyUnitFromMsg(list_units, msg)
    assert result is not None
    assert isinstance(result, str)
    print(f"Result: {result}")

@pytest.mark.skip(reason="Uses Gemini API - rate limiting issues")
@patch('aia_read_svc.wh40kSvc.Warhammer40KService.sendMsg')
def test_process_wh40k_obj(mock_send_msg):
    print("test_process_wh40k_obj")
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    testFile = currentPath + "/resources/test/wh40k_ancient.json"
    prompt = "dame las estadìsticas solo del arma bolter de los marines espaciales tácticos"
    result = wh40kSvc.process_wh40k_obj(prompt)
    assert result is not None
    mock_send_msg.assert_called_once()

def test_imports_and_instantiation():
    """Test that all imports work and the service can be instantiated"""
    print("test_imports_and_instantiation")
    
    # Test that we can import the repositories
    assert AIAWH40KRepository is not None
    assert AIAMessageRepository is not None
    
    # Test that we can instantiate the service
    wh40kSvc = Warhammer40KService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'])
    assert wh40kSvc is not None
    assert wh40kSvc.aiaWHRepo is not None
    assert wh40kSvc.aiaMsgRepo is not None
    
    print("✓ All imports and instantiation working correctly")

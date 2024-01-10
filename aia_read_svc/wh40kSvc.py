import json
import html_to_json
import requests
from bs4 import BeautifulSoup
import bs4
from .model.wh40k_model import WH40K_Characteristic, WH40K_Unit
from .model.read_model import Speech
from .model.wh40k_enum import WH40K_PROFILES
from typing import List
import Levenshtein as lev
from numpy import loadtxt
import os
import io
from repositories.aiaWh40kRepo import AIAWH40KRepository
from repositories.aiaRepo import AIAMessageRepository
from dotenv import load_dotenv
load_dotenv()
from aia_utils.img_utils import ImageUtils
from aia_utils.Queue import QueueProducer
from aia_utils.logs_cfg import config_logger
import logging

class Warhammer40KService:
    def __init__(self, topic_producer: str, version: str = "v1", output_path='target'):
        self.topic_producer = topic_producer
        config_logger()
        self.logger = logging.getLogger(__name__)
        self.aiaWHRepo = AIAWH40KRepository(os.environ['MONGODB_URI'])
        self.aiaMsgRepo = AIAMessageRepository(os.environ['MONGODB_URI'])
        self.queueProducer = QueueProducer(self.topic_producer, version, "aia-read-svc")
        self.queueDevice = QueueProducer(os.environ['CLOUDKAFKA_TOPIC_DEVICE_PRODUCER'], version, "aia-read-svc")
        self.wahapedia_css = open("resources/wh40k/wahapedia.css", "r")
        self.wahapedia_css = self.wahapedia_css.read()
        self.output_path = output_path
        self.hti = ImageUtils(output_path=output_path)

    def compareToken(self, token_list: List, word: str, ratio_compare: float = 0.5):
        token_list_resp = []
        self.logger.debug(word)
        max_ratio = float(0.0)
        max_token = None
        for token in token_list:
            distance = lev.distance(str(token), word)
            ratio = float(lev.ratio(str(token), word))
            token_list_resp.append({
                "token": token,
                "distance": distance,
                "ratio": ratio
            })
            if ratio > max_ratio and ratio > ratio_compare:
                max_ratio = ratio
                max_token = {
                    'token': token,
                    'ratio': ratio,
                    'distance': distance,
                    'word_count': len(token.split('-'))
                }
            
        self.logger.debug(token_list_resp)
        return max_token

    def getUnitFromMsg(self, listNodes: List, countTokens: int) -> WH40K_Unit:
        msgArray = []
        count = int(0)
        for node in listNodes:
            count = count + 1
            if countTokens < count:
                msgArray.append(node['originalText'])
        return ' '.join(msgArray)
    
    def sendImgToDev(self, name: str):
        self.queueDevice.send({"type": "image_resources", "origin": "resources/images", "name": name})
        self.queueDevice.flush()

    def sendMsg(self, sentences: list):

        dbObject = self.queueProducer.msgBuilder({
            "sentences": sentences,
            "classification": "WH40K"
        })
        id = self.aiaMsgRepo.insertAIAReadMessage(dbObject)
        self.logger.debug(id)
        sendObject = self.queueProducer.msgBuilder({
            "sentences": sentences,
            "classification": "WH40K"
        })
        sendObject['id'] = str(id)
        sendObject['database'] = "aIAReadMessage"
        msg_str = json.dumps(sendObject)
        self.logger.debug(msg_str)
        self.queueProducer.send(msg_str)
        self.queueProducer.flush()  

    def process(self, wh40kObj: any, edition: str = "wh40k10ed"):
        ratio_compare: float = 0.51
        self.logger.debug("Processing wh40kObj")
        self.logger.debug(os.getcwd())
        data = loadtxt('./resources/wh40k/wh40k_tokens.txt', dtype='str')
        self.logger.debug(data)
        self.logger.debug(data.dtype)
        faction_token = self.compareToken(data, wh40kObj['sentence'].replace("modo warhammer", ""), ratio_compare)
        self.logger.info(faction_token)
        factionKeys = self.getUnitListKeywords(faction_token['token'], edition)

        #self.logger.debug(factionKeys['tokens_factions'])
        #self.logger.debug(wh40kObj['nodes'])
        msg_current = self.getUnitFromMsg(wh40kObj['nodes'], int(faction_token['word_count']) + 2)
        self.logger.debug(msg_current)
        keywordsUnits = self.getUnitListKeywords(faction_token['token'], edition)
        unit_token = self.compareToken(keywordsUnits['tokens_factions'], msg_current, ratio_compare = 0.5)
        self.logger.info(unit_token)
        unit = self.getUnitFactionAttr(faction_token['token'], unit_token['token'])
        self.logger.debug(unit)
        sentences = [{"msg": f"{unit.speech.text}", "sound_in": "transition02.wav", "language": f"{unit.speech.language}"}]
        self.sendMsg(sentences)
        self.sendImgToDev(unit.image_name)
        self.logger.debug(sentences)
        
    def getFactionsKeywords(self, edition: str = "wh40k10ed") -> List:
        self.logger.debug("Getting factions keywords")
        tokensFactions = loadtxt('./resources/wh40k/wh40k_tokens.txt', dtype='str')
        keywordFactions = []
        for token in tokensFactions:
            factionKeys = self.getUnitListKeywords(token, edition)
            keywordFactions.append(factionKeys)

        self.logger.debug(keywordFactions)
        return keywordFactions

    def getUnitListKeywords(self, faction: str, edition : str = 'wh40k10ed') -> List:
        self.logger.debug("Getting faction getUnitListKeywords")
        urlTokensList = []
        respFaction = self.aiaWHRepo.findWh40kFaction(faction, edition)
        if (respFaction is not None) and (respFaction["_id"] is not None):
            urlTokensList.append(respFaction)
        else:
            response = requests.get(f"https://wahapedia.ru/{edition}/factions/{faction}/")
            print (response.status_code)            
            if response.status_code == 200:
                f = open("wenfactions.html", "w")
                #f.write(str(response.content))
                soup = BeautifulSoup(response.content, 'html.parser')
                mydivs = soup.find_all("div", {"class": "NavDropdown-content_P"})
                divMain = mydivs[0]
                print(type(divMain))
                urlsTokens = divMain.findChildren("a", {"class": "contentColor"})

                for urlToken in urlsTokens:
                    #print(urlToken.attrs["href"])
                    srtReplace = f"/{edition}/factions/{faction}/"
                    tokenElement = urlToken.attrs["href"].replace(srtReplace, "")
                    urlTokensList.append(tokenElement)
            #self.logger.debug(urlsTokens)
            #self.logger.debug(divMain.prettify())
            #charachteristicsDivs = soup.select("a.contentColor")
            respFaction = {"faction": faction, "edition": edition, "tokens_factions": urlTokensList}
            self.aiaWHRepo.insertWh40kFaction(respFaction)
        #self.logger.debug(respFaction)
        return respFaction

    def getUnitFactionAttr(self, faction: str, unit_code: str, edition: str = 'wh40k10ed') -> WH40K_Unit:
        self.logger.debug("Getting unit faction attr")
        unit = self.aiaWHRepo.findWH40KUnit(unit_code, faction, edition)
        #TODO: agregar copiar imagen a ruta cuando se carga de la url self.output_path
        if (unit is not None) and (unit["_id"] is not None):
            self.logger.debug(type(unit))
            speech = Speech(unit["speech"]["text"], unit["speech"]["language"])
            unit = WH40K_Unit(unit)
            unit.speech = speech
            return unit
        response = requests.get(f"https://wahapedia.ru/{edition}/factions/{faction}/{unit_code}")
        unit = None
        
        print (response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find("div", {"class": "dsOuterFrame"})
            html_main_div = main_div.prettify()
            image_name = 'wahapedia_snapshot.png'
            img_snapshot = self.hti.html2img(name=image_name, html=html_main_div, css=self.wahapedia_css, size=(960, 640))            
            mydivs = soup.find_all("div", {"class": "dsProfileWrapLeft"})
            html_content = mydivs[0].prettify()
            print(html_content)
            output_json_fullcontent = html_to_json.convert(html_content)
            print(output_json_fullcontent)
            charachteristicsDivs = soup.select("div.dsCharWrap")
            unitDivs = soup.select_one("div.dsH2Header div:first-child")
            characteristics = []
            print("-----------------------------")
            self.logger.debug(charachteristicsDivs)
            speech = Speech("", "en")
            if charachteristicsDivs is not None:
                speech.text = f"{speech.text}{unitDivs.text.strip()} characteristics are: "            
            for ele in charachteristicsDivs:
                if isinstance(ele, bs4.element.Tag):
                    print(">>>>>>>>>>>>>< DIV <<<<<<<<<<<<<<<<<<<")
                    divCharName = ele.findChildren("div", {"class": "dsCharName"})
                    divValue = ele.findChildren("div", {"class": "dsCharValue"})
                    divCharName = divCharName.pop(0)
                    divValue = divValue.pop(0)
                    strProfile = WH40K_PROFILES[divCharName.text.strip()].value
                    self.logger.info(divCharName.text.strip())
                    self.logger.info(strProfile)
                    speech.text = speech.text + f"{strProfile} {divValue.text.strip()}, "
                    characteristics.append(WH40K_Characteristic(divCharName.text.strip(), divValue.text.strip()))
            invulDivs = soup.select_one("div.dsInvulWrap")
            if (invulDivs is not None):
                chr_name = soup.select_one("div.dsInvulWrap div:first-child").text.strip()
                chr_value = soup.select_one("div.dsInvulWrap div.dsCharInvulValue").text.strip()
                characteristics.append(WH40K_Characteristic(
                    chr_name,
                    chr_value))
                speech.text = speech.text + f"{chr_name} {chr_value} "
            self.logger.debug(invulDivs)

            image_bytes = io.BytesIO()
            img_snapshot.save(image_bytes, format='PNG')

            unit = WH40K_Unit({
                "name": unitDivs.text.strip(), 
                "code": unit_code, 
                "speech": speech, 
                "faction": faction, 
                "edition": edition, 
                "characteristics":characteristics,
                "image": image_bytes.getvalue(),
                "image_name": image_name
                })
            self.aiaWHRepo.insertWh40kUnit(unit.dict())
        return unit
        
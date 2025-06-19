import pytest
import mongomock
from unittest.mock import patch
from aia_read_svc.repositories.aiaWh40kRepo import AIAWH40KRepository

class TestAIAWH40KRepository:
    """Tests unitarios para AIAWH40KRepository usando mongomock"""
    
    def setup_method(self):
        """Configurar el mock de MongoDB antes de cada test"""
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client["wh40k-db"]
        
        # Mock de las colecciones
        self.mock_faction_collection = self.mock_db["wh40kFaction"]
        self.mock_unit_collection = self.mock_db["wh40kUnit"]
        self.mock_image_collection = self.mock_db["wh40kUnitImages"]
    
    @patch('aia_read_svc.repositories.aiaWh40kRepo.MongoClient')
    def test_insert_wh40k_faction(self, mock_mongo_client):
        """Test para insertar una facción de WH40K"""
        # Configurar el mock
        mock_mongo_client.return_value = self.mock_client
        
        # Crear instancia del repositorio
        repo = AIAWH40KRepository("mongodb://localhost:27017")
        
        # Datos de prueba
        faction_data = {
            "faction": "space-marines",
            "edition": "wh40k10ed",
            "tokens_factions": ["Captain", "Lieutenant", "Tactical Squad"]
        }
        
        # Ejecutar el método
        result_id = repo.insertWh40kFaction(faction_data)
        
        # Verificar que se insertó correctamente
        assert result_id is not None
        
        # Verificar que los datos están en la colección
        inserted_faction = self.mock_faction_collection.find_one({"_id": result_id})
        assert inserted_faction is not None
        assert inserted_faction["faction"] == "space-marines"
        assert inserted_faction["edition"] == "wh40k10ed"
        assert len(inserted_faction["tokens_factions"]) == 3
    
    @patch('aia_read_svc.repositories.aiaWh40kRepo.MongoClient')
    def test_find_wh40k_faction(self, mock_mongo_client):
        """Test para buscar una facción de WH40K"""
        # Configurar el mock
        mock_mongo_client.return_value = self.mock_client
        
        # Insertar datos de prueba
        faction_data = {
            "faction": "orks",
            "edition": "wh40k10ed",
            "tokens_factions": ["Warboss", "Boyz", "Trukk"]
        }
        self.mock_faction_collection.insert_one(faction_data)
        
        # Crear instancia del repositorio
        repo = AIAWH40KRepository("mongodb://localhost:27017")
        
        # Ejecutar el método
        result = repo.findWh40kFaction("orks", "wh40k10ed")
        
        # Verificar el resultado
        assert result is not None
        assert result["faction"] == "orks"
        assert result["edition"] == "wh40k10ed"
        assert len(result["tokens_factions"]) == 3
    
    @patch('aia_read_svc.repositories.aiaWh40kRepo.MongoClient')
    def test_find_wh40k_faction_not_found(self, mock_mongo_client):
        """Test para buscar una facción que no existe"""
        # Configurar el mock
        mock_mongo_client.return_value = self.mock_client
        
        # Crear instancia del repositorio
        repo = AIAWH40KRepository("mongodb://localhost:27017")
        
        # Ejecutar el método
        result = repo.findWh40kFaction("non-existent", "wh40k10ed")
        
        # Verificar que no se encontró
        assert result is None
    
    @patch('aia_read_svc.repositories.aiaWh40kRepo.MongoClient')
    def test_insert_wh40k_unit(self, mock_mongo_client):
        """Test para insertar una unidad de WH40K"""
        # Configurar el mock
        mock_mongo_client.return_value = self.mock_client
        
        # Crear instancia del repositorio
        repo = AIAWH40KRepository("mongodb://localhost:27017")
        
        # Datos de prueba
        unit_data = {
            "name": "Captain",
            "code": "captain",
            "faction": "space-marines",
            "edition": "wh40k10ed",
            "characteristics": []
        }
        
        # Ejecutar el método
        result_id = repo.insertWh40kUnit(unit_data)
        
        # Verificar que se insertó correctamente
        assert result_id is not None
        
        # Verificar que los datos están en la colección
        inserted_unit = self.mock_unit_collection.find_one({"_id": result_id})
        assert inserted_unit is not None
        assert inserted_unit["name"] == "Captain"
        assert inserted_unit["code"] == "captain"
        assert inserted_unit["faction"] == "space-marines"
    
    @patch('aia_read_svc.repositories.aiaWh40kRepo.MongoClient')
    def test_find_wh40k_unit(self, mock_mongo_client):
        """Test para buscar una unidad de WH40K"""
        # Configurar el mock
        mock_mongo_client.return_value = self.mock_client
        
        # Insertar datos de prueba
        unit_data = {
            "name": "Lieutenant",
            "code": "lieutenant",
            "faction": "space-marines",
            "edition": "wh40k10ed",
            "characteristics": []
        }
        unit_id = self.mock_unit_collection.insert_one(unit_data).inserted_id
        
        # Crear instancia del repositorio
        repo = AIAWH40KRepository("mongodb://localhost:27017")
        
        # Ejecutar el método
        unit, unit_image = repo.findWH40KUnit("lieutenant", "space-marines", "wh40k10ed")
        
        # Verificar el resultado
        assert unit is not None
        assert unit["name"] == "Lieutenant"
        assert unit["code"] == "lieutenant"
        assert unit_image is None  # No hay imagen asociada
    
    @patch('aia_read_svc.repositories.aiaWh40kRepo.MongoClient')
    def test_find_wh40k_unit_with_image(self, mock_mongo_client):
        """Test para buscar una unidad de WH40K con imagen"""
        # Configurar el mock
        mock_mongo_client.return_value = self.mock_client
        
        # Insertar datos de prueba
        unit_data = {
            "name": "Captain",
            "code": "captain",
            "faction": "space-marines",
            "edition": "wh40k10ed",
            "characteristics": []
        }
        unit_id = self.mock_unit_collection.insert_one(unit_data).inserted_id
        
        # Insertar imagen asociada
        image_data = {
            "unit_id": unit_id,
            "image_name": "captain.png",
            "image": b"fake_image_data"
        }
        self.mock_image_collection.insert_one(image_data)
        
        # Crear instancia del repositorio
        repo = AIAWH40KRepository("mongodb://localhost:27017")
        
        # Ejecutar el método
        unit, unit_image = repo.findWH40KUnit("captain", "space-marines", "wh40k10ed")
        
        # Verificar el resultado
        assert unit is not None
        assert unit["name"] == "Captain"
        assert unit_image is not None
        assert unit_image["image_name"] == "captain.png"
    
    @patch('aia_read_svc.repositories.aiaWh40kRepo.MongoClient')
    def test_insert_unit_image(self, mock_mongo_client):
        """Test para insertar una imagen de unidad"""
        # Configurar el mock
        mock_mongo_client.return_value = self.mock_client
        
        # Crear instancia del repositorio
        repo = AIAWH40KRepository("mongodb://localhost:27017")
        
        # Datos de prueba
        image_data = {
            "unit_id": "fake_unit_id",
            "image_name": "test_image.png",
            "image": b"fake_image_data"
        }
        
        # Ejecutar el método
        result_id = repo.insertUnitImage(image_data)
        
        # Verificar que se insertó correctamente
        assert result_id is not None
        
        # Verificar que los datos están en la colección
        inserted_image = self.mock_image_collection.find_one({"_id": result_id})
        assert inserted_image is not None
        assert inserted_image["image_name"] == "test_image.png"
        assert inserted_image["unit_id"] == "fake_unit_id" 
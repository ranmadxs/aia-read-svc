import pytest
import mongomock
from unittest.mock import patch
from aia_read_svc.repositories.aiaRepo import AIAMessageRepository
from datetime import datetime

class TestAIAMessageRepository:
    """Tests unitarios para AIAMessageRepository usando mongomock"""
    
    def setup_method(self):
        """Configurar el mock de MongoDB antes de cada test"""
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client["aia-db"]
        
        # Mock de las colecciones
        self.mock_breadcrumb_collection = self.mock_db["aIABreadcrumb"]
        self.mock_message_collection = self.mock_db["aIAMessage"]
        self.mock_read_message_collection = self.mock_db["aIAReadMessage"]
    
    #poetry run pytest tests/test_aiaRepo.py::TestAIAMessageRepository::test_insert_aia_breadcrumb -v
    @patch('aia_read_svc.repositories.aiaRepo.MongoClient')
    def test_insert_aia_breadcrumb(self, mock_mongo_client):
        """Test para insertar un breadcrumb"""
        mock_mongo_client.return_value = self.mock_client
        repo = AIAMessageRepository("mongodb://localhost:27017")
        breadcrumb_data = {"user": "test", "timestamp": datetime.now()}
        result_id = repo.insertAIABreadcrumb(breadcrumb_data)
        assert result_id is not None
        inserted = self.mock_breadcrumb_collection.find_one({"_id": result_id})
        assert inserted is not None
        assert inserted["user"] == "test"
    
    #poetry run pytest tests/test_aiaRepo.py::TestAIAMessageRepository::test_insert_aia_message -v
    @patch('aia_read_svc.repositories.aiaRepo.MongoClient')
    def test_insert_aia_message(self, mock_mongo_client):
        """Test para insertar un mensaje"""
        mock_mongo_client.return_value = self.mock_client
        repo = AIAMessageRepository("mongodb://localhost:27017")
        message_data = {"msg": "hello", "timestamp": datetime.now()}
        result_id = repo.insertAIAMessage(message_data)
        assert result_id is not None
        inserted = self.mock_message_collection.find_one({"_id": result_id})
        assert inserted is not None
        assert inserted["msg"] == "hello"
    
    #poetry run pytest tests/test_aiaRepo.py::TestAIAMessageRepository::test_insert_aia_read_message -v
    @patch('aia_read_svc.repositories.aiaRepo.MongoClient')
    def test_insert_aia_read_message(self, mock_mongo_client):
        """Test para insertar un mensaje leído"""
        mock_mongo_client.return_value = self.mock_client
        repo = AIAMessageRepository("mongodb://localhost:27017")
        read_message_data = {"msg": "read", "timestamp": datetime.now()}
        result_id = repo.insertAIAReadMessage(read_message_data)
        assert result_id is not None
        inserted = self.mock_read_message_collection.find_one({"_id": result_id})
        assert inserted is not None
        assert inserted["msg"] == "read" 
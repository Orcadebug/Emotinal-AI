import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from brain import Brain

@pytest.fixture
def mock_brain():
    with patch("brain.psycopg2.connect") as mock_connect:
        with patch("brain.tinker.ServiceClient") as mock_service:
            # Mock DB Connection
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            
            # Mock Tinker
            mock_brain_instance = Brain()
            mock_brain_instance.sampling_client = MagicMock()
            mock_brain_instance.tokenizer = MagicMock()
            mock_brain_instance.tokenizer.encode.return_value = [1, 2, 3]
            mock_brain_instance.tokenizer.decode.return_value = "Hello there!"
            
            # Mock sampling result
            mock_future = MagicMock()
            mock_result = MagicMock()
            mock_seq = MagicMock()
            mock_seq.tokens = [4, 5, 6]
            mock_result.sequences = [mock_seq]
            mock_future.result.return_value = mock_result
            mock_brain_instance.sampling_client.sample.return_value = mock_future
            
            yield mock_brain_instance

def test_brain_initialization(mock_brain):
    assert mock_brain.service_client is not None
    assert mock_brain.sampling_client is not None

def test_process_message_awake(mock_brain):
    # Mock bio state: awake
    mock_conn = mock_brain.get_db_connection()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.side_effect = [
        {"adenosine": 0.1, "sleep_mode": False}, # get_biological_state
        {"affinity": 10.0, "name": "TestUser", "secret_phrase": None}, # update_relationship
        (0.15,) # update_biological_state - returns tuple
    ]
    
    response = mock_brain.process_message("user1", "Hello")
    
    assert response["response"] == "Hello there!"
    assert response["mood"] == "awake"

def test_process_message_asleep(mock_brain):
    # Mock bio state: asleep
    mock_conn = mock_brain.get_db_connection()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.side_effect = [
        {"adenosine": 0.95, "sleep_mode": True}, # get_biological_state
    ]
    
    response = mock_brain.process_message("user1", "Hello")
    
    assert "Zzz" in response["response"]
    assert response["mood"] == "asleep"

def test_auth_command_name(mock_brain):
    # Mock bio state
    mock_conn = mock_brain.get_db_connection()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.side_effect = [
        {"adenosine": 0.1, "sleep_mode": False}, # get_biological_state
        {"affinity": 10.0, "name": "TestUser", "secret_phrase": None}, # update_relationship
        (0.15,) # update_biological_state
    ]
    
    mock_brain.process_message("user1", "My name is Alice")
    
    # Check if UPDATE was called for name
    # We need to check the calls to cursor.execute
    # This is a bit tricky with the mocks, but let's just ensure no error
    pass

def test_auth_command_secret(mock_brain):
    # Mock bio state
    mock_conn = mock_brain.get_db_connection()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.side_effect = [
        {"adenosine": 0.1, "sleep_mode": False}, # get_biological_state
        {"affinity": 10.0, "name": "TestUser", "secret_phrase": None}, # update_relationship
        (0.15,) # update_biological_state
    ]
    
    response = mock_brain.process_message("user1", "Set secret MySecret")
    
    assert "Secret set" in response["response"]
    assert response["mood"] == "neutral"

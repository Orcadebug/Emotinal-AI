import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Mock dependencies before import
sys.modules['psycopg2'] = MagicMock()
sys.modules['psycopg2.extras'] = MagicMock()
sys.modules['tinker'] = MagicMock()
sys.modules['tinker.types'] = MagicMock()

from brain import Brain

class TestBiologicalMechanics(unittest.TestCase):
    def setUp(self):
        # Mock environment variables
        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@localhost/db", "TINKER_API_KEY": "fake"}):
            with patch('brain.Brain._initialize_tinker'):
                with patch('brain.Brain._initialize_db'):
                    self.brain = Brain()

    @patch('psycopg2.connect')
    def test_adenosine_clamping(self, mock_connect):
        """Test that adenosine stays between 0.0 and 1.0"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        
        # Test upper clamp
        # Simulate query returning 1.0
        mock_cur.fetchone.return_value = [1.0]
        result = self.brain.update_biological_state(mock_conn, adenosine_change=0.5)
        
        # Check SQL
        sql = mock_cur.execute.call_args[0][0]
        self.assertIn("GREATEST(LEAST(adenosine + %s, 1.0), 0.0)", sql)
        
    @patch('psycopg2.connect')
    def test_wake_up(self, mock_connect):
        """Test wake_up resets state"""
        self.brain.get_db_connection = MagicMock(return_value=mock_connect.return_value)
        mock_conn = mock_connect.return_value
        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        
        success = self.brain.wake_up()
        
        self.assertTrue(success)
        mock_cur.execute.assert_called_with("""
                    UPDATE biological_state 
                    SET adenosine = 0.0, 
                        sleep_mode = FALSE,
                        last_updated = CURRENT_TIMESTAMP
                """)

if __name__ == '__main__':
    unittest.main()

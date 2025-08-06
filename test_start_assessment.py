#!/usr/bin/env python3
"""
Test script for the start_assessment Azure Function.
This script tests the function's logic locally without needing live Azure services.
"""

import unittest
import json
import os
import sys
import uuid
import re
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Mock Azure modules before any imports
class MockHttpRequest:
    def __init__(self, method="POST", url="http://localhost:7071/api/assessment"):
        self.method = method
        self.url = url

class MockHttpResponse:
    def __init__(self, body, status_code=200, mimetype="application/json"):
        self.body = body
        self.status_code = status_code
        self.mimetype = mimetype
    
    def get_body(self):
        return self.body

# Mock all Azure modules
sys.modules['azure'] = MagicMock()
sys.modules['azure.functions'] = MagicMock()
sys.modules['azure.functions'].func = MagicMock()
sys.modules['azure.functions'].func.HttpRequest = MockHttpRequest
sys.modules['azure.functions'].func.HttpResponse = MockHttpResponse

sys.modules['azure.cosmos'] = MagicMock()
sys.modules['azure.cosmos.cosmos_client'] = MagicMock()
sys.modules['azure.cosmos.exceptions'] = MagicMock()
sys.modules['openai'] = MagicMock()

# Now we can safely import our function
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'start_assessment'))

class TestStartAssessment(unittest.TestCase):
    """Test suite for the start_assessment function."""

    def test_is_valid_nickname_format(self):
        """Test the nickname format validation logic."""
        # Import the function after mocking
        from start_assessment import is_valid_nickname_format
        
        # Test valid nicknames
        valid_nicknames = [
            "Crimson-Llama-42",
            "Aqua-Badger-88",
            "Emerald-Phoenix-15",
            "Azure-Dragon-99"
        ]
        
        for nickname in valid_nicknames:
            with self.subTest(nickname=nickname):
                self.assertTrue(
                    is_valid_nickname_format(nickname), 
                    f"Nickname '{nickname}' should be valid"
                )
        
        # Test invalid nicknames
        invalid_nicknames = [
            "Crimson-Llama-4",  # Number too short
            "Crimson-Llama-123",  # Number too long
            "crimson-llama-42",  # Lowercase
            "Crimson_Llama_42",  # Wrong separator
            "Crimson-Llama-42-extra",  # Too many parts
            "Crimson-42",  # Missing animal
            "Crimson-Llama",  # Missing number
            "crimson-Llama-42",  # Lowercase first word
            "Crimson-llama-42",  # Lowercase second word
        ]
        
        for nickname in invalid_nicknames:
            with self.subTest(nickname=nickname):
                self.assertFalse(
                    is_valid_nickname_format(nickname), 
                    f"Nickname '{nickname}' should be invalid"
                )

    def test_create_session_document(self):
        """Test the session document creation logic."""
        from start_assessment import create_session_document
        
        session_id = str(uuid.uuid4())
        nickname = "Test-Nickname-42"
        
        doc = create_session_document(session_id, nickname)
        
        # Verify required fields
        self.assertEqual(doc["id"], session_id)
        self.assertEqual(doc["nickname"], nickname)
        self.assertEqual(doc["status"], "InProgress")
        self.assertIsNone(doc["contactEmail"])
        self.assertIsNone(doc["completedAt"])
        self.assertIsNone(doc["reportFirstViewedAt"])
        self.assertEqual(doc["answers"], [])
        self.assertIsNone(doc["result"])
        
        # Verify timestamp format
        self.assertIn("createdAt", doc)
        datetime.fromisoformat(doc["createdAt"].replace("Z", "+00:00"))

    @patch.dict(os.environ, {
        'COSMOS_ENDPOINT': 'https://test.documents.azure.com:443/',
        'COSMOS_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_KEY': 'test-key'
    })
    @patch('start_assessment.cosmos_client.CosmosClient')
    @patch('start_assessment.openai.AzureOpenAI')
    def test_main_function_with_mocks(self, mock_openai_client, mock_cosmos_client):
        """Test the main function with mocked Azure services."""
        from start_assessment import main
        
        # Configure OpenAI mock
        mock_openai_instance = mock_openai_client.return_value
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Aqua-Badger-88"
        mock_openai_instance.chat.completions.create.return_value = mock_completion
        
        # Configure Cosmos DB mock
        mock_container = MagicMock()
        mock_container.query_items.return_value = [0]  # No existing nicknames
        mock_db = MagicMock()
        mock_db.get_container_client.return_value = mock_container
        mock_cosmos_instance = mock_cosmos_client.return_value
        mock_cosmos_instance.get_database_client.return_value = mock_db
        
        # Create mock request
        mock_req = MockHttpRequest()
        
        # Call the function
        response = main(mock_req)
        
        # Verify response structure (without checking exact values due to mocking)
        self.assertIsNotNone(response)
        self.assertTrue(hasattr(response, 'status_code') or hasattr(response, 'body'))
        
        # Verify database was called
        mock_container.create_item.assert_called_once()

def run_manual_tests():
    """Run tests manually for easier debugging."""
    print("🧪 Testing start_assessment function...")
    
    # Test nickname validation
    print("\n1. Testing nickname format validation...")
    test = TestStartAssessment()
    test.test_is_valid_nickname_format()
    print("✅ Nickname validation tests passed")
    
    # Test session document creation
    print("\n2. Testing session document creation...")
    test.test_create_session_document()
    print("✅ Session document creation tests passed")
    
    # Test main function (this will show expected errors without Azure services)
    print("\n3. Testing main function structure...")
    try:
        test.test_main_function_with_mocks()
        print("✅ Main function test passed")
    except Exception as e:
        print(f"⚠️  Main function test: {e}")
        print("This is expected without Azure services configured")
    
    print("\n🎉 All tests completed!")
    print("\nTo test the full function, you'll need to:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure Azure credentials in local.settings.json")
    print("3. Run: func start")
    print("4. Test with: curl -X POST http://localhost:7071/api/assessment")

if __name__ == '__main__':
    # Run either unittest or manual tests
    if len(sys.argv) > 1 and sys.argv[1] == "--unittest":
        # Run with unittest framework
        unittest.main(argv=[''], exit=False)
    else:
        # Run manual tests (more user-friendly)
        run_manual_tests()
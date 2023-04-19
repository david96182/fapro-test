import sys
import os

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch
from app import create_app
import json


class GetUfValueTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()

    def test_get_valid_uf_value(self):
        # Test getting a valid UF value for a date
        response = self.client.get('/api/date?date=19-04-2023')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('date', data)
        self.assertIsInstance(data, dict)

    def test_missing_date_parameter(self):
        # Test getting a UF value without providing the date parameter
        data = {'date': ''}
        headers = {'Content-Type': 'application/json'}
        response = self.client.get('/api/date', data=json.dumps(data), headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'DATE_MISSING')
        self.assertIn('message', data)

    def test_invalid_date_format(self):
        # Test getting a UF value with an invalid date format
        response = self.client.get('/api/date?date=2023-04-19')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'DATE_INVALID_FORMAT')
        self.assertIn('message', data)

    def test_invalid_date_range(self):
        # Test getting a UF value with a date outside the valid range
        response = self.client.get('/api/date?date=01-01-2012')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'DATE_INVALID_RANGE')
        self.assertIn('message', data)

    def test_post_body_parameter(self):
        # Test getting a UF value from a POST request with a body parameter
        data = {'date': '19-04-2023'}
        headers = {'Content-Type': 'application/json'}
        response = self.client.post('/api/date', data=json.dumps(data), headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('date', data)
        self.assertIsInstance(data, dict)

    def test_date_url_parameter(self):
        # Test getting a UF value from a GET request with a URL parameter
        response = self.client.get('/api/date?date=19-04-2022')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('date', data)
        self.assertIsInstance(data, dict)

    @patch('requests.get')
    def test_external_api_connection_error(self, mock_get):
        # Test handling a connection error when calling the external API
        mock_get.side_effect = requests.exceptions.ConnectionError()
        response = self.client.get('/api/date?date=19-04-2023')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'CONNECTION_ERROR')
        self.assertIn('message', data)

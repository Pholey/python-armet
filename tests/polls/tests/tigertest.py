from django.utils import unittest
from django.test.client import Client
from lxml import etree
import json


class TigerTest(unittest.TestCase):
    """Unit Tests for the Are You A Tiger poll object"""

    def setUp(self):
        """Set up the django HTTP client"""
        self.c = Client()

    def test_list_view_xml(self):
        """Gets the list view in xml format"""
        response = self.c.get('/api/v1/poll.xml/')
        self.assertEqual(response.status_code, 200)
        try:
            etree.fromstring(response.content)
        except XMLSyntaxError:
            self.assertEqual(False, 'This is not XML!')

    def test_list_view_json(self):
        """Gets the list view in json format"""
        response = self.c.get('/api/v1/poll.json/')
        self.assertEqual(response.status_code, 200)
        try:
            json.loads(response.content)
        except ValueError:
            self.assertEqual(False, 'This is not really JSON!')

    def test_list_view_text(self):
        """Gets the list view in text format"""
        response = self.c.get('/api/v1/poll.text/')
        self.assertEqual(response.status_code, 200)

    def test_get_poll_json(self):
        """Gets a json listing on a poll"""
        response = self.c.get('/api/v1/poll/1.json')
        self.assertEqual(response.status_code, 200)
        try:
            json.loads(response.content)
        except ValueError:
            self.assertEqual(False, 'This is not really JSON!')

    def test_get_poll_file_json(self):
        """Gets poll file in JSON"""
        response = self.c.get('/api/v1/poll/1/file.json')
        self.assertEqual(response.status_code, 200)
        try:
            json.loads(response.content)
        except ValueError:
            self.assertEqual(False, 'This is not really JSON!')

    def test_get_choice_list_json(self):
        """Gets poll file in JSON"""
        response = self.c.get('/api/v1/choice.json')
        self.assertEqual(response.status_code, 200)
        try:
            json.loads(response.content)
        except ValueError:
            self.assertEqual(False, 'This is not really JSON!')

    def test_get_choice_json(self):
        """Gets poll file in JSON"""
        response = self.c.get('/api/v1/choice/1.json')
        self.assertEqual(response.status_code, 200)
        try:
            json.loads(response.content)
        except ValueError:
            self.assertEqual(False, 'This is not really JSON!')

# Stuff we should implement in the flapjack REST tester:

# assertResponseisJSON

# assertResponseisText

# assertResponseisXML

# assertHttpOK

# assertHttpCreated

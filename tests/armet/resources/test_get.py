# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division
from armet import http, test
import json


class GetTestCase(test.TestCase):

    def test_list(self):
        response, content = self.client.request('/api/poll/')

        content = json.loads(content.decode('utf-8'))

        self.assertEqual(response.status, http.client.OK)
        self.assertIsInstance(content, list)
        self.assertEqual(len(content), 100)
        self.assertEqual(
            content[0]['question'], 'Are you an innie or an outie?')
        self.assertEqual(
            content[-1]['question'],
            'What one question would you add to this survey?')

    def test_single(self):
        response, content = self.client.request('/api/poll/1/')

        content = json.loads(content.decode('utf-8'))

        self.assertEqual(response.status, http.client.OK)
        self.assertIsInstance(content, dict)
        self.assertEqual(
            content['question'], 'Are you an innie or an outie?')

        response, content = self.client.request('/api/poll/100/')

        content = json.loads(content.decode('utf-8'))

        self.assertEqual(response.status, http.client.OK)
        self.assertIsInstance(content, dict)
        self.assertEqual(
            content['question'],
            'What one question would you add to this survey?')

    def test_not_found(self):
        response, _ = self.client.request('/api/poll/101/')

        self.assertEqual(response.status, http.client.NOT_FOUND)

    def test_streaming(self):
        response, content = self.client.request('/api/streaming/')

        self.assertEqual(response.status, http.client.OK)
        self.assertEqual(response.get('content-type'), 'text/plain')
        self.assertEqual(
            content, 'this\nwhere\nwhence\nthat\nwhy\nand the other')

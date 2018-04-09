# -*- coding: utf-8 -*-
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from collective.behavior.richpreview.testing import INTEGRATION_TESTING
from plone import api

import json
import unittest


class RichPreviewJsonViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.view = api.content.get_view(
            u'richpreview-json-view', self.portal, self.request)

    def _encrypt(self, value):
        import base64
        import rsa
        pubkey = api.portal.get_registry_record(
            'public_key', interface=IRichPreviewSettings)
        pubkey = rsa.PublicKey.load_pkcs1(pubkey)
        value = rsa.encrypt(value, pubkey)
        return base64.urlsafe_b64encode(value)

    def test_view_no_url(self):
        self.view.publishTraverse(self.request, '')
        response = self.view()
        self.assertEqual(response, '')
        self.assertEqual(self.request.RESPONSE.getStatus(), 400)

    def test_view(self):
        url = u'http://www.plone.org'.encode('utf-8')
        self.view.publishTraverse(self.request, self._encrypt(url))

        expected = {
            'image': 'https://plone.org/logo.png',
            'description': '',
            'title': 'Plone CMS: Open Source Content Management',
        }

        response = self.view()
        content_type = response.getHeader('Content-Type')
        body = response.getBody()
        self.assertEqual(content_type, 'application/json')
        self.assertEqual(body, json.dumps(expected))

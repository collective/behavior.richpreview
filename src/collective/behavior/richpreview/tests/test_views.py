# -*- coding: utf-8 -*-
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from collective.behavior.richpreview.testing import INTEGRATION_TESTING
from plone import api

import unittest


class RichPreviewJsonViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.view = api.content.get_view(
            u'richpreview-json-view', self.portal, self.request)

    def encrypt(self, value):
        import base64
        import rsa
        pubkey = api.portal.get_registry_record(
            'public_key', interface=IRichPreviewSettings)
        pubkey = rsa.PublicKey.load_pkcs1(pubkey)
        value = rsa.encrypt(value, pubkey)
        return base64.urlsafe_b64encode(value)

    def traverse(self, path):
        return self.view.publishTraverse(self.request, path)

    def test_view_no_url(self):
        response = self.view()
        self.assertEqual(response, '')
        self.assertEqual(self.request.RESPONSE.getStatus(), 400)

    def test_view(self):
        import json
        expected = {
            'image': 'https://plone.org/logo.png',
            'description': '',
            'title': 'Plone CMS: Open Source Content Management',
        }

        path = self.encrypt('http://www.plone.org/')
        view = self.traverse(path)
        response = view()
        content_type = response.getHeader('Content-Type')
        body = response.getBody()
        self.assertEqual(content_type, 'application/json')
        self.assertEqual(body, json.dumps(expected))

    def test_view_caching_headers(self):
        import time
        path = self.encrypt('http://www.plone.org/')
        view = self.traverse(path)
        response = view()
        cache_control = response.getHeader('Cache-Control')
        self.assertEqual(cache_control, 'public')
        expires = response.getHeader('Expires')
        expires = time.strptime(expires, '%a, %d %b %Y %H:%M:%S GMT')
        self.assertGreater(expires, time.time())

    def test_view_invalid_url(self):
        from zope.publisher.interfaces import NotFound
        with self.assertRaises(NotFound):
            self.traverse('foo')

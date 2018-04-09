# -*- coding: utf-8 -*-
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from collective.behavior.richpreview.testing import INTEGRATION_TESTING
from collective.behavior.richpreview.transform import RichPreviewTransform
from plone import api
from plone.app.testing import logout

import lxml
import unittest


HTML = u"""<html>
  <body>
    <div id="content">
      <a href="{url}">foo</a>
    </div>
  </body>
</html>
"""


class TransformerTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        request = self.layer['request']
        request.response.setHeader('Content-Type', 'text/html')
        self.transformer = RichPreviewTransform(None, request)

    def _decrypt(self, value):
        import base64
        import rsa
        value = base64.urlsafe_b64decode(value)
        privkey = api.portal.get_registry_record(
            'private_key', interface=IRichPreviewSettings)
        privkey = rsa.PrivateKey.load_pkcs1(privkey)
        return rsa.decrypt(value, privkey)

    def test_transformer_anonymous_user(self):
        logout()
        url = 'https://plone.org/'
        html = HTML.format(url=url)
        result = self.transformer.transformIterable(html, 'utf-8')
        a = result.tree.xpath('//a')[0]
        self.assertEqual(a.attrib['href'], url)
        self.assertIn('data-richpreview', a.attrib)
        href = self._decrypt(a.attrib['data-richpreview'])
        self.assertIn(href, url)

    def test_transformer_authenticated_user_disabled(self):
        api.portal.set_registry_record(
            'enable', interface=IRichPreviewSettings, value=False)
        logout()
        url = 'https://plone.org/'
        html = HTML.format(url=url)
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertIsNone(result)

    def test_transformer_empty_href(self):
        logout()
        url = ''
        html = HTML.format(url=url)
        result = self.transformer.transformIterable(html, 'utf-8')
        a = result.tree.xpath('//a')[0]
        self.assertEqual(a.attrib['href'], url)
        self.assertNotIn('data-richpreview', a.attrib)

    def test_richpreview_a_no_href(self):
        element = lxml.html.fromstring('<a>foo</a>')
        # the transformer returns None (skip element)
        self.assertIsNone(self.transformer._richpreview(element))

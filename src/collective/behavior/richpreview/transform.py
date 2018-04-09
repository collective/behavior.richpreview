# -*- coding: utf-8 -*-
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from collective.behavior.richpreview.logger import logger
from lxml import etree
from plone import api
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zope.interface import implementer

import base64
import rsa


@implementer(ITransform)
class RichPreviewTransform(object):
    """Transform a response to add an attribute containing the URL of
    an anchor encripted.
    """

    order = 8888

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def _parse(self, result):
        """Create an XMLSerializer from an HTML string, if needed."""
        content_type = self.request.response.getHeader('Content-Type')
        if not content_type or not content_type.startswith('text/html'):
            return

        try:
            return getHTMLSerializer(result)
        except (AttributeError, TypeError, etree.ParseError):
            return

    def _encript(self, url):
        """Process <a> tags for rich preview by adding a
        `data-richpreview` attribute with a `data-src`.

        :param element: the HTML node to be processed
        :type element: instance of lxml.html.HtmlElement
        :returns: the URL of the iframe to be lazy loaded
        :rtype: str
        """
        pubkey = api.portal.get_registry_record(
            'public_key', interface=IRichPreviewSettings, default='')
        try:
            pubkey = rsa.PublicKey.load_pkcs1(pubkey)
            return rsa.encrypt(url, pubkey)
        except ValueError:
            return None

    def _richpreview(self, element):
        """Add a 'data-richpreview' attribute to an <a> element
        containing the href encrypted.
        """
        assert element.tag == 'a'
        href = element.attrib.get('href', None)
        # having an <a> with no href attribute is valid
        if not href:
            return  # nothing to do

        encrypted = self._encript(href)
        encrypted = base64.b64encode(encrypted)
        element.attrib['data-richpreview'] = encrypted
        logger.debug('href: "{0}"; encrypted: "{1}"'.format(href, encrypted))

    def transformBytes(self, result, encoding):
        return

    def transformUnicode(self, result, encoding):
        return

    def transformIterable(self, result, encoding):
        name = IRichPreviewSettings.__identifier__ + '.enable'
        enabled = api.portal.get_registry_record(name, default=False)
        if not (api.user.is_anonymous() and enabled):
            return  # apply the transform to anonymous users only

        result = self._parse(result)
        if result is None:
            return

        path = '//*[@id="content"]//a'  # look for all anchors inside the content area
        for el in result.tree.xpath(path):
            self._richpreview(el)

        return result

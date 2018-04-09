# -*- coding: utf-8 -*-
from collective.behavior.richpreview.behaviors import IRichPreview
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from collective.behavior.richpreview.logger import logger
from lxml import etree
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from requests.exceptions import RequestException
from zope.interface import implementer
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse

import base64
import json
import requests
import rsa


TIMEOUT = 5


@implementer(IPublishTraverse)
class RichPreviewJsonView(BrowserView):
    """Helper view to return page metadata in JSON format."""

    url = None

    def get_meta_property(self, name):
        meta = self.html.find('*/meta[@property="' + name + '"]')
        if meta is None:
            return ''
        return meta.attrib.get('content', '')

    def extract_data(self):
        """Extracts metadata from the page."""
        try:
            r = requests.get(url=self.url, timeout=TIMEOUT)
        except RequestException:
            return {}

        if r.status_code != 200:
            return {}

        self.html = etree.HTML(r.content)

        title = self.get_meta_property('og:title')
        description = self.get_meta_property('og:description')
        image = self.get_meta_property('og:image')

        if not all((image, title)):
            return {}

        return {
            'title': title,
            'description': description,
            'image': image,
        }

    def __call__(self):
        if self.url is None:
            self.request.RESPONSE.setStatus(400)
            return ''

        response = self.request.RESPONSE
        response.setHeader('Content-Type', 'application/json')
        return response.setBody(json.dumps(self.extract_data()))

    def publishTraverse(self, request, url):
        """Get the page URL."""
        privkey = api.portal.get_registry_record(
            'private_key', interface=IRichPreviewSettings, default='')
        try:
            url = base64.urlsafe_b64decode(url)
            privkey = rsa.PrivateKey.load_pkcs1(privkey)
            self.url = rsa.decrypt(url, privkey)
        except rsa.pkcs1.DecryptionError:
            msg = 'URL decryption failed: {0} ({1})'.format(self.context, url)
            logger.warn(msg)
        except (TypeError, ValueError):
            pass
        return self


class RichPreviewViewlet(ViewletBase):
    """Viewlet with rich preview templates and settings."""

    @property
    def enabled(self):
        if not IRichPreview.providedBy(self.context):
            return False

        name = IRichPreviewSettings.__identifier__ + '.enable'
        enabled = api.portal.get_registry_record(name, default=False)
        return api.user.is_anonymous() and enabled

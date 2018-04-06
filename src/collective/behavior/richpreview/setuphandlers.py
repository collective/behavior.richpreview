# -*- coding: utf-8 -*-
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from collective.behavior.richpreview.logger import logger
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from zope.component import getUtility
from zope.interface import implementer

import rsa


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Return a list of non-installable profiles."""
        return [
            u'collective.behavior.richpreview:uninstall',
        ]


def generate_key():
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IRichPreviewSettings)  # noqa: P001
    (pubkey, privkey) = rsa.newkeys(1024)
    settings.public_key = pubkey.save_pkcs1()
    settings.private_key = privkey.save_pkcs1()
    logger.info('A pair of cryptographic keys was successfully generated')


def post_install(setup_tool):
    """Post install script."""
    generate_key()

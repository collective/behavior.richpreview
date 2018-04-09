# -*- coding: utf-8 -*-
from collective.behavior.richpreview import _
from plone.autoform import directives as form
from zope import schema
from zope.interface import Interface


class IBrowserLayer(Interface):
    """A layer specific for this add-on product."""


class IRichPreviewSettings(Interface):
    """Schema for the control panel form."""

    enable = schema.Bool(
        title=_(u'Enable Rich Link Previews?'),
        description=_(
            u'Rich Link Previews are only available for Dexterity-based content types.'),
        default=True,
    )

    form.widget('public_key', rows=5)
    public_key = schema.Text(
        title=_(u'Public Key'),
        description=_(
            u'Used to encrypt the URL.'),
    )

    form.widget('private_key', rows=15)
    private_key = schema.Text(
        title=_(u'Private Key'),
        description=_(
            u'Used to decrypt the URL. Never share this key with anyone.'),
    )

    # keys are available to Administrators only
    form.read_permission(
        public_key='cmf.ManagePortal', private_key='cmf.ManagePortal')
    form.write_permission(
        public_key='cmf.ManagePortal', private_key='cmf.ManagePortal')

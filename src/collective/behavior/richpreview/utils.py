# -*- coding: utf-8 -*-
from collective.behavior.richpreview import _
from zope.interface import Invalid

import rsa


def validate_public_key(value):
    """Check if a public key is valid."""
    try:
        rsa.PublicKey.load_pkcs1(value)
    except ValueError:
        raise Invalid(_(u'The public key is not valid'))
    return True


def validate_private_key(value):
    """Check if a private key is valid."""
    try:
        rsa.PrivateKey.load_pkcs1(value)
    except ValueError:
        raise Invalid(_(u'The private key is not valid'))
    return True


def validate_key_pair(data):
    """Check if a key pair is valid."""
    pubkey = rsa.PublicKey.load_pkcs1(data.public_key)
    privkey = rsa.PrivateKey.load_pkcs1(data.private_key)
    try:
        rsa.decrypt(rsa.encrypt('test', pubkey), privkey)
    except rsa.pkcs1.DecryptionError:
        raise Invalid(_(u'Cryptographic keys do not match'))

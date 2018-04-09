# -*- coding: utf-8 -*-
from collective.behavior.richpreview.utils import validate_key_pair
from collective.behavior.richpreview.utils import validate_private_key
from collective.behavior.richpreview.utils import validate_public_key
from zope.interface import Invalid

import unittest


PUBLIC_KEY = """
-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAJb4fHbK1zOquXlskUTtj7zCP6/UH0qqdbPTSgugiCzgwAAQ2QaCEgMQ
bR/zB0QBqWcATg5dk4/38p4SNbd4GJCgtpkbk0do3VlB0J3TljrcWw3uhx2NTIYD
IpONPPEqSbtqwC5sS+1wLYdRaS5sQ3elFiA9INJ4N5bkajBSiJbDAgMBAAE=
-----END RSA PUBLIC KEY-----
"""

PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIICYAIBAAKBgQCW+Hx2ytczqrl5bJFE7Y+8wj+v1B9KqnWz00oLoIgs4MAAENkG
ghIDEG0f8wdEAalnAE4OXZOP9/KeEjW3eBiQoLaZG5NHaN1ZQdCd05Y63FsN7ocd
jUyGAyKTjTzxKkm7asAubEvtcC2HUWkubEN3pRYgPSDSeDeW5GowUoiWwwIDAQAB
AoGALp/vUIC0lbBUN7vf4Xm8un8DTDomr9iVIURPyed6JuICagLKA8iH54pbKVLV
G5unxbfCY41i1UOuGkNlQEzivw3RwTXz3MmORrAxSHhNasMg6i1Ri9gOxeQ8cGUy
zU8moNYHQPKAR8qFQiIdbu2H+aJgn0v51xfZ5qXM1CuO7oECRQCmCcPSmABGCMsO
sPZ7G341I6h/Q0+MVuDy2hrtt0LrDlOt21qQKsPtk3GaqL5TOxd+gGUHwkLHXzw+
FCAlsy0YRSQE7QI9AOjEysjp6BfQYfDulqvRjS4Lac0KzPUNDb67sdgZR/pX/xXk
jWQdh9rhxLlP+5ZpgRdWCgYOpCRHTRnEbwJESJw0msAGPppR0pbo82VOiAaUBTN2
cjT8Irfm1tYx2YFmbr1imXFaRWcZYz0wHk3VNGkJxZ7afT3UpoE+nb4Bln+GBPEC
PAgehSxI7G2YOTJcQCkyIAiRIVmjnM6Xa/lRNrzg9N/Inf83f68UUJ7T7TbBkXcH
qxcTSzo23IbfbdMORQJFAI8VpNoTLz5VWUC8MAWnw/pHBYRqjUbjuZ+lEfx1Gkjh
fF2RvylwjCEVnjrXjXH/or3512Tzoe/pEFwhId0ijIHuamIW
-----END RSA PRIVATE KEY-----
"""

PUBLIC_KEY_MISMATCH = """
-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAMGPH7+gSVr6vHJ2u5kAYYGYVLYTvp3e/1cwD8kz8obzBSl+BQrSQg+0
q5aJQjIo/5hK1BNy7hMdidagF/dbtXiVMdKWWIZiXx/GOdFOzk1znnhygxVf8V07
RuvWiWf7yeizXAERcUHuBLUlYIiQmNqT5yiit6T4J60tnin+E8nxAgMBAAE=
-----END RSA PUBLIC KEY-----
"""


class Dummy:
    public_key = None
    private_key = None


class ValidatorsTestCase(unittest.TestCase):

    def test_public_key_validator(self):
        self.assertTrue(validate_public_key(PUBLIC_KEY))
        with self.assertRaises(Invalid):
            validate_public_key('invalid')

    def test_private_key_validator(self):
        self.assertTrue(validate_private_key(PRIVATE_KEY))
        with self.assertRaises(Invalid):
            validate_public_key('invalid')

    def test_key_pair_validator(self):
        data = Dummy()
        data.public_key = PUBLIC_KEY
        data.private_key = PRIVATE_KEY
        self.assertIsNone(validate_key_pair(data))
        data.public_key = PUBLIC_KEY_MISMATCH
        with self.assertRaises(Invalid):
            validate_key_pair(data)

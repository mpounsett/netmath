# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Copyright 2014, Matthew Pounsett <matt@conundrum.com>
# ------------------------------------------------------------
import os
import sys
import unittest

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                )
from netmath import Address, AddressFamily # noqa


class TestIPv4(unittest.TestCase):
    def test_v4_default_mask(self):
        x = Address('192.0.2.190')
        self.assertEqual(x.address_int, 3221226174)
        self.assertEqual(x.address, '192.0.2.190')
        self.assertEqual(x.mask_length, 32)
        self.assertEqual(x.to_network(), '192.0.2.190/32')

    def test_v4_string_mask(self):
        x = Address('192.0.2.190/24')
        self.assertEqual(x.address_int, 3221226174)
        self.assertEqual(x.address, '192.0.2.190')
        self.assertEqual(x.mask_length, 24)
        self.assertEqual(x.to_network(), '192.0.2.0/24')

    def test_v4_int_mask(self):
        x = Address('192.0.2.190', 24)
        self.assertEqual(x.address_int, 3221226174)
        self.assertEqual(x.address, '192.0.2.190')
        self.assertEqual(x.mask_length, 24)
        self.assertEqual(x.to_network(), '192.0.2.0/24')

    def test_v4_override_mask(self):
        x = Address('192.0.2.190', 24)
        self.assertEqual(x.to_network(mask_length=8), '192.0.0.0/8')


class TestIPv6(unittest.TestCase):
    def test_v6_default_mask(self):
        x = Address('2001:DB8:DEAD:BEEF::1')
        self.assertEqual(x.address_int, 42540766480198310862439499904952827905)
        self.assertEqual(x.address, '2001:db8:dead:beef::1')
        self.assertEqual(x.mask_length, 128)
        self.assertEqual(x.to_network(), '2001:db8:dead:beef::1/128')

    def test_v6_string_mask(self):
        x = Address('2001:DB8:DEAD:BEEF::1/64')
        self.assertEqual(x.address_int, 42540766480198310862439499904952827905)
        self.assertEqual(x.address, '2001:db8:dead:beef::1')
        self.assertEqual(x.mask_length, 64)
        self.assertEqual(x.to_network(), '2001:db8:dead:beef::0/64')

    def test_v6_int_mask(self):
        x = Address('2001:DB8:DEAD:BEEF::1', 64)
        self.assertEqual(x.address_int, 42540766480198310862439499904952827905)
        self.assertEqual(x.address, '2001:db8:dead:beef::1')
        self.assertEqual(x.mask_length, 64)
        self.assertEqual(x.to_network(), '2001:db8:dead:beef::0/64')

    def test_v6_override_mask(self):
        x = Address('2001:DB8:DEAD:BEEF::1', 64)
        self.assertEqual(x.to_network(mask_length=48), '2001:db8:dead::0/48')

    def test_v6_tidy(self):
        x = Address('[2001:DB8:DEAD:BEEF:0:0::1]')
        self.assertEqual(x.address_int, 42540766480198310862439499904952827905)
        self.assertEqual(x.address, '2001:db8:dead:beef::1')
        self.assertEqual(x.mask_length, 128)
        self.assertEqual(x.to_network(), '2001:db8:dead:beef::1/128')

    def test_v6_embedded(self):
        x = Address('::ffff:192.168.56.102')
        self.assertEqual(x.address_int, 281473913993318)
        self.assertEqual(x.address, '::ffff:192.168.56.102')
        self.assertEqual(x.mask_length, 128)
        self.assertEqual(x.to_network(), '::ffff:192.168.56.102/128')

    def test_v6_malformed(self):
        with self.assertRaises(ValueError):
            Address('2001:DB8:DEAD:BEEF:0:0:0::1')

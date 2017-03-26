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
from netmath import addr2int, int2addr, addr2net


class TestNetworkMethods(unittest.TestCase):

    def test_addr2int_v4(self):
        self.assertEqual(addr2int('192.0.2.190'), 3221226174)

    def test_int2addr_v4(self):
        self.assertEqual(int2addr(3221226174, 'INET'), '192.0.2.190')

    def test_addr2int_v6(self):
        self.assertEqual(addr2int('2001:DB8:DEAD:BEEF::1'),
                         42540766480198310862439499904952827905)

    def test_int2addr_v6(self):
        self.assertEqual(
            int2addr(42540766480198310862439499904952827905, 'INET6'),
            '2001:DB8:DEAD:BEEF::1'.lower()
        )

    def test_addr2int_v6_embedded(self):
        self.assertEqual(addr2int('::ffff:192.168.56.102'), 281473913993318)

    def test_int2addr_v6_embedded(self):
        self.assertEqual(int2addr(281473913993318, 'INET6'),
                         '::ffff:192.168.56.102')

    def test_addr2net_str_v4(self):
        self.assertEqual(addr2net('192.0.2.190', 28), '192.0.2.176/28')

    def test_addr2net_str_v4_cidr(self):
        self.assertEqual(addr2net('192.0.2.190/28'), '192.0.2.176/28')

    def test_addr2net_str_v6(self):
        self.assertEqual(addr2net('2001:DB8:DEAD:BEEF::1', 48),
                         '2001:db8:dead::0/48')

    def test_addr2net_str_v6_cidr(self):
        self.assertEqual(addr2net('2001:DB8:DEAD:BEEF::1/48'),
                         '2001:db8:dead::0/48')

    def test_addr2net_str_v6_wrapped(self):
        self.assertEqual(addr2net('[2001:DB8:DEAD:BEEF::1]', 48),
                         '[2001:db8:dead::0]/48')

    def test_addr2net_str_v6_wrapped_cidr(self):
        self.assertEqual(addr2net('[2001:DB8:DEAD:BEEF::1]/48'),
                         '[2001:db8:dead::0]/48')

    def test_addr2net_v4_list(self):
        self.assertEqual(addr2net(['192.0.2.190', '192.0.2.250'], 28),
                         ['192.0.2.176/28', '192.0.2.240/28'])

    def test_addr2net_v4_list_cidr(self):
        self.assertEqual(addr2net(['192.0.2.190/28', '192.0.2.250/29']),
                         ['192.0.2.176/28', '192.0.2.248/29'])

    def test_addr2net_str_v6_list(self):
        self.assertEqual(
            addr2net(['2001:DB8:DEAD:BEEF::1', '2001:DB8:BAD:DAD::9'], 48),
            ['2001:db8:dead::0/48', '2001:db8:bad::0/48']
        )

    def test_addr2net_str_v6_list_cidr(self):
        self.assertEqual(
            addr2net(['2001:DB8:DEAD:BEEF::1/48', '2001:DB8:BAD:DAD::9/64']),
            ['2001:db8:dead::0/48', '2001:db8:bad:dad::0/64']
        )

    def test_addr2net_mixed(self):
        self.assertEqual(
            addr2net(['192.0.2.190/28',
                      '192.0.2.10',
                      '[2001:DB8:DEAD:BEEF::1]/48',
                      '2001:DB8:BAD:DAD::9/64',
                      '192.0.2.250/29']),
            ['192.0.2.176/28',
             '192.0.2.10',
             '[2001:db8:dead::0]/48',
             '2001:db8:bad:dad::0/64',
             '192.0.2.248/29']
        )

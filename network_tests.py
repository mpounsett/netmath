import unittest
from network import addr2int, int2addr, addr2net


class TestNetworkMethods(unittest.TestCase):

    def test_addr2int_v4(self):
        assert addr2int('192.0.2.190') == 3221226174

    def test_int2addr_v4(self):
        assert int2addr(3221226174, 'INET') == '192.0.2.190'

    def test_addr2int_v6(self):
        assert addr2int(
            '2001:DB8:DEAD:BEEF::1'
        ) == 42540766480198310862439499904952827905L

    def test_int2addr_v6(self):
        assert int2addr(42540766480198310862439499904952827905L,
                        'INET6') == '2001:DB8:DEAD:BEEF::1'.lower()

    def test_addr2net_str_v4(self):
        assert addr2net('192.0.2.190', 28) == '192.0.2.176/28'

    def test_addr2net_str_v4_cidr(self):
        assert addr2net('192.0.2.190/28') == '192.0.2.176/28'

    def test_addr2net_str_v6(self):
        assert addr2net('2001:DB8:DEAD:BEEF::1', 48) == '2001:db8:dead::0/48'

    def test_addr2net_str_v6_cidr(self):
        assert addr2net('2001:DB8:DEAD:BEEF::1/48') == '2001:db8:dead::0/48'

    def test_addr2net_str_v6_wrapped(self):
        assert addr2net('[2001:DB8:DEAD:BEEF::1]',
                        48) == '[2001:db8:dead::0]/48'

    def test_addr2net_str_v6_wrapped_cidr(self):
        assert addr2net(
            '[2001:DB8:DEAD:BEEF::1]/48') == '[2001:db8:dead::0]/48'

    def test_addr2net_v4_list(self):
        assert addr2net(['192.0.2.190',
                         '192.0.2.250'], 28) == ['192.0.2.176/28',
                                                 '192.0.2.240/28']

    def test_addr2net_v4_list_cidr(self):
        assert addr2net(['192.0.2.190/28',
                         '192.0.2.250/29']) == ['192.0.2.176/28',
                                                '192.0.2.248/29']

    def test_addr2net_str_v6_list(self):
        assert addr2net(['2001:DB8:DEAD:BEEF::1',
                         '2001:DB8:BAD:DAD::9'],
                        48) == ['2001:db8:dead::0/48', '2001:db8:bad::0/48']

    def test_addr2net_str_v6_list_cidr(self):
        assert addr2net(['2001:DB8:DEAD:BEEF::1/48',
                         '2001:DB8:BAD:DAD::9/64']
                        ) == ['2001:db8:dead::0/48', '2001:db8:bad:dad::0/64']

    def test_addr2net_mixed(self):
        assert addr2net(['192.0.2.190/28',
                         '192.0.2.10',
                         '[2001:DB8:DEAD:BEEF::1]/48',
                         '2001:DB8:BAD:DAD::9/64',
                         '192.0.2.250/29']) == ['192.0.2.176/28',
                                                '192.0.2.10',
                                                '[2001:db8:dead::0]/48',
                                                '2001:db8:bad:dad::0/64',
                                                '192.0.2.248/29'
                                                ]

if __name__ == '__main__':
    unittest.main()

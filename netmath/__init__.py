# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Copyright 2014, Matthew Pounsett <matt@conundrum.com>
# ------------------------------------------------------------

"""
Network math helper module.

A native python module for doing common network math operations.  Current
supports conversion of IPv4 and IPv6 literals to CIDR-style notation and back,
as well as conversion to integers for easy sorting.
"""

import re


def addr2int(address):
    """Convert an IPv4 or IPv6 address string literal into its integer form."""
    if ":" in address:
        family = 'INET6'
        size = 128
        bits = 16
        base = 16
        separator = ":"

        # If the address starts with :: then split will break.  Prepend a
        # 0 to the string.
        if address.startswith("::"):
            address = '0' + address
        parts = address.split(separator)

        # IPv4 embedded addresses have fewer octets in their text
        # representation
        segments = 8
        if "." in parts[-1]:
            segments = 7

        # Replace any :: with enough zeros to pad the address to 8 octets
        for (i, _) in enumerate(parts):
            if parts[i] == '':
                parts[i] = '0'
                for _ in range(segments - len(parts)):
                    parts.insert(i, '0')

        # fill any empty fields still remaining with zeros.
        for (i, _) in enumerate(parts):
            if parts[i] == '':
                parts[i] = '0'

        # put it back together so our generic code can deal with the
        # expanded shortcuts
        address = separator.join(parts)

    else:
        family = 'INET'
        size = 32
        bits = 8
        base = 10
        separator = '.'

    parts = address.split(separator)
    new_address = 0
    for (i, _) in enumerate(parts):
        if family == 'INET6' and '.' in parts[i] and new_address >> 48 == 0:
            part = addr2int(parts[i])
        else:
            part = int(parts[i], base) << int(bits * (size / bits - i - 1))

        new_address += part
    return new_address


def int2addr(address, family):
    """
    Convert IP address from integer to its string literal form.

    Accepts an integer and a network family ('INET' or 'INET6') and returns
    the appropriate IPv4 or IPv6 string literal.
    """
    # mapped = embedded = False
    embedded = False
    if family.upper() == 'INET6':
        bit = "{:x}"
        bits = 16
        size = 128
        separator = ":"

        # Check if this is a v4/v6 embedded or mapped address
        # No use for specially handling mapped addresses (yet)
        # if (address >> 32 == 0):
        #     mapped = True
        if address >> 48 == 0:
            embedded = True

    elif family.upper() == 'INET':
        bit = "{:d}"
        bits = 8
        size = 32
        separator = "."
    else:
        raise TypeError("Unknown address family {!r}.".format(family))

    parts = []
    mask = (2 ** bits) - 1
    while size > 0:
        if embedded and size == 32:
            parts.append(int2addr(address & ((2 ** 32) - 1), "INET"))
            size -= 32
        else:
            parts.append(bit.format((address >> (size - bits)) & mask))
            size -= bits
    addr = separator.join(parts)

    if family.upper() == 'INET6':
        addr = re.sub(r'(^0)?:0(:0)*:', '::', addr, 1)

    return addr


def addr2net(address, bits=0):
    """
    Convert string literal address(es) to CIDR-notation.

    Address is either a string or a list of strings.  Each address may be a
    string literal address (undecorated) or a string literal address decorated
    with a CIDR-notation mask length.  If no mask length decorates an address,
    the 'bits' value will be used for its mask length.  Where an address is in
    CIDR notation and 'bits' is specified, the mask length on the address will
    be preferred.

    INET and INET6 families can be mixed in a list of addresses, however
    note that only one 'bits' can be provided, so it's likely you will want
    to specify addresses in CIDR notation in order to mix address
    families.

    INET6 addresses may be enclosed in square brackets, a common notation
    to differentiate them from other data types.

    addr2net() will return the same data type that is passed to it.
    """
    address_out = []
    input_type = type(address)
    if input_type is str:
        address = [address]

    for addr in address:
        if "/" in addr:
            addr, masklen = addr.split("/")
            masklen = int(masklen)
        else:
            masklen = bits
        if masklen == 0:
            address_out.append(addr)
            continue

        if ":" in addr:
            family = 'INET6'
            size = 128
        else:
            family = 'INET'
            size = 32

        if addr.startswith("["):
            wrapped = True
            addr = addr.lstrip('[')
            addr = addr.rstrip(']')
        else:
            wrapped = False

        addr_bits = addr2int(addr)
        mask = (2 ** masklen - 1) << (size - masklen)
        addr = int2addr(addr_bits & mask, family)

        if wrapped:
            addr = "[{addr}]".format(addr=addr)

        address_out.append("{addr}/{mask}".format(addr=addr, mask=masklen))

    if input_type is str:
        return address_out[0]

    return address_out

# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Copyright 2014-2021, Matthew Pounsett <matt@conundrum.com>
# ------------------------------------------------------------

"""
Network math helper module.

A native python module for doing common network math operations.  Current
supports conversion of IPv4 and IPv6 literals to CIDR-style notation and back,
as well as conversion to integers for easy sorting.
"""
import enum
import re
from dataclasses import dataclass, field
from typing import List, Optional


class AddressFamily(enum.Enum):
    """ENUM type for address family."""

    INET = enum.auto()
    INET6 = enum.auto()


@dataclass(order=True, frozen=True)
class Address:
    """An object representing an IP address."""

    address_int: int = field(init=False, repr=False)
    address: str = field(compare=False)
    mask_length: Optional[int] = field(default=None)
    family: AddressFamily = field(init=False, compare=False)

    def __post_init__(self) -> None:
        """
        Do post-init setup of the object.

        This calculates the integer representation of the address,
        then recomputes the string representation in order to standardize
        format.  Mask_length defaults to all-ones if it is not specified.
        """
        object.__setattr__(self, 'family', self._detect_family(self.address))
        if '/' in self.address:
            address, mask_length = self.address.split('/')
            object.__setattr__(self, 'address', address)
            object.__setattr__(self, 'mask_length', int(mask_length))

        object.__setattr__(self, 'address_int',
                           self._address_to_int(self.address))
        object.__setattr__(self, 'address',
                           self._int_to_address(self.address_int, self.family))

        if self.mask_length is None:
            if self.family == AddressFamily.INET:
                mask = 32
            else:
                mask = 128
            object.__setattr__(self, 'mask_length', mask)

    @staticmethod
    def _detect_family(address: str) -> AddressFamily:
        if ":" in address:
            return AddressFamily.INET6
        return AddressFamily.INET

    @staticmethod
    def _refactor_v6(address: str) -> str:
        """Eliminate v6 syntax shortcuts."""
        if address.startswith('['):
            address = address.lstrip('[')
            address = address.rstrip(']')
        if address.startswith('::'):
            address = '0' + address

        parts: List[str] = address.split(":")

        # IPv4 embedded addresses occupy both of the last two octets of the
        # v6 address they're contained in, so the v6 address has fewer segments
        segments = 8
        if '.' in parts[-1]:
            segments = 7

        if len(parts) > segments:
            raise ValueError("IPv6 address has too many octets.")

        # Replace any :: with enough zeros to pad the address to 8 octets
        for (i, _) in enumerate(parts):
            if parts[i] == '':
                for _ in range(segments - len(parts)):
                    parts.insert(i, '0')

        # fill any empty fields still remaining with zeros.
        parts = ['0' if x == '' else x for x in parts]

        return ":".join(parts)

    def _address_to_int(self, address: str) -> int:
        """Convert an IP address string representation into an integer."""
        family = self._detect_family(address)
        if family == AddressFamily.INET:
            size = 32
            bits = 8
            base = 10
            separator = '.'
        else:
            size = 128
            bits = 16
            base = 16
            separator = ':'
            address = self._refactor_v6(address)

        parts: List[str] = address.split(separator)
        address_int = 0
        for (i, _) in enumerate(parts):
            if (family == AddressFamily.INET6 and
                    '.' in parts[i] and
                    address_int >> 48 == 0):
                part = self._address_to_int(parts[i])
            else:
                part = int(parts[i], base) << int(bits * (size / bits - i - 1))

            address_int += part
        return address_int

    def _int_to_address(self, address: int, family: AddressFamily) -> str:
        """
        Convert an integer representation of an IP address to its string form.

        Accepts an integer and a network family of type AddressFamily,
        and returns the appropriate IPv4 or IPv6 string representation.
        """
        embedded = False
        if family == AddressFamily.INET6:
            bit = "{:x}"
            bits = 16
            size = 128
            separator = ":"

            if address >> 48 == 0:
                embedded = True
        else:
            bit = "{:d}"
            bits = 8
            size = 32
            separator = "."

        parts: List[str] = []

        mask = (2 ** bits) - 1
        while size > 0:
            if embedded and size == 32:
                parts.append(self._int_to_address(address & (2 ** 32) - 1,
                             AddressFamily.INET))
                size -= 32
            else:
                parts.append(bit.format((address >> (size - bits)) & mask))
                size -= bits
        address_str = separator.join(parts)

        if family == AddressFamily.INET6:
            address_str = re.sub(r'(^0)?:0(:0)*:', '::', address_str, 1)

        return address_str

    def to_network(self, mask_length=None) -> str:
        """
        Return the covering network in CIDR notation.

        Will return a string describing the covering network, in CIDR
        notation.  If unspecified, the object's default mask_length will be
        used.

        >>> x = Address("192.0.2.9/24")
        >>> x.to_network()
        '192.0.2.0/24'
        >>> x.to_network(mask_length=8)
        '192.0.0.0/8'
        """
        if self.family == AddressFamily.INET:
            size = 32
        else:
            size = 128

        mask_length = (mask_length if mask_length is not None
                       else self.mask_length)
        mask = (2 ** mask_length - 1) << (size - mask_length)
        address = self._int_to_address(self.address_int & mask, self.family)
        return f"{address}/{mask_length}"

"""Antelope concrete primitive types."""

import calendar
import datetime as dt
import re
import struct

from pydantic import BaseModel, Field, StringConstraints, field_validator, model_validator
from typing_extensions import Annotated

from .base import Primitive


class Asset(Primitive):
    """
    Serialize an Asset.

    Serializes an amount (can be a float value) and currency name together.
    Uses Symbol type to serialize precision and name of currency,
    uses Uint64 type to serialize amount.
    Amount and name are separated by one space.
    Example: 50.100000 XPR
    """

    value: str

    def get_name(self):
        """
        Extract the name from a raw Asset string.

        Example: "XPR" from Asset string "99.1000000 XPR"
        """
        stripped_value = self.value.strip()
        return stripped_value.split(" ")[1]

    def get_int_digits(self):
        """
        Extract the integer digits (digits before the decimal).

        From raw Asset string.
        Example: "99" from Asset string "99.1000000 XPR"
        """
        stripped_value = self.value.strip()
        pos = 0
        int_digits = ""

        # Check for negative sign
        if stripped_value[pos] == "-":
            int_digits += "-"
            pos += 1

        # Get amount value
        while pos < len(stripped_value) and stripped_value[pos].isdigit():
            int_digits += stripped_value[pos]
            pos += 1

        return int_digits

    def get_frac_digits(self):
        """
        Extract the decimal digits as integers (digits after the decimal).

        Example: "1000000" from Asset string "99.1000000 XPR"
        """
        stripped_value = self.value.strip()
        if "." in stripped_value:
            pos = stripped_value.index(".") + 1
            frac_digits = ""
            while pos < len(stripped_value) and stripped_value[pos].isdigit():
                frac_digits += stripped_value[pos]
                pos += 1
            return frac_digits
        else:
            return ""

    def get_precision(self):
        """
        Get the precision (number of digits after decimal).

        Example: "7" from Asset string "99.1000000 XPR"
        """
        return len(self.get_frac_digits())

    def __bytes__(self):
        amount = Uint64(int(self.get_int_digits() + self.get_frac_digits()))
        name = self.get_name()
        symbol = Symbol(str(self.get_precision()) + "," + name)

        amount_bytes = bytes(amount)
        symbol_bytes = bytes(symbol)

        return amount_bytes + symbol_bytes

    @classmethod
    def from_bytes(cls, bytes_):
        amount_bytes = bytes_[:8]  # Get first 8 bytes
        amount = struct.unpack("<Q", amount_bytes)[0]  # Unpack amount

        # Get symbol
        symbol = Symbol.from_bytes(bytes_[8:])
        precision, name = symbol.value.split(",")
        precision = int(precision)

        # Reconstruct amount with correct precision
        amount_str = str(amount).zfill(precision + 1)
        integer_part = amount_str[:-precision] if precision != 0 else amount_str
        decimal_part = amount_str[-precision:] if precision != 0 else ""
        value = f"{integer_part}.{decimal_part} {name}" if precision != 0 else f"{integer_part} {name}"
        return cls(value=value)

    @field_validator("value")
    def amount_must_have_one_space(cls, v):
        value_list = str(v).strip().split(" ")
        if len(value_list) != 2:
            msg = f'Input "{v}" must have exactly one space between amount and name.'
            raise ValueError(msg)
        return v

    @field_validator("value")
    def check_for_frac_digit_if_decimal_exists(cls, v):
        stripped_value = v.strip()
        if "." in stripped_value:
            pos = stripped_value.index(".") + 1
            if pos >= len(stripped_value) or not stripped_value[pos].isdigit():
                msg = "Decimal provided but no fractional digits were provided."
                raise ValueError(msg)
        return v

    @field_validator("value")
    def check_if_amount_is_valid(cls, v):
        stripped_value = v.strip()
        try:
            amount = float(stripped_value.split(" ")[0])
        except ValueError:
            raise ValueError(f'Amount "{stripped_value.split(" ")[0]}" is not a valid number.')
        if amount < 0 or amount > 18446744073709551615:
            msg = f'Amount "{amount}" must be between 0 and 2^64 inclusive.'
            raise ValueError(msg)
        return v

    @field_validator("value")
    def check_if_name_is_valid(cls, v):
        stripped_value = v.strip()
        name = stripped_value.split(" ")[1]
        if not re.fullmatch(r"^[A-Z]{1,7}$", name):
            msg = f'Input "{name}" must be A-Z and between 1 to 7 characters.'
            raise ValueError(msg)
        return v


class Bool(Primitive):
    value: bool

    def __bytes__(self):
        return b"\x01" if self.value else b"\x00"

    @classmethod
    def from_bytes(cls, bytes_):
        return cls(value=bool(int(bytes_[:1].hex(), 16)))


class Bytes(Primitive):
    value: bytes

    def __bytes__(self):
        return self.value

    @classmethod
    def from_bytes(cls, bytes_):
        return cls(value=bytes_)


class Int8(Primitive):
    value: Annotated[int, Field(ge=-128, le=127)]

    def __bytes__(self):
        return struct.pack("<b", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<b", bytes_[:1])[0]
        return cls(value=value)


class Int16(Primitive):
    value: Annotated[int, Field(ge=-(2**15), le=2**15 - 1)]

    def __bytes__(self):
        return struct.pack("<h", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<h", bytes_[:2])[0]
        return cls(value=value)


class Int32(Primitive):
    value: Annotated[int, Field(ge=-(2**31), le=2**31 - 1)]

    def __bytes__(self):
        return struct.pack("<i", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<i", bytes_[:4])[0]
        return cls(value=value)


class Int64(Primitive):
    value: Annotated[int, Field(ge=-(2**63), le=2**63 - 1)]

    def __bytes__(self):
        return struct.pack("<q", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<q", bytes_[:8])[0]
        return cls(value=value)


class Float32(Primitive):
    value: float

    def __bytes__(self):
        return struct.pack("<f", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<f", bytes_)[0]
        return cls(value=value)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return bytes(self) == bytes(other)


class Float64(Primitive):
    value: float

    def __bytes__(self):
        return struct.pack("<d", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<d", bytes_)[0]
        return cls(value=value)


class Name(Primitive):
    # Adjusted regex pattern to avoid unsupported look-around assertions
    value: Annotated[str, StringConstraints(
        max_length=13,
        pattern=r"^[\.a-z1-5]{0,13}$"
    )]

    def __eq__(self, other):
        """Equality disregards dots in names."""
        if not isinstance(other, self.__class__):
            return False
        return self.value.replace(".", "") == other.value.replace(".", "")

    @field_validator("value")
    def last_char_restriction(cls, v):
        if len(v) == 13:
            allowed = set("abcdefghijklmnopqrstuvwxyz.")
            if v[-1] not in allowed:
                msg = (
                    "When account name is 13 characters long, last character must be "
                    f'in a-z or ".". "{v[-1]}" found.'
                )
                raise ValueError(msg)
        return v

    def __bytes__(self):
        value_int = self.string_to_uint64(self.value)
        uint64 = Uint64(value=value_int)
        return bytes(uint64)

    @classmethod
    def from_bytes(cls, bytes_):
        uint64 = Uint64.from_bytes(bytes_)
        value_str = cls.uint64_to_string(uint64.value, strip_dots=True)
        return cls(value=value_str)

    @classmethod
    def char_to_symbol(cls, c):
        c = ord(c)
        if ord('a') <= c <= ord('z'):
            return (c - ord('a')) + 6
        if ord('1') <= c <= ord('5'):
            return (c - ord('1')) + 1
        return 0

    @classmethod
    def string_to_uint64(cls, s):
        if len(s) > 13:
            raise ValueError("Invalid string length")
        name = 0
        i = 0
        while i < min(len(s), 12):
            name |= (cls.char_to_symbol(s[i]) & 0x1F) << (64 - 5 * (i + 1))
            i += 1
        if len(s) == 13:
            name |= cls.char_to_symbol(s[12]) & 0x0F
        return name

    @classmethod
    def uint64_to_string(cls, n, strip_dots=False):
        charmap = ".12345abcdefghijklmnopqrstuvwxyz"
        s = bytearray(13 * b".")
        tmp = n
        for i in range(13):
            c = charmap[tmp & (0x0F if i == 0 else 0x1F)]
            s[12 - i] = ord(c)
            tmp >>= 4 if i == 0 else 5

        s = s.decode("utf8")
        if strip_dots:
            s = s.strip(".")
        return s


class String(Primitive):
    value: str

    def __bytes__(self):
        bytes_ = self.value.encode("utf8")
        length = len(bytes_)
        bytes_ = bytes(Varuint32(value=length)) + bytes_
        return bytes_

    @field_validator("value")
    def must_not_contain_multi_utf_char(cls, v):
        if len(v) < len(v.encode("utf8")):
            msg = (
                f'Input "{v}" has a multi-byte UTF character in it, '
                "currently xprpy does not support serialization of "
                "multi-byte UTF characters."
            )
            raise ValueError(msg)
        return v

    @classmethod
    def from_bytes(cls, bytes_):
        size = Varuint32.from_bytes(bytes_)
        start = len(bytes(size))
        string_bytes = bytes_[start : start + size.value]
        value = string_bytes.decode("utf8")
        return cls(value=value)


class Symbol(Primitive):
    """
    Serialize a Symbol.

    Serializes a precision and currency name together.
    Precision is used to indicate how many decimals there are in an Asset type amount.
    Precision and name are separated by a comma.
    Example: 1,XPR
    """

    value: str

    @field_validator("value")
    def name_must_be_of_valid_length(cls, v):
        parts = v.split(",")
        if len(parts) != 2:
            raise ValueError(f'Input "{v}" must contain a single comma separating precision and name.')
        name = parts[1]
        if not re.fullmatch(r"^[A-Z]{1,7}$", name):
            msg = f'Input "{name}" must be A-Z and between 1 to 7 characters.'
            raise ValueError(msg)
        return v

    @field_validator("value")
    def precision_must_be_in_the_valid_range(cls, v):
        precision_str = v.split(",")[0]
        if not precision_str.isdigit():
            raise ValueError(f'Precision "{precision_str}" must be a non-negative integer.')
        precision = int(precision_str)
        if precision < 0 or precision > 16:
            msg = f'Precision "{precision}" must be between 0 and 16 inclusive.'
            raise ValueError(msg)
        return v

    def __bytes__(self):
        precision = int(self.value.split(",")[0])
        precision_bytes_ = struct.pack("<B", (precision & 0xFF))
        name = self.value.split(",")[1]
        name_bytes_ = name.encode("utf8")
        bytes_ = precision_bytes_ + name_bytes_
        leftover_byte_space = len(name_bytes_) + 1
        while leftover_byte_space < 8:
            bytes_ += struct.pack("<B", 0)
            leftover_byte_space += 1
        return bytes_

    @classmethod
    def from_bytes(cls, bytes_):
        precision = bytes_[0]
        name_bytes = bytes_[1:].split(b'\x00', 1)[0]
        name = name_bytes.decode("utf8")
        value = f"{precision},{name}"
        return cls(value=value)


class Uint8(Primitive):
    value: Annotated[int, Field(ge=0, le=255)]  # 2 ** 8 - 1

    def __bytes__(self):
        return struct.pack("<B", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<B", bytes_[:1])[0]
        return cls(value=value)


class Uint16(Primitive):
    value: Annotated[int, Field(ge=0, le=65535)]  # 2 ** 16 - 1

    def __bytes__(self):
        return struct.pack("<H", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<H", bytes_[:2])[0]
        return cls(value=value)


class Uint32(Primitive):
    value: Annotated[int, Field(ge=0, le=4294967295)]  # 2 ** 32 - 1

    def __bytes__(self):
        return struct.pack("<I", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<I", bytes_[:4])[0]
        return cls(value=value)


class Uint64(Primitive):
    value: Annotated[int, Field(ge=0, le=18446744073709551615)]  # 2 ** 64 - 1

    def __bytes__(self):
        return struct.pack("<Q", self.value)

    @classmethod
    def from_bytes(cls, bytes_):
        value = struct.unpack("<Q", bytes_[:8])[0]
        return cls(value=value)


class TimePoint(Primitive):
    """
    Serialize a datetime.

    Max precision is in milliseconds, anything below is rejected.
    Considers UTC time.
    """

    value: dt.datetime

    @field_validator("value")
    def max_precision_is_milliseconds(cls, v):
        if v.microsecond % 1000 != 0:
            msg = "The smallest time unit allowed is milliseconds."
            raise ValueError(msg)
        return v

    def _to_number(self) -> int:
        epoch = dt.datetime(1970, 1, 1, 0, 0, 0)
        since_epoch = self.value - epoch
        n = int(since_epoch.total_seconds() * 1_000_000)
        return n

    @classmethod
    def _from_number(cls, n: int):
        epoch = dt.datetime(1970, 1, 1, 0, 0, 0)
        delta = dt.timedelta(microseconds=n)
        datetime = epoch + delta
        return cls(value=datetime)

    def __bytes__(self):
        n = self._to_number()
        uint64_secs = Uint64(n)
        bytes_ = bytes(uint64_secs)
        return bytes_

    @classmethod
    def from_bytes(cls, bytes_):
        n = Uint64.from_bytes(bytes_).value
        obj = cls._from_number(n)
        return obj


class UnixTimestamp(Primitive):
    """
    Serialize a datetime.

    Precision is in seconds.
    Considers UTC time.
    """

    value: dt.datetime

    @field_validator("value")
    def remove_everything_below_seconds(cls, v):
        new_v = v.replace(microsecond=0)
        return new_v

    def __bytes__(self):
        unix_secs = calendar.timegm(self.value.utctimetuple())
        uint32_secs = Uint32(value=unix_secs)
        bytes_ = bytes(uint32_secs)
        return bytes_

    @classmethod
    def from_bytes(cls, bytes_):
        uint32_secs = Uint32.from_bytes(bytes_)
        datetime = dt.datetime.utcfromtimestamp(uint32_secs.value)
        return cls(value=datetime)


class Varuint32(Primitive):
    value: Annotated[int, Field(ge=0, le=20989371979)]

    def __bytes__(self):
        bytes_ = b""
        val = self.value
        while True:
            b = val & 0x7F
            val >>= 7
            b |= (0x80 if val > 0 else 0x00)
            bytes_ += struct.pack("<B", b)
            if not val:
                break
        return bytes_

    @classmethod
    def from_bytes(cls, bytes_):
        shift = 0
        result = 0
        for i in range(len(bytes_)):
            b = bytes_[i]
            result |= (b & 0x7F) << shift
            shift += 7
            if not (b & 0x80):
                break
        return cls(value=result)


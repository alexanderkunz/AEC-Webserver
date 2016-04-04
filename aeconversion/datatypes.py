import math

# precalculate values
_SQRT2 = math.sqrt(2.0)


def to16dot16(data):
    return round(int.from_bytes(data, byteorder="big") / 65536.0, 2)


def to16dot16_vertex(data):
    return round((int.from_bytes(data, byteorder="big") / 100000.0) * _SQRT2, 2)
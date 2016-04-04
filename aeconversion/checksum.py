
def checksum_calculate(msg):
    """
    Calculates the checksum of a message for validation.
    The algorithm is a xor of the string representing the hex of the byte object.
    The start, stop and checksum bytes must not be included!
    """
    crc = 0
    for b in msg:
        crc ^= b
    return crc
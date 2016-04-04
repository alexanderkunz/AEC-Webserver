from .request import AeConvRequest
from .response import AeConvResponse


def aeconvcmd_parse(msg):
    """
    Automatically detects the type of the message and parses it.
    """
    request = int.from_bytes(msg[0:2], byteorder="big") < 1005
    return aeconvcmd_parse_request(msg) if request else aeconvcmd_parse_response(msg)


def aeconvcmd_parse_request(msg):
    """
    Parse an aeconversion request to an AeConvRequest object. Don't include start and stop bytes.
    msg should be a bytes object.
    """

    device_adress = int.from_bytes(msg[0:2], byteorder="big")
    message_id = int.from_bytes(msg[2:4], byteorder="big")
    data = msg[4:-1]
    checksum = msg[-1]

    return AeConvRequest(msg, device_adress=device_adress, message_id=message_id, data=data, checksum=checksum)


def aeconvcmd_parse_response(msg):
    """
    Parse an aeconversion response to an AeConvResponse object. Don't include start and stop bytes.
    msg should be a bytes object.
    """

    message_id = int.from_bytes(msg[0:2], byteorder="big")
    data = msg[2:-1]
    checksum = msg[-1]

    return AeConvResponse(msg, message_id=message_id, data=data, checksum=checksum)
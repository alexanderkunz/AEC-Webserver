from binascii import unhexlify
from aeconversion import aeconvcmd_parse, aeconvcmd_parse_response, aeconvcmd_parse_request

if __name__ == "__main__":
    print("Testing Script for aeconversion protocol libary.")

    print("\nParsing Request: 03A603FD5B")
    print(aeconvcmd_parse_request(unhexlify("03A603FD5B")))

    print("\nParsing Request: 00E603F015")
    print(aeconvcmd_parse_request(unhexlify("00E603F015")))

    print("\nParsing Response: 27170023AAE000BC1913EF")
    print(aeconvcmd_parse_response(unhexlify("27170023AAE000BC1913EF")))

    print("\nParsing AutoDetect: 03A703ED4A")
    print(aeconvcmd_parse(unhexlify("03A703ED4A")))

    print("\nParsing AutoDetect: 03A703ED4A")
    print(aeconvcmd_parse(unhexlify("27170023AAE000BC1913EF")))
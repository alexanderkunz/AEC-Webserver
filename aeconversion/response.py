from .checksum import checksum_calculate
from .message import Message


class AeConvResponse:

    def __init__(self, msg, message_id, data, checksum):
        self.message = Message.get_by_id(message_id)
        if self.message is None:
            print("Couldn't find: " + str(message_id))
        self.data = data
        self.checksum = checksum
        self.valid = checksum_calculate(msg[:-1]) == checksum
        self.data_parsed = None if not self.valid or self.message is None else self.message.try_parse_data(data)

    def __str__(self):
        return "AeConvResponse(message={}, data={}, data_parsed={}, checksum={}, valid={})".format(
            self.message, str(self.data), str(self.data_parsed), self.checksum, self.valid
        )
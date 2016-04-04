from .checksum import checksum_calculate
from .message import Message


class AeConvRequest:

    def __init__(self, msg, device_adress, message_id, data, checksum):
        self.device_adress = device_adress
        self.message = Message.get_by_id(message_id)
        self.data = data
        self.checksum = checksum
        self.valid = checksum_calculate(msg[:-1]) == checksum
        self.data_parsed = None if not self.valid or self.message is None else self.message.try_parse_data(data)

    def __str__(self):
        return "AeConvRequest(device_adress={}, message={}, data={}, data_parsed={} checksum={}, valid={})".format(
            self.device_adress, self.message, str(self.data), str(self.data_parsed), self.checksum, self.valid
        )
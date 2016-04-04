from .datatypes import to16dot16, to16dot16_vertex


class Message:

    _MESSAGES_BY_ID = {}
    _MESSAGES_BY_NAME = {}

    def __init__(self, name, id, request, parse_func=None):
        self.name = name
        self.id = id
        self.request = request
        self.parse_func = parse_func

    def __str__(self):
        return "Message(name={}, id={}, type={})".format(
            self.name, self.id, "Request" if self.request else "Response"
        )

    def is_request(self):
        return self.request

    def is_response(self):
        return not self.request

    @staticmethod
    def append_to_dict(msg):
        Message._MESSAGES_BY_ID[msg.id] = msg
        Message._MESSAGES_BY_NAME[msg.name] = msg
        return msg

    @staticmethod
    def get_by_id(msg_id):
        try:
            return Message._MESSAGES_BY_ID[msg_id]
        except KeyError:
            return None

    @staticmethod
    def get_by_name(msg_name):
        try:
            return Message._MESSAGES_BY_NAME[msg_name]
        except KeyError:
            return None

    def try_parse_data(self, data):
        return None if self.parse_func is None else self.parse_func(data)

# Parse functions
###############################################################################


def parse_performance_response(data):
    if len(data) != 8:
        return None
    ac_performance_watts = to16dot16(data[0:4])
    energy_total_kj = to16dot16(data[4:8])

    # filter invalid overflow data
    # insanely high values are received when the sensors measure negative values
    if ac_performance_watts > 2000:
        return None
    return {
        "ac_performance_watts": (ac_performance_watts, "W"),
        "energy_total_kj": (energy_total_kj, "KJ")
    }


def parse_device_data_response(data):
    try:
        roof_amplitude_ac_voltage = to16dot16(data[0:4])
        roof_amplitude_ac_current = to16dot16_vertex(data[4:8])
        pv_current = to16dot16(data[8:12])
        pv_dc_input_voltage = to16dot16(data[12:16])
        performance_ac = to16dot16(data[16:20])
        performance_dc = to16dot16(data[20:24])
        temperature = to16dot16(data[24:28])
        dc_on_i_ac = to16dot16_vertex(data[28:32])
        return {
            "roof_amplitude_ac_voltage": (roof_amplitude_ac_voltage, "V"),
            "roof_amplitude_ac_current": (roof_amplitude_ac_current, "A"),
            "pv_current": (pv_current, "A"),
            "pv_dc_input_voltage": (pv_dc_input_voltage, "V"),
            "performance_ac": (performance_ac, "W"),
            "performance_dc": (performance_dc, "W"),
            "temperature": (temperature, "°C"),
            "dc_on_i_ac": (dc_on_i_ac, "%")
        }
    except:
        return None


# Message database
###############################################################################

# device data
Message.append_to_dict(Message("DEVICE_DATA_REQUEST", 0x03ED, True))
Message.append_to_dict(Message("DEVICE_DATA_RESPONSE", 0x2712, False, parse_device_data_response))

# country settings
Message.append_to_dict(Message("COUNTRY_SETTINGS_REQUEST", 0x03EF, True))
Message.append_to_dict(Message("COUNTRY_SETTINGS_RESPONSE", 0x03EE, False))

# error status
Message.append_to_dict(Message("ERROR_STATUS_REQUEST", 0x03F0, True))
Message.append_to_dict(Message("ERROR_STATUS_RESPONSE", 0x2713, False))

# device parameters
Message.append_to_dict(Message("DEVICE_PARAMETERS_REQUEST", 0x03F6, True))
Message.append_to_dict(Message("DEVICE_PARAMETERS_RESPONSE", 0x2715, False))

# performance
Message.append_to_dict(Message("PERFORMANCE_REQUEST", 0x3FD, True))
Message.append_to_dict(Message("PERFORMANCE_RESPONSE", 0x2717, False, parse_performance_response))

# device parameters
Message.append_to_dict(Message("DEVICE_PARAMETERS_OFFSET_REQUEST", 0xC746, True))
Message.append_to_dict(Message("DEVICE_PARAMETERS_OFFSET_RESPONSE", 0xEA65, False))

# etc
Message.append_to_dict(Message("PERFORMANCE_REDUCEMENT_RERQUEST", 0x03FE, True))
Message.append_to_dict(Message("OK_RESPONSE", 0x2710, False))
Message.append_to_dict(Message("ERROR_RESPONSE", 0x2711, False))
Message.append_to_dict(Message("ERROR_STORAGE_REQUEST", 0x0406, True))
Message.append_to_dict(Message("SCHUECO_ADDRESS_REQUEST", 0x03F7, True))
import threading
import bottle
from aeconversion import SerialParser
from .dataconnection import DataConnection


class Server(threading.Thread):

    routed = False

    def __init__(self, host, port, debug, serial=0):
        super(Server, self).__init__()
        self.host = host
        self.port = port
        self.debug = debug
        self.serial = serial
        self.data_connection = DataConnection()

        # route
        if not Server.routed:
            Server.routed = True
            bottle.route("/")(self.main)
            bottle.route("/graph.png")(self.performance_graph)

    def main(self):
        bottle.response.content_type = "text/html"
        return """
<!DOCTYPE html>
<html lang="de">
<head>
<title>Solarpanel Statistics</title>
</head>
<meta charset="utf-8"/>
<meta http-equiv="refresh" content="60" />
<body onload="getText(deviceSelect)">

<script language="JavaScript">
var text = new Array()
text[0] = "Please select the device."
""" + self.data_connection.information_get() + """
function getText(slction){
txtSelected = slction.selectedIndex;
document.getElementById('textDiv').innerHTML = text[txtSelected];
}
</script>

<center><table width="100%"><tr>
<td width="480px" align="right" valign="top"><img src="graph.png"></td>

<td align="left" valign="top"><h1>Information</h1>
<select id="deviceSelect" class="body_text" name="information" onchange="getText(this)">
    <option value="Select Device">Select Device</option>
""" + self.data_connection.information_options() + """
</select>
<div id="textDiv"></div>
</td>
</tr></table></center>

</body>
</html>
"""

    def performance_graph(self):
        bottle.response.content_type = "image/png"
        return self.data_connection.graph_get()

    def run(self):
        bottle.run(host=self.host, port=self.port, debug=self.debug)

    def run_parser(self):

        # parse serial messages
        serial_parser = SerialParser(self.serial)
        request = None
        while True:
            msg = serial_parser.read()
            print(str(msg))
            if msg is not None and msg.valid and msg.message is not None:
                if msg.message.is_request():
                    request = msg
                elif request is not None:
                    if msg.message.name == "PERFORMANCE_RESPONSE" and msg.data_parsed is not None:
                        self.data_connection.graph_performance_add_value(
                            request.device_adress,
                            msg.data_parsed["ac_performance_watts"][0])
                    if msg.message.name == "DEVICE_DATA_RESPONSE" and msg.data_parsed is not None:
                        for name in msg.data_parsed.keys():
                            value = str(msg.data_parsed[name][0]) + str(msg.data_parsed[name][1])
                            self.data_connection.information_set(request.device_adress, name, value)
                    request = None
        serial_parser.close()
import threading
import datetime
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
from matplotlib.dates import DateFormatter

class DataConnection():

    def __init__(self):
        self.lock = threading.Lock()

        # init information
        self.information = {}

        # init graph
        self.graph_invalid = True
        self.graph_fig = Figure()
        self.graph_canvas = FigureCanvas(self.graph_fig)
        self.graph_png_output = None

        self.subplots = {}
        self.subplot_values_x = {}
        self.subplot_values_y = {}

        # draw graph
        self.graph_redraw()

    def graph_performance_add_value(self, device_id, value):
        with self.lock:
            try:
                self.subplot_values_x[device_id].append(datetime.datetime.now())
                self.subplot_values_y[device_id].append(value)
                self.graph_invalid = True
            except KeyError:
                self.subplots[device_id] = self.graph_fig.add_subplot(111)
                self.subplot_values_x[device_id] = []
                self.subplot_values_y[device_id] = []
                self.subplot_values_x[device_id].append(datetime.datetime.now())
                self.subplot_values_y[device_id].append(value)
                self.graph_invalid = True

    def graph_redraw(self):
        handles = []
        labels = []
        for key in self.subplots.keys():
            self.subplots[key].xaxis.set_major_formatter(DateFormatter("%H:%M"))
            self.subplots[key].yaxis.set_major_formatter(FormatStrFormatter("%dW"))
            curhandle, = self.subplots[key].plot_date(
                self.subplot_values_x[key], self.subplot_values_y[key],
                "-", label=str(key))
            handles.append(curhandle)
            labels.append(str(key))
        self.graph_fig.legend(handles, labels)
        self.graph_fig.autofmt_xdate()
        self.graph_png_output = BytesIO()
        self.graph_canvas.print_png(self.graph_png_output)
        self.graph_invalid = False

    def graph_get(self):
        if self.graph_invalid:
            self.graph_redraw()
        return self.graph_png_output.getvalue()

    def information_set(self, device_id, key, value):
        try:
            self.information[device_id][key] = value
        except KeyError:
            self.information[device_id] = {key: value}

    def information_get(self):
        if len(self.information) == 0:
            return ""

        html = ""
        num = 0
        for device_id in self.information.keys():
            num += 1
            html += "text[{}]=\"".format(num)
            html += "<h2>Device {id}:<br></h2>".format(id=device_id)
            i = self.information[device_id]
            for key in i.keys():
                html += "{key}: {value}<br>".format(key=key, value=i[key])
            html += "\"\n"
        return html

    def information_options(self):
        html = ""
        for device_id in self.information.keys():
            html += "<option value=\"{value}\">{value}</option>".format(value=device_id)
        return html
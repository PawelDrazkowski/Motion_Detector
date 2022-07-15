from motion_detection import df 
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool

f = figure(width=1000, height=500, title="Motion graph", x_axis_type="datetime")

hover = HoverTool(
    tooltips = [("Start", "@Start{%Y-%m-%d %H:%M:%S.%3N}"), ("End", "@End{%Y-%m-%d %H:%M:%S.%3N}")],
    formatters = {"@Start":"datetime", "@End":"datetime"})
f.add_tools(hover)

f.quad(left="Start", right="End", top=1, bottom=0, color='green', source=df)
output_file("Motion_graph.html")

show(f)
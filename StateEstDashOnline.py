


import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

#our imports:
from data.StateEst_DataFromMessage import ParseDataFromStateEstMessage
from config import BACKGROUND_COLOR , IS_DARK , DASH_THEME , FONT_COLOR, IS_UPDATING_DASH,  DashThemeEnum

''' Map: '''
map_figure = go.Figure()
map_figure.add_trace(
    go.Scatter(
        x=[0,1,3] ,
        y=[5,1,15], 
        name="Estimated Car Position"
    )
)

map_figure.update_layout(
    xaxis_title = "yEast[m]",
    yaxis_title = "xNorth[m]",
    xaxis = dict(range =[-10 , 10]),
    yaxis = dict(range =[0,50])
)


''' Entire Window Layout: '''
app_layout = html.Div(children=[
    # Title:
    html.H1(children='State Estimation'), 
    # sub title:
    html.Div(children='Hello Formula'), 
    # Map graph:
    dcc.Graph(
        id='map',
        figure= map_figure
    )
    # buttons:
]) 


class StateDash():
    def __init__(self):
        self.app =  dash.Dash(__name__)
        self.data = ParseDataFromStateEstMessage()

        
        self.app.layout = app_layout 

    def run(self):
        self.app.run_server(debug=True)




if __name__ == '__main__':
    dash = StateDash()
    dash.run()

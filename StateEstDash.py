

#Plotly and Dash:
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

#our imports:
from data.StateEst_DataFromMessage import ParseDataFromStateEstMessage
from config import BACKGROUND_COLOR , IS_DARK , DASH_THEME , FONT_COLOR, IS_UPDATING_DASH,  DashThemeEnum


#Here you can set the default values of the self updating class: 
class AutoUpdateControl():
    update_interval = 1000 #[msec]
    is_disabled = False  #set true to stop auto update
    index = 0 #will count from 0 until the end of our data


''' Map: '''
map_figure = go.Figure()
map_figure.add_trace(
    go.Scatter(
        x=[0,1,3] ,
        y=[5,1,15], 
        name="Estimated Car Position"
    )
)
map_layout = go.Layout(
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
        animate=True,
        figure=map_figure,
        layout=map_layout
    ),
    dcc.Interval(
        id ='interval-component',
        interval = AutoUpdateControl.update_interval,
        disabled = AutoUpdateControl.is_disabled,
        n_intervals = 0
    )
    # buttons:
]) 


class StateDash():
    def __init__(self):
        self.app =  dash.Dash(__name__)
        self.data = ParseDataFromStateEstMessage()
        self.auto_update_control = AutoUpdateControl()
        
        self.app.layout = app_layout 


        '''Defint our callback: '''
        @self.app.callback(
            #from component with id='map' (our main map)  update the field called 'figure':
            [Output('map', 'figure')],  
            [Input('interval-component' , 'n_intervals')]
        )
        def per_time_interval_callback(interval):
            print(f"{interval:4} intervals have passed")
            self.auto_update_control.index = self.auto_update_control.index  - 1
            print(f"auto_update_control.index = {self.auto_update_control.index}")

            data = plotly.graph_objs.Scatter(
                x=[interval],
                y=[4],
                name='fake-graph',
                mode='lines+markers'
            )
            layout = map_layout
            # return the value of the field called 'figure' fron component with id='map' (our main map) 
            return {'data': data , 'layout': layout }

    def run(self):
        self.app.run_server(debug=True)

    
        


if __name__ == '__main__':
    dash = StateDash()
    dash.run()

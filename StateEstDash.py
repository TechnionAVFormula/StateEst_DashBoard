# Typical
import numpy as np
import array as arr

#Plotly and Dash:
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

#our imports:
from data.StateEst_DataFromMessage import ParseDataFromStateEstMessage



#Here you can set the default values of the self updating class: 
class AutoUpdateControl():
    update_interval = 3*1000 #[msec]
    is_disabled = False  #set true to stop auto update
    index = 0 #will count from 0 until the end of our data


def map_data_scatter_from_car_state(x,y,Vx,Vy,theta):
    data_dict = {
        'x':x,
        'y':y,
        'text': f"car position:  x={x} ,y={y}",
        'mode': 'markers',
        'marker': {
            'size': 15 , 
            'line': {'width': 0.5 , 'color': 'black'}
        },
        'opacity': 0.7,
        #Added:
        'name': 'Car Position',
        'type': 'scatter'           
    }   
    data_scatter = go.Scatter(
        x=list([x]),
        y=list([y]),
        name='Car Position',
        mode= 'markers'
        # mode= 'lines+markers'
    )
    return data_dict , data_scatter


map_layout_go_object = go.Layout(
    xaxis=dict(range=[-60  ,60] ),
    yaxis=dict(range=[-15,15] ),  
    xaxis_title="Temp xLabel",
    yaxis_title="Temp yLabel"
)

map_layout_dict = dict(
        xaxis =dict(title='yEast [m]'),
        yaxis =dict(title='xNorth [m]'),
        margin=dict(l=0,b=0,t=0,r=0),
        legend=dict(x=0,y=0),
        hovermode='closest'
)        


#starting values for map:
map_data , _  = map_data_scatter_from_car_state(0,0,0,0,0)

''' Entire Window Layout: '''
app_layout = html.Div(children=[
    # Title:
    html.H1(children='State Estimation'), 
    # sub title:
    html.Div(children='Hello Formula'), 
    # Map graph:
    dcc.Graph(
        id='map',
        animate=True
    ),
    dcc.Interval(
        id ='interval-component',
        interval = AutoUpdateControl.update_interval,
        disabled = AutoUpdateControl.is_disabled,
        n_intervals = 0
    ),
    #Current index/itteration text:
    html.Div(id='current_index' , children= f"Current Index is  {0:5}" )
    #Current simulation time text:
    # buttons:
]) 


class StateDash():
    def __init__(self):
        # Our data and control over stuff:
        self.data = ParseDataFromStateEstMessage()
        self.auto_update_control = AutoUpdateControl()
        #app stuff:
        self.app =  dash.Dash(__name__)
        self.app.layout = app_layout 
        self.app_server = self.app.server


        '''Defint our callback: '''
        @self.app.callback(
            #from component with id='map' (our main map)  update the field called 'figure':
            Output('map', 'figure'),  
            [Input('interval-component' , 'n_intervals')]
        )
        def per_interval_callback(interval):
            self.print_on_per_interval_callback(interval)
            self.auto_update_control.index = self.auto_update_control.index  + 1
            
            #Values from current moment in time:

            #Getting plotly oriented scatters from data: 
            _ , map_scatter_data = map_data_scatter_from_car_state(interval,2,0,0,0) 

            data = plotly.graph_objs.Scatter(
                x=list([5,interval]),
                y=list([6,7]),
                name='Speed',
                mode= 'lines+markers'
            )

            output_dict = {
                'data': list([data]),
                'layout' : go.Layout(
                    xaxis=dict(range=[-60, 60]),
                    yaxis=dict(range=[-5 , 25]),  
                    xaxis_title="Time[Second]",
                    yaxis_title="speed[KMH]"
                )
            }

            return output_dict

    
    '''Methods: '''
    def print_on_per_interval_callback(self, interval):
        print(f"{interval:5} intervals have passed")

    def run(self):
        self.app.run_server(debug=True)





if __name__ == '__main__':
    dash = StateDash()
    dash.run()

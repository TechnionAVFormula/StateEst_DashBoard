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
    update_interval = 0.05*1000 #[msec]
    is_disabled = False  #set true to stop auto update
    index = 0 #will count from 0 until the end of our data


def current_index_string(index):
    return f"Current index is  {index:5}"

def current_time_string(time_msec):
    return f"Current time is  {time_msec:015} [mili-sec]"


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
    html.Div(id='current_index' , children= current_index_string(0) ),
    #Current simulation time text:
    html.Div(id='current_time' , children= current_time_string(0) ),
    # update interval in mili-sec:
    html.Div(id='update_interval_mili_sec' , children= f"Auto refresh interval is {AutoUpdateControl.update_interval} [mili-sec]")

    # buttons:
]) 



class StateDash():
    def __init__(self):
        # Our data and control over stuff:
        self.data = ParseDataFromStateEstMessage()
        self.auto_update_control = AutoUpdateControl()
        #app stuff:
        self.app =  dash.Dash(__name__)  # The app itself
        self.app.layout = app_layout  #The app's layout
        self.app_server = self.app.server #for debugging


        '''Defint our callbacks: ''' # Callback definition inside class __init__ as this is kind of like a property of our class.

        @self.app.callback(
            #from component with id='map' (our main map)  update the field called 'figure':
            [Output('map', 'figure'),
             Output('current_index' , 'children'),
             Output('current_time'  , 'children')],
            [Input('interval-component' , 'n_intervals')]
        )
        def per_interval_callback(interval):
            # index and itteration info:
            index = self.auto_update_control.index 
            self.act_on_per_interval_callback(interval,index)
            self.auto_update_control.index = self.auto_update_control.index  + 1
            
            #Getting plotly oriented scatters and layout from data at current index: 
            map_go_scatter , map_go_layout = self.map_scatter_and_layout_from_current_data(index) 
            # Get current time:
            current_time = self.data[index]['time']

            '''All output values:'''
            figure_dict = {
                'data'  : [map_go_scatter],
                'layout': map_go_layout
            }
            index_str = current_index_string(index)
            time_str  = current_time_string(current_time)

            #return: map.figure  , current_index.children   , current_time.children
            return   figure_dict , index_str                , time_str
    
    
    '''Methods: '''
    def act_on_per_interval_callback(self, interval , index):
        #reset our running index if app restarted:
        if interval<=0 :
            self.auto_update_control.index = 0
        #print:
        print(f"[interval,index] = [{interval:5},{index:5}]")



    def run(self):
        self.app.run_server(debug=True)

    
    def map_scatter_and_layout_from_current_data(self, index):
        current_data = self.data[index]

        data_scatter = go.Scatter(
            x=list([ current_data['car_state']['x'] ]),
            y=list([ current_data['car_state']['y'] ]),
            name='Car Position',
            mode= 'markers'
            # mode= 'lines+markers'
        )
        map_go_layout  = go.Layout(
            xaxis=dict(range=[-60  ,60] ),
            yaxis=dict(range=[-15,15] ),  
            xaxis_title="yEast [m]",
            yaxis_title="xNorth [m]"
        )
        
        return data_scatter , map_go_layout



if __name__ == '__main__':
    dash = StateDash()
    dash.run()

# Typical
import numpy as np

#Plotly and Dash:
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

#our imports:
from data.StateEst_DataFromMessage import ParseDataFromStateEstMessage


'''Flags and Defines:'''
IS_xNorth_Yeast = True
DEFAULT_STARTING_INDEX = 1000


#Here you can set the default values of the self updating class: 
class AutoUpdateControl():
    update_interval = 0.5*1000 #[msec]
    is_disabled = False  #set true to stop auto update
    DefaultStartingIndex = DEFAULT_STARTING_INDEX
    index = DEFAULT_STARTING_INDEX  #will count from  DEFAULT_STARTING_INDEX  until the end of our data
    


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
    # Interval is the objetc that defines how frequently to AutoUpdate the App:
    dcc.Interval(
        id ='interval-component',
        interval = AutoUpdateControl.update_interval,
        disabled = AutoUpdateControl.is_disabled,
        n_intervals = 0
    ),
    # update interval in mili-sec:
    html.Div(id='update_interval_mili_sec' , children= f"Auto refresh interval is {AutoUpdateControl.update_interval} [mili-sec]"),
    #Current index/itteration text:
    html.Div(id='current_index' , children= current_index_string(0) ),
    #Current simulation time text:
    html.Div(id='current_time' , children= current_time_string(0) )
    
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

        '''
        This is the Auto Update function that runs every [interval] mili-seconds.
        Here we control everything that runs automatically
        '''
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
            map_go_scatters , map_go_layout = self.map_scatter_and_layout_from_current_data(index) 
            # Get current time:
            current_time = self.data[index]['time']

            '''All output values:'''
            figure_dict = {
                'data'  : map_go_scatters,
                'layout': map_go_layout
            }
            index_str = current_index_string(index)
            time_str  = current_time_string(current_time)

            #return: map.figure     , current_index.children   , current_time.children
            return   figure_dict    , index_str                , time_str
    
    
    '''Methods: '''
    def act_on_per_interval_callback(self, interval , index):
        #reset our running index if app restarted:
        if interval<=0 :
            self.auto_update_control.index = AutoUpdateControl.DefaultStartingIndex
        #print:
        print(f"[interval,index] = [{interval:5},{index:5}]")



    def run(self):
        self.app.run_server(debug=True)

    
    def map_scatter_and_layout_from_current_data(self, index):
        current_data = self.data[index]

        x_car = current_data['car_state']['x']
        y_car = current_data['car_state']['y']
        x_car , y_car =flip_x_y(x_car , y_car)   #flip axes if we are in xNorth Yeast Convention

        car_position_scatter = go.Scatter(
            x=list([ x_car  ]),
            y=list([ y_car  ]),
            name='Car Position',
            mode= 'markers'
            # mode= 'lines+markers'
        )
        if IS_xNorth_Yeast:
            x_title = "yEast [m]"
            y_title = "xNorth [m]"
        else:        
            x_title = "xNorth [m]"
            y_title = "yEast [m]"

        map_go_layout  = go.Layout(
            xaxis=dict(range=[-160  ,160] ),
            yaxis=dict(range=[-100,100] ),  
            xaxis_title=x_title,
            yaxis_title=y_title
        )
        # Return Scatters array          ,       map layout
        return [car_position_scatter] , map_go_layout

def flip_x_y(x,y):
    if IS_xNorth_Yeast:
        return y , x
    else:
        return x , y


if __name__ == '__main__':
    dash = StateDash()
    dash.run()

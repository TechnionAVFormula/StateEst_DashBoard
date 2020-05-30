

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from math import exp,tanh
from collections import deque
import dash_table
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Constants:

    ACTUAL_SPEED = "actual_speed"
    DESIRABLE_SPEED = "desirable_speed"
    ACTUAL_STEERING = "actual_steering"
    DESIRABLE_STEERING = "desirable_steering"
    COEFF_A="coeff_A"
    COEFF_B="coeff_B"
    COEFF_C="coeff_C"
    COEFF_D="coeff_D"
    GAS="gas"
    BREAK="break"
    POLYNOMIAL_A_COEFF_a = "polynomial_A_coeef_a"
    POLYNOMIAL_A_COEFF_b = "polynomial_A_coeef_b"
    POLYNOMIAL_A_COEFF_c = "polynomial_A_coeef_c"
    POLYNOMIAL_A_COEFF_d = "polynomial_A_coeef_d"
    POLYNOMIAL_B_COEFF_a = "polynomial_B_coeef_a"
    POLYNOMIAL_B_COEFF_b = "polynomial_B_coeef_b"
    POLYNOMIAL_B_COEFF_c = "polynomial_B_coeef_c"
    POLYNOMIAL_B_COEFF_d = "polynomial_B_coeef_d"
    POLYNOMIAL_C_COEFF_a = "polynomial_C_coeef_a"
    POLYNOMIAL_C_COEFF_b = "polynomial_C_coeef_b"
    POLYNOMIAL_C_COEFF_c = "polynomial_C_coeef_c"
    POLYNOMIAL_C_COEFF_d = "polynomial_C_coeef_d"
    POLYNOMIAL_A = "polynomial_A"
    POLYNOMIAL_B = "polynomial_B"
    POLYNOMIAL_C = "polynomial_C"
    Cones = "cones"
    Cones_X = "cones_x"
    Cones_Y = "cones_y"


#    POLYNOMIAL_B_ = "polynomial_b"
#    POLYNOMIAL_C = "polynomial_c"
    TIME ="time"
    X = "x"
    Y = "y"
    ACCURACY_SPEED = "accuracy_speed"
    ACCURACY_STEERING = "accuracy_steering"

class Dash:

    def __init__(self,state:{}):
        actual_speed = state[Constants.ACTUAL_SPEED]
        desirable_speed = state[Constants.DESIRABLE_SPEED]
        actual_steering = state[Constants.ACTUAL_STEERING]
        gas = state[Constants.GAS]
        breaks= state[Constants.BREAK]
        desirable_steering = state[Constants.DESIRABLE_STEERING]
        polynomial_a = state[Constants.POLYNOMIAL_A]
        polynomial_b = state[Constants.POLYNOMIAL_B]
        polynomial_c = state[Constants.POLYNOMIAL_C]
        polynomial_a_coeef_a =polynomial_a[Constants.COEFF_A]
        polynomial_a_coeef_b=polynomial_a[Constants.COEFF_B]
        polynomial_a_coeef_c=polynomial_a[Constants.COEFF_C]
        polynomial_a_coeef_d=polynomial_a[Constants.COEFF_D]
        polynomial_b_coeef_a = polynomial_b[Constants.COEFF_A]
        polynomial_b_coeef_b = polynomial_b[Constants.COEFF_B]
        polynomial_b_coeef_c = polynomial_b[Constants.COEFF_C]
        polynomial_b_coeef_d = polynomial_b[Constants.COEFF_D]
        polynomial_c_coeef_a = polynomial_c[Constants.COEFF_A]
        polynomial_c_coeef_b = polynomial_c[Constants.COEFF_B]
        polynomial_c_coeef_c = polynomial_c[Constants.COEFF_C]
        polynomial_c_coeef_d = polynomial_c[Constants.COEFF_D]
        cones_x = state[Constants.Cones][Constants.Cones_X]
        cones_y = state[Constants.Cones][Constants.Cones_Y]
        polynomial_b = state[Constants.POLYNOMIAL_B]
        polynomial_c = state[Constants.POLYNOMIAL_C]
        time = state[Constants.TIME]


        x_const =[i for i in range(max(time)+10)]
        self.app = dash.Dash(__name__)

        # SPEED

        self.speed_fig =go.Figure()
        self.speed_fig.add_trace(go.Scatter(x=time,y=actual_speed, name="actual speed"))
        self.speed_fig.add_trace(go.Scatter(x=time,y=desirable_speed, name="desirable speed"))
        self.speed_fig.add_trace(go.Scatter(x=time,y=actual_speed, name="actual speed -kmh"))
        self.speed_fig.add_trace(go.Scatter(x=x_const,y=[30/3.6]*len(x_const),name="30-kmh - 1"))
        self.speed_fig.add_trace(go.Scatter(x=x_const,y=[60/3.6]*len(x_const),name="60-kmh - 2"))

        self.speed_fig.update_layout(
            xaxis_title = "Time[second]",
            yaxis_title = "Speed[meter/second]",
            xaxis = dict(range =[0,max(time)+10]),
            yaxis = dict(range =[0,100/3.6])
        )

        value =lambda mona,machna: tanh(mona/(machna+0.001)) if mona<machna else tanh(machna/(mona+0.001))
        accuracy = lambda mona , machna : [100*abs(value(abs(mona),abs(machna))) for mona, machna in zip(mona, machna)]
        # self.speed_fig_data= go.Figure(
        #     data =[go.Table(header=dict(values=[Constants.TIME,Constants.ACTUAL_SPEED,Constants.DESIRABLE_SPEED,Constants.ACCURACY]),
        #                     cells = dict(values =[
        #                                  time,actual_speed,
        #                                  desirable_speed,
        #                                  accuracy(actual_speed, desirable_speed)]))])
        # STEERING

        self.data= go.Figure(
            data =[go.Table(header=dict(values=[Constants.TIME,Constants.ACTUAL_SPEED,
                                                Constants.DESIRABLE_SPEED,Constants.ACCURACY_SPEED,
                                                Constants.ACTUAL_STEERING,
                                                Constants.DESIRABLE_STEERING,
                                               Constants.ACCURACY_STEERING]),
                            cells = dict(values =[
                                         time,actual_speed,desirable_speed,accuracy(actual_speed, desirable_speed),
                                         actual_steering, desirable_speed, accuracy(actual_steering, desirable_steering),

                            ]))])




        self.steering_fig = go.Figure()
        self.steering_fig.add_trace(go.Scatter(x=time, y= actual_steering, name="actual steering",fillcolor="black"))
        self.steering_fig.add_trace(go.Scatter(x=time, y= desirable_steering, name="desirable steering"))

        self.steering_fig.update_layout(
            xaxis_title = "Time[Second]",
            yaxis_title = "Steering[Degree]",
            xaxis = dict(range=[0, max(time)+10]),
            yaxis = dict(range=[-40, 40])
        )

        # self.steering_fig_data = go.Figure(
        #     data=[go.Table(header=dict(
        #         values=[Constants.TIME, Constants.ACTUAL_STEERING, Constants.DESIRABLE_STEERING, Constants.ACCURACY]),
        #                    cells=dict(values=[
        #                        time, actual_steering,
        #                        desirable_steering,
        #                        accuracy(actual_steering, desirable_steering)]))])




        # functions

        Calculate=lambda A,B,C,D,Y : A*(Y**3)+B*(Y**2)+C*(Y)+D

        Y_range =np.arange(-15,25,0.5)

        #polynomial_a_coeef_a = polynomial_a[Constants.COEFF_A]
        #polynomial_a_coeef_b = polynomial_a[Constants.COEFF_B]
        #polynomial_a_coeef_c = polynomial_a[Constants.COEFF_C]
        #polynomial_a_coeef_d = polynomial_a[Constants.COEFF_D]
        #polynomial_b_coeef_a = polynomial_b[Constants.COEFF_A]
        #polynomial_b_coeef_b = polynomial_b[Constants.COEFF_B]
        #polynomial_b_coeef_c = polynomial_b[Constants.COEFF_C]
        #polynomial_b_coeef_d = polynomial_b[Constants.COEFF_D]
        #polynomial_c_coeef_a = polynomial_c[Constants.COEFF_A]
        #polynomial_c_coeef_b = polynomial_c[Constants.COEFF_B]
        #polynomial_c_coeef_c = polynomial_c[Constants.COEFF_C]
        #polynomial_c_coeef_d = polynomial_c[Constants.COEFF_D]
        X_1_range= [Calculate(polynomial_a_coeef_a,polynomial_a_coeef_b,
                              polynomial_a_coeef_c,polynomial_a_coeef_d,y) for y in Y_range]
        X_2_range = [Calculate(polynomial_b_coeef_a, polynomial_b_coeef_b,
                               polynomial_b_coeef_c, polynomial_b_coeef_d, y) for y in Y_range]
        X_3_range = [Calculate(polynomial_c_coeef_a, polynomial_c_coeef_b,
                               polynomial_c_coeef_c, polynomial_c_coeef_d, y) for y in Y_range]
        self.constrants_fig = go.Figure()




        self.constrants_fig.add_trace(go.Scatter(x=Y_range,
                                                 y=X_1_range,name = "polynomial a"))
        #### Cones
        self.constrants_fig.add_trace(go.Scatter(x=cones_x,
                                                 y=cones_y, name="Cones",mode='markers', marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}}))


        self.constrants_fig.add_trace(go.Scatter(x=Y_range,
                                                     y=X_2_range, name="polynomial b"))
        self.constrants_fig.add_trace(go.Scatter(x=Y_range,
                                                 y=X_3_range, name="polynomial c"))






        ##################print relevant data###############################################33

       # gas = state[Constants.GAS]
       # breaks = state[Constants.BREAK]
        self.relevant_data = go.Figure(
            data=[go.Table(header=dict(values=[Constants.ACTUAL_SPEED+str(" IN KMH"),
                                               Constants.ACCURACY_SPEED+str(" IN %"),
                                               Constants.ACTUAL_STEERING+str(" IN Degrees"),
                                               Constants.ACCURACY_STEERING+str(" IN %"),
                                               Constants.GAS+str(" IN %"),
                                               Constants.BREAK+str(" IN %"),
                                               ],  line_color='darkslategray',fill_color='lightskyblue',),
                           cells=dict(values=[[speed*3.6 for speed  in actual_speed],
                                              [100*(speed * 3.60 /80) for speed in actual_speed],
                                              actual_steering,
                                              [(100 *abs(steering))//22 for steering in actual_steering],
                                              gas,breaks
                           ],  line_color='darkslategray',
                fill_color='lightcyan',) ,name = "relevant data")])

        # self.const_fig_data = go.Figure(
        #     data=[go.Table(header=dict(
        #         values=[Constants.POLYNOMIAL_A+"X",Constants.POLYNOMIAL_A+"Y", Constants.POLYNOMIAL_B+"X",
        #                 Constants.POLYNOMIAL_B+"Y" ,Constants.POLYNOMIAL_C+"X" , Constants.POLYNOMIAL_C+"Y"]),
        #         cells=dict(values=[
        #                        polynomial_a[Constants.X],
        #                        polynomial_a[Constants.Y],
        #                        polynomial_b[Constants.X],
        #                        polynomial_b[Constants.Y],
        #                        polynomial_c[Constants.X],
        #                        polynomial_c[Constants.Y]
        #         ]))])

        self.constrants_fig.update_layout(
            xaxis_title="y value",
            yaxis_title="x value",

            xaxis=dict(range=[-15,25]),
            yaxis=dict(range=[-15,25])
        )

        self.app.layout = html.Div(children=[
            html.H1(children='Control'),

            html.Div(children='''Hello
            '''),
            dcc.Graph(
                id='speed graph',
                figure=self.speed_fig
            ),

            dcc.Graph(
                id='streeing',
                figure=self.steering_fig
            ),
            dcc.Graph(
                id='data streeing',
                figure=self.data

            ),


            dcc.Graph(
                id='constrants',
                figure=self.constrants_fig
            ),

            dcc.Graph(
                id='relevant data',
                figure=self.relevant_data
            ),


            # dcc.Graph(
            #     id ="const fig data",
            #     figure =self.const_fig_data
            # )

        ])



    def run(self):
        self.app.run_server(debug=True)


if __name__ == '__main__':

    dic = {
        Constants.ACTUAL_SPEED:[10,20,20,17],
        Constants.DESIRABLE_SPEED : [12,14,15,20] ,
        Constants.ACTUAL_STEERING :  [0,-5,5,10] ,
        Constants.DESIRABLE_STEERING : [0,-1,2,7 ] ,
        Constants.POLYNOMIAL_A: {
            Constants.COEFF_A:0.1,
            Constants.COEFF_B: 0.1,
            Constants.COEFF_C: 1,
            Constants.COEFF_D: 0.1

        },
        Constants.GAS:[10,20,30,50],
        Constants.BREAK:[1,24,12,57],

        Constants.Cones:{ Constants.Cones_X:[1,2,3,4],
                          Constants.Cones_Y:[2,3,5,7]
        },

        Constants.POLYNOMIAL_B: {
            Constants.COEFF_A: 1,
            Constants.COEFF_B: 2,
            Constants.COEFF_C: 1,
            Constants.COEFF_D: 3

        },
        Constants.POLYNOMIAL_C: {
            Constants.COEFF_A: 1,
            Constants.COEFF_B: 1,
            Constants.COEFF_C: 1,
            Constants.COEFF_D: 1
        },

        Constants.TIME : [6,9,15,20]

    }
    my=Dash(dic)
    my.run()
    print("yes!!!!!")
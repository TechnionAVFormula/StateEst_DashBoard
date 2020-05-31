import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque



class Constants:

    ACTUAL_SPEED = "actual_speed"
    DESIRABLE_SPEED = "desirable_speed"
    ACTUAL_STEERING = "actual_steering"
    DESIRABLE_STEERING = "desirable_steering"
    COEFF_A="coeff_A"
    COEFF_B="coeff_B"
    COEFF_C="coeff_C"
    COEFF_D="coeff_D"
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
    GAS="gas"
    BREAKS="breaks"


#    POLYNOMIAL_B_ = "polynomial_b"
#    POLYNOMIAL_C = "polynomial_c"
    TIME ="time"
    X = "x"
    Y = "y"
    ACCURACY_SPEED = "accuracy_speed"
    ACCURACY_STEERING = "accuracy_steering"


#X = deque(maxlen=20)
#X.append(1)
#Y = deque(maxlen=20)
#Y.append(1)

msgDict={
    Constants.ACTUAL_STEERING,
    Constants.ACTUAL_SPEED,
    Constants.BREAKS,
    Constants.GAS,
    Constants.DESIRABLE_SPEED,
    Constants.DESIRABLE_STEERING,
    Constants.POLYNOMIAL_A,
    Constants.POLYNOMIAL_B,
    Constants.POLYNOMIAL_C,
}

class Dash:

    def __init__(self,state:{}):
        self.i = 0

        actual_speed = state[Constants.ACTUAL_SPEED]
        desirable_speed = state[Constants.DESIRABLE_SPEED]
        actual_steering = state[Constants.ACTUAL_STEERING]
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

        polynomial_b = state[Constants.POLYNOMIAL_B]
        polynomial_c = state[Constants.POLYNOMIAL_C]
        time = state[Constants.TIME]
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(
            [
                dcc.Graph(id='live-graph', animate=True),
                dcc.Interval(
                    id='    ',  
                    interval=1 * 1000
                ),
            ]
        )
        X_time = deque(maxlen=5)
        Y_speed = deque(maxlen=20)


        @self.app.callback(
            Output('live-graph', 'figure'),
            [Input('    ', 'n_intervals')]
        )
        def update_graph_scatter(input_data):
            i = self.i
            X_time.append(i)
            Y_speed.append(i)
            self.i = i+1
            data = plotly.graph_objs.Scatter(
            x=list(X_time),
            y=list(Y_speed),
            name='Speed',
            mode= 'lines+markers')

            output_dict = {
                'data': [data],
                'layout' : go.Layout(
                    xaxis=dict(range=[min(X_time),max(X_time)]),
                    yaxis=dict(range=[min(Y_speed),max(Y_speed)]),  
                    xaxis_title="Time[Second]",
                    yaxis_title="speed[KMH]"
                )
            }

            return output_dict


        self.app.run_server(debug=True)

if __name__ == '__main__':
    dic = {
        Constants.ACTUAL_SPEED: [10, 20, 20, 26],
        Constants.DESIRABLE_SPEED: [12, 14, 15, 20],
        Constants.ACTUAL_STEERING: [0, -5, 5, 10],
        Constants.DESIRABLE_STEERING: [0, -1, 2, 7],
        Constants.POLYNOMIAL_A: {
            Constants.COEFF_A: 0.1,
            Constants.COEFF_B: 0.1,
            Constants.COEFF_C: 1,
            Constants.COEFF_D: 0.1

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

        Constants.TIME: [6, 9, 15, 20]

    }
    my = Dash(dic)
    #my.run()

    #app.run_server(debug=True)
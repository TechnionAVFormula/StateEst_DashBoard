import os, sys, pathlib
currentPath = pathlib.Path( os.path.dirname(__file__) )
relativePath = currentPath.parent
sys.path.append(str(relativePath))

from StateEst_Utils.MessagesClass import messages , NoFormulaMessages
from data.Client import ControlClient

NO_MSG_LIMIT = 150
class ParserObject():

    def __init__(self):
        self._client = ControlClient()
        self._start_client()
        self._message_timeout = 0.0001
        #
        self._data = []
        self._no_msg_counter = 0
        self._is_finish = False


    def _start_client(self):
        print(f"starting client")
        self._client.connect(1)
        self._client.set_read_delay(0.05)
        self._client.start()

    def _process_data( self , formula_state_msg ):
        """unpack data and time:"""
        Data = messages.state_est.FormulaState()
        formula_state_msg.data.Unpack(Data)
        time_in_milisec = formula_state_msg.header.timestamp.ToMilliseconds()

        '''parse data'''
        #time:
        time=time_in_milisec

        # Car State Estimation:
        x  = Data.current_state.position.x
        y  = Data.current_state.position.y
        x_deviation = Data.current_state.position_deviation.x
        y_deviation = Data.current_state.position_deviation.y

        steering_angle = Data.current_state.steering_angle
        steering_angle_deviation = Data.current_state.steering_angle_deviation

        theta = Data.current_state.theta
        theta_deviation = Data.current_state.theta_deviation
        theta_dot = Data.current_state.theta_dot
        theta_dot_deviation = Data.current_state.theta_dot_deviation

        Vx = Data.current_state.velocity.x
        Vy = Data.current_state.velocity.y
        Vx_deviation = Data.current_state.velocity_deviation.x
        Vy_deviation = Data.current_state.velocity_deviation.y

        car_state = {'x' : x , 'y' : y ,  'x_deviation' : x_deviation , 'y_deviation' : y_deviation ,
                     'steering_angle': steering_angle , 'steering_angle_deviation': steering_angle_deviation,
                      'theta': theta , 'theta_deviation': theta_deviation ,
                      'theta_dot':theta_dot , 'theta_dot_deviation': theta_dot_deviation ,
                      'Vx':Vx , 'Vy':Vy , 'Vx_deviation':Vx_deviation , 'Vy_deviation':Vy_deviation} 

        distance_to_finish = Data.distance_to_finish

        #Cones:
        left_cones = []
        for cone in Data.left_bound_cones:
            cone_dict = parse_data_from_cone(cone)
            left_cones.append(cone_dict)

        right_cones = []
        for cone in Data.right_bound_cones:
            cone_dict = parse_data_from_cone(cone)
            right_cones.append(cone_dict)

        # Ground Truth if exist:
        '''save data'''
        current_data_dict = {
                            'time':time , 
                            'car_state':car_state ,
                            'distance_to_finish':distance_to_finish ,
                            'left_cones':left_cones,
                            'right_cones':right_cones 
                            }
        self._data.append(current_data_dict)



    def _act_on_no_msg(self):        
        print(f"no state msg {self._no_msg_counter:03}")
        self._no_msg_counter = self._no_msg_counter + 1
        if self._no_msg_counter > NO_MSG_LIMIT:
            self._is_finish = True
    
    def _parse_messages_one_by_one(self):
        print(f"Parsing Data from Message")
        while not self._is_finish:
            try:
                server_msg = self._client.pop_server_message()
                if server_msg is not None:
                    if server_msg.data.Is(messages.server.ExitMessage.DESCRIPTOR):
                        break
            # except NoFormulaMessages:
            #     pass
            except Exception as e:
                print(f"{e}")

            try:
                formula_state_msg = self._client.get_formula_state_message(timeout= self._message_timeout )
                self._process_data( formula_state_msg )
            except NoFormulaMessages:
                self._act_on_no_msg()
            except Exception as e:
                print(f"{e}")
        
        #when is_finsied        
        return self._data

def ParseDataFromStateEstMessage():
    Parser = ParserObject()
    data = Parser._parse_messages_one_by_one()
    return data

def parse_data_from_cone(cone):
    cone_dict = {
                'angle_from_car':cone.alpha,
                'distance_from_Car':cone.r,
                'id': cone.cone_id ,
                'x' :cone.position.x ,
                'y' :cone.position.y ,
                'position_deviation':cone.position_deviation,
                'type':cone.type
                }
    return cone_dict

if __name__ == "__main__":
    data = ParseDataFromStateEstMessage()
import os, sys, pathlib
currentPath = pathlib.Path( os.path.dirname(__file__) )
relativePath = currentPath.parent
sys.path.append(str(relativePath))

from StateEst_Utils.MessagesClass import messages , NoFormulaMessages
from Client import ControlClient

INPUT_MESSAGE = 'state.messages'


#######################################################################################################################
# Setup
#######################################################################################################################
client = ControlClient()
message_timeout = 0.01


while True:
    try:
        server_msg = client.pop_server_message()
        if server_msg is not None:
            if server_msg.data.Is(messages.server.ExitMessage.DESCRIPTOR):
                break
    except NoFormulaMessages:
        print(f"no server_msg")
    except Exception as e:
        pass

    try:
        formula_state = client.get_formula_state_message(timeout= message_timeout )
        print(formula_state )
    except NoFormulaMessages:
        print(f"no state msg")
    except Exception as e:
        pass


#######################################################################################################################
# Data
#######################################################################################################################

import os, sys, pathlib
currentPath = pathlib.Path( os.path.dirname(__file__) )
relativePath = currentPath.parent
sys.path.append(str(relativePath))


from StateEst_Utils.config import CONFIG  
from StateEst_Utils.ConfigEnum import ConfigEnum

if CONFIG  == ConfigEnum.REAL_TIME or CONFIG == ConfigEnum.COGNATA_SIMULATION:
    from pyFormulaClient import FormulaClient, messages
    from pyFormulaClient.ModuleClient import ModuleClient
    from pyFormulaClient.MessageDeque import MessageDeque
elif CONFIG == ConfigEnum.LOCAL_TEST:
    from pyFormulaClientNoNvidia import FormulaClient, messages
    from pyFormulaClientNoNvidia.ModuleClient import ModuleClient
    from pyFormulaClientNoNvidia.MessageDeque import MessageDeque
else:
    raise NameError('User Should Choose Configuration from config.py')

IN_MESSAGE_FILE = 'state.messages'
OUT_MESSAGE_FILE = 'StateEst_Dash.messages'

class ControlClient(ModuleClient):
    def __init__(self):
        if CONFIG == ConfigEnum.REAL_TIME or CONFIG == ConfigEnum.COGNATA_SIMULATION:
            super().__init__(FormulaClient.ClientSource.CONTROL)
        elif CONFIG == ConfigEnum.LOCAL_TEST:
            super().__init__(FormulaClient.ClientSource.STATE_EST, IN_MESSAGE_FILE, OUT_MESSAGE_FILE)

        self.server_messages = MessageDeque()                                              
        self.formula_state = MessageDeque(maxlen=1)        

    def _callback(self, msg):  
        if msg.data.Is(messages.state_est.FormulaState.DESCRIPTOR):
            self.formula_state.put(msg)
        else:
            self.server_messages.put(msg)

    def get_formula_state_message(self, blocking=True, timeout=None):
        return self.formula_state.get(blocking, timeout)

    def pop_server_message(self, blocking=False, timeout=None):
        return self.server_messages.get(blocking, timeout)
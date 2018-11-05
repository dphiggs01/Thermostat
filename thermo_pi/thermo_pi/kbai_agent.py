from thermo_pi.thermo_util import ThermoUtils
import logging
logger = logging.getLogger()

class Agent:
    RULES_BASE= "rules_base.json"

    def __init__(self):
        self._rules = ThermoUtils.load(Agent.RULES_BASE)

    def predict(self, set_point, sensor_readings):
        ret_val = None
        if sensor_readings['temperature'] < set_point[3]:
            # prediction[0]=burn time, prediction[1]=idle time
            ret_val = (10,3)

        return ret_val


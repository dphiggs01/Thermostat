import datetime
import logging

from thermo_pi.relay import Relay
logger = logging.getLogger()


class Furnace(object):
    CYCLE_ON_MAX = 15
    CYCLE_IDLE_MIN = 3
    BURNER_IDLE = 0
    BURNER_ON = 1
    BURNER_OFF = 2

    def __init__(self):
        self._cycle_idle_duration = 0
        self._cycle_on_time = None
        self._cycle_idle_time = None

    def burner_on_request(self, cycle_on_duration, cycle_idle_duration):
        """
        You will get a burner_on_request when a set point is below the room temp.
        """
        burner_status = self.burner_status_update()
        if burner_status == Furnace.BURNER_OFF:
            self._cycle_idle_duration = cycle_idle_duration
            self._cycle_on_time = self._get_time_plus_duration(cycle_on_duration)
            Relay.on()
            burner_status = Furnace.BURNER_ON

        return burner_status

    def burner_status_update(self):
        """
        check if burner on timer or the idle timer has been reached.
        :return:
        """

        ret_val = None
        current_time = self._get_time()
        if self._cycle_on_time is not None:
            if current_time > self._cycle_on_time:
                self.burner_off_request()
                ret_val = Furnace.BURNER_IDLE
            else:
                ret_val = Furnace.BURNER_ON

        if self._cycle_idle_time is not None:
            if current_time > self._cycle_idle_time:
                self._cycle_idle_time = None
                ret_val = Furnace.BURNER_OFF
            else:
                ret_val = Furnace.BURNER_IDLE

        if self._cycle_on_time is None and self._cycle_idle_time is None:
            ret_val = Furnace.BURNER_OFF

        return ret_val

    def burner_off_request(self):
        """
        You will get a burner off request when the room temperature is reached or
        when the on cycle duration is reached.
        """
        self._cycle_on_time = None
        Relay.off()
        if self._cycle_idle_time is None:  # we have reached room temp during a cycle
            self._cycle_idle_time = self._get_time_plus_duration(self._cycle_idle_duration)
        else:
            pass
        return None

    def _get_time(self):
        return datetime.datetime.now()

    def _get_time_plus_duration(self, duration):
        now = datetime.datetime.now()
        return now + datetime.timedelta(minutes=duration)

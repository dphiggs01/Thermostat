import logging
import datetime
import json

from thermo_pi.thermo_util import ThermoUtils

logger = logging.getLogger()


class Singleton(type):
    """
    Create a single instance of an object
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Scheduler(metaclass=Singleton):
    SCHEDULE_FILE_NM = 'thermostat_schedule.json'
    AWAY_FILE_NM = 'thermostat_away.json'
    WEEK_DAYS = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]

    def __init__(self):
        self._schedule = ThermoUtils.load(Scheduler.SCHEDULE_FILE_NM)
        self._away_schedule = ThermoUtils.load(Scheduler.AWAY_FILE_NM)
        self._active_set_point = (None, None, None, None, None)

    def is_away(self):
        if 'away' in self._away_schedule:
            return True
        else:
            return False

    def get_active_set_point(self):
        return self._active_set_point

    def check_next_set_point(self):
        if self.is_away():
            logging.debug("yup we are away")
            schedule = self._away_schedule
        else:
            logging.debug("no we are not away")
            schedule = self._schedule
        time_tuple = datetime.datetime.today().timetuple()
        season = self.get_season()
        week_day = Scheduler.WEEK_DAYS[time_tuple.tm_wday]
        time_hh_mm = '{:02d}:{:02d}'.format(time_tuple.tm_hour, time_tuple.tm_min)
        # logging.debug(self._schedule[season][week_day])
        # logging.debug(week_day, time_hh_mm)
        keys = sorted(schedule[season][week_day].keys())

        set_point_key = None
        for key in keys:
            if key <= time_hh_mm:
                set_point_key = key

        if set_point_key:
            logging.debug("using tuple one [{}]".format(self.is_away()))
            set_point = (season, week_day, set_point_key, schedule[season][week_day][set_point_key], self.is_away())
        else:
            # It's midnight so start new day with the last set_point temp from the prior day
            logging.debug("using tuple two [{}]".format(self._active_set_point[4]))
            set_point = (season, week_day, "00:00", self._active_set_point[3], self._active_set_point[4])

        if set_point != self._active_set_point:
            self._active_set_point = set_point

        return self._active_set_point

    def set_away(self, away):
        if away == 'True':
            time_stamp = datetime.datetime.now().timestamp()
            time_str = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %I:%M %p')
            self._away_schedule['away'] = time_str
        else:
            if 'away' in self._away_schedule:
                del self._away_schedule['away']
        ThermoUtils.save(Scheduler.AWAY_FILE_NM, self._away_schedule)
        self.check_next_set_point()

    def add_set_point_now(self, temperature):
        time_tuple = datetime.datetime.today().timetuple()
        season = self.get_season()
        day_of_week = Scheduler.WEEK_DAYS[time_tuple.tm_wday]
        time_hh_mm = '{:02d}:{:02d}'.format(time_tuple.tm_hour, time_tuple.tm_min)
        set_point = (season, day_of_week, time_hh_mm, temperature)
        self.add_set_point(set_point)
        self.check_next_set_point()

    def del_set_point(self, set_point):
        season = set_point[0]
        day_of_week = set_point[1]
        time = set_point[2]
        # Expecting that the set_point exists
        try:
            del self._schedule[season][day_of_week][time]
        except KeyError:
            pass

        ThermoUtils.save(Scheduler.SCHEDULE_FILE_NM, self._schedule)

    def mod_set_point(self, set_point):
        self.add_set_point(set_point)

    def add_set_point(self, set_point):
        season = set_point[0]
        day_of_week = set_point[1]
        time = set_point[2]
        temperature = set_point[3]
        self._schedule[season][day_of_week][time] = temperature
        ThermoUtils.save(Scheduler.SCHEDULE_FILE_NM, self._schedule)

    def get_season(self):
        """
        Spring 3/20 - 6/20
        Summer 6/21 - 9/21
        Fall   9/22 - 12/20
        Winter anything else
        """
        spring = range(320, 621)
        summer = range(621, 922)
        fall = range(922, 1221)

        time_tuple = datetime.datetime.today().timetuple()

        month = time_tuple.tm_mon * 100
        day = time_tuple.tm_mday
        month_day = month + day

        if month_day in spring:
            season = 'spring'
        elif month_day in summer:
            season = 'summer'
        elif month_day in fall:
            season = 'fall'
        else:
            season = 'winter'

        return season

    def get_schedule(self):
        schedule = ThermoUtils.load(Scheduler.SCHEDULE_FILE_NM)
        return schedule


if __name__ == "__main__":
    print(datetime.datetime.today().timetuple())
    scheduler1 = Scheduler()
    scheduler2 = Scheduler()
    set_point_t1 = ('fall', 'Sun', '22:59', 90)
    scheduler1.add_set_point(set_point_t1)
    print(json.dumps(scheduler1.get_schedule(), indent=4, sort_keys=True))
    set_point_t2 = ('fall', 'Sun', '22:58', 90)
    scheduler1.del_set_point(set_point_t2)
    print("XXXXXXXXXXXXXX")
    print(json.dumps(scheduler1.get_schedule(), indent=4, sort_keys=True))

import logging
import datetime
import sqlite3


logger = logging.getLogger()

class DataStore:
    SQLITE_FILE = "../config/thermostat_db.sqlite"
    CREATE_DB = """CREATE TABLE thermostat
                    (time_stamp INTEGER, room_temp REAL, target_temp REAL,
                     outside_temp REAL) 
                 """

    def __init__(self):
        self._conn = sqlite3.connect(DataStore.SQLITE_FILE)

    def setup(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute(DataStore.CREATE_DB)
            self._conn.commit()
        except sqlite3.OperationalError as e:
            logging.debug("file already exists error")

    def write_row(self,room_temp,target_temp,outside_temp):
        time_stamp = int(datetime.datetime.now().timestamp())
        try:
            self._conn.execute("INSERT INTO thermostat (time_stamp, room_temp, target_temp, outside_temp) VALUES ({},{},{},{})".format(time_stamp,room_temp,target_temp,outside_temp))
            self._conn.commit()
        except sqlite3.IntegrityError:
            logging.debug('ERROR: ID already exists in PRIMARY KEY column')

    def fetch_rows(self):
        cursor = self._conn.cursor()
        cursor.execute('SELECT * FROM thermostat')
        return cursor.fetchall()


if __name__ == "__main__":
    dataStore = DataStore()
    #dataStore.setup()
    dataStore.write_row(68,72,32)
    print(dataStore.fetch_rows())
    ts = int(datetime.datetime.now().timestamp())
    dt = datetime.datetime.fromtimestamp(ts)
    print(ts)
    print(dt)
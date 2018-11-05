import sys
import json
import os
import logging
import inspect
from thermo_pi.exceptions import JSONFileError

logger = logging.getLogger()

class ThermoUtils:

    @staticmethod
    def load(file_name):
        logger.debug("**************** entering {}.{}".format(ThermoUtils.__class__.__name__, inspect.currentframe().f_code.co_name))

        schedule = None
        not_found = True
        path = sys.path
        path.insert(0, "./config")
        path.insert(1, "../config")
        for x in path:
            resource = os.path.join(x, file_name)
            if os.path.isfile(resource):
                with open(resource, 'r') as file_ptr_r:
                    schedule = json.load(file_ptr_r)
                not_found = False
                break

        if not_found:
            raise JSONFileError('Unable to load json for {}'.format(file_name))

        return schedule

    @staticmethod
    def save(file_name, json_data):
        logger.debug("**************** entering {}.{}".format(ThermoUtils.__class__.__name__, inspect.currentframe().f_code.co_name))
        schedule = None
        not_found = True
        path = sys.path
        path.insert(0, "./config")
        for x in path:
            resource = os.path.join(x, file_name)
            if os.path.isfile(resource):
                with open(resource, 'w') as outfile:
                    json.dump(json_data, outfile, sort_keys = True, indent = 4)
                not_found = False
                break

        if not_found:
            raise JSONFileError('Unable to save json for {}'.format(file_name))

        return schedule

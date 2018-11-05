class Thermostat(Exception):
    """ Common base class for all Thermostat exceptions."""


class JSONFileError(Thermostat):
    """Attempting to a load or save a file but cannot find it or its corrupt.  """

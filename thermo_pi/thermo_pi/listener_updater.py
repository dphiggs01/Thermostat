from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import os
import sys
from thermo_pi.scheduler import Scheduler
from thermo_pi.sensor import TempSensor
from thermo_pi.furnace import Furnace
from thermo_pi.thermo_util import ThermoUtils
from thermo_pi.kbai_agent import Agent

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

_global_call_shadow_update = True
_global_current_temp = 68 # Arbitrary Temp to start

def custom_shadow_callback_delta(payload, response_status, token):
    """
    This callback gets invoked if we get a set_point or away request from the web site.
    :param payload:
    :param response_status:
    :param token:
    :return:
    """
    logging.debug("In custom_shadow_callback_delta response_status={}, token={}".format(response_status, token))
    global _global_call_shadow_update
    _global_call_shadow_update = True
    payload_dict = json.loads(payload)
    logging.debug("payload_dict {}".format(payload_dict))
    if "set_point" in payload_dict["state"]:
        if payload_dict["state"]["set_point"]:
            # global set_point
            set_point_temp = payload_dict["state"]["set_point"]
            scheduler = Scheduler()
            scheduler.add_set_point_now(set_point_temp)
            logging.debug("Updating set point temp to {}".format(set_point_temp))

    if "del_set_point" in payload_dict["state"]:
        if payload_dict["state"]["del_set_point"]:
            del_set_point = payload_dict["state"]["del_set_point"]
            scheduler = Scheduler()
            scheduler.del_set_point(del_set_point)
            logging.debug("delete set point {}".format(del_set_point))

    if "add_set_point" in payload_dict["state"]:
        if payload_dict["state"]["add_set_point"]:
            add_set_point = payload_dict["state"]["add_set_point"]
            scheduler = Scheduler()
            scheduler.del_set_point(add_set_point)
            logging.debug("add set point {}".format(add_set_point))

    if "get_schedule" in payload_dict["state"]:
        # refresh = payload_dict["state"]["refresh"]
        logging.debug("get_schedule called")

    if "away" in payload_dict["state"]:
        away = payload_dict["state"]["away"]
        scheduler = Scheduler()
        scheduler.set_away(away)
        logging.debug("Updating away to [{}]".format(away))

    if "refresh" in payload_dict["state"]:
        logging.debug("Refresh called")

def custom_shadow_callback_update(payload, response_status, token):
    """
    This callback gets invoked when we are sending temperature updates to AWS
    :param payload:
    :param response_status:
    :param token:
    :return:
    """
    logging.debug("In method custom_shadow_callback_update")
    if response_status == "timeout":
        logging.debug("Update request " + token + " time out!")
    if response_status == "accepted":
        # payload_dict = json.loads(payload)
        logging.debug("~~~~~~~~~~~~~~~~~~~~~~~")
        logging.debug("Update request with token: " + token + " accepted!")
        # logging.debug("property: " + str(payload_dict["state"]["desired"]["property"]))
        logging.debug("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if response_status == "rejected":
        logging.debug("Update request " + token + " rejected!")


def custom_shadow_callback_delete(payload, response_status, token):
    """
    This callback gets invoke once at the start of the pi application to refresh the shadow
    and sync with the pi
    :param payload:
    :param response_status:
    :param token:
    :return:
    """
    logging.debug("In method custom_shadow_callback_delete")
    if response_status == "timeout":
        logging.debug("Delete request " + token + " time out!")
    if response_status == "accepted":
        logging.debug("~~~~~~~~~~~~~~~~~~~~~~~")
        logging.debug("Delete request with token: " + token + " accepted!")
        logging.debug("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if response_status == "rejected":
        logging.debug("Delete request " + token + " rejected!")


def get_device_shadow_handler():
    congig_json = ThermoUtils.load("aws_iot_config.json")
    endpoint = congig_json['endpoint']
    root_ca_path = congig_json['rootCAPath']
    certificate_path = congig_json['certificatePath']
    private_key_path = congig_json['privateKeyPath']
    thing_name = congig_json['thingName']
    client_id = congig_json['clientId']

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Init AWSIoTMQTTShadowClient
    mqtt_shadow_client = AWSIoTMQTTShadowClient(client_id)
    mqtt_shadow_client.configureEndpoint(endpoint, 8883)
    mqtt_shadow_client.configureCredentials(root_ca_path, private_key_path, certificate_path)

    # AWSIoTMQTTShadowClient configuration
    mqtt_shadow_client.configureAutoReconnectBackoffTime(1, 32, 20)
    mqtt_shadow_client.configureConnectDisconnectTimeout(10)  # 10 sec
    mqtt_shadow_client.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect to AWS IoT
    mqtt_shadow_client.connect()
    # Create a deviceShadow with persistent subscription
    device_shadow_handler = mqtt_shadow_client.createShadowHandlerWithName(thing_name, True)

    return device_shadow_handler


def main():
    device_shadow_handler = get_device_shadow_handler()

    device_shadow_handler.shadowRegisterDeltaCallback(custom_shadow_callback_delta)

    device_shadow_handler.shadowDelete(custom_shadow_callback_delete, 5)

    agent = Agent()
    furnace = Furnace()
    thermostat = TempSensor()
    scheduler = Scheduler()

    logging.debug('Press Ctrl-C to quit.')
    while True:
        furnace.burner_status_update()
        readings = thermostat.thermostat_readings()
        set_point = scheduler.check_next_set_point()
        prediction = agent.predict(set_point, readings)
        if prediction is not None:
            # prediction[0]=burn time, prediction[1]=idle time
            furnace.burner_on_request(prediction[0], prediction[1])
        else:
            furnace.burner_off_request()

        json_payload = {"state": {"reported": readings}}
        json_payload['state']['reported']['set_point'] = set_point[3]
        json_payload['state']['reported']['away'] = set_point[4]
        logging.debug("json_payload={}".format(json_payload))

        global _global_call_shadow_update
        global _global_current_temp
        last_reading_temp = round(readings['temperature'], 0)
        logging.debug("_global_current_temp {} last_reading_temp".format(_global_current_temp,last_reading_temp))
        if _global_call_shadow_update or _global_current_temp != last_reading_temp:
            logging.debug("calling shadowUpdate")
            device_shadow_handler.shadowUpdate(json.dumps(json_payload), custom_shadow_callback_update, 5)
            _global_current_temp = last_reading_temp
            _global_call_shadow_update = False

        time.sleep(1)


if __name__ == "__main__":
    main()

import boto3
import json
import datetime
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    client = boto3.client('iot-data', region_name='us-east-1')
    refresh = 'False'
    if event and 'refresh' in event:
        refresh = event['refresh']

    if refresh:
        last_refresh = time.time()
        client.publish(
            topic='$aws/things/Thermostat_pi/shadow/update',
            qos=1,
            payload=json.dumps({"state": {"desired": {"last_refresh": last_refresh}}})
        )
        #give the thing time to update
        time.sleep(1.5)

    response = client.get_thing_shadow(thingName='Thermostat_pi')
    streaming_body = response["payload"]
    json_state = json.loads(streaming_body.read().decode('utf-8'))
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json_state
    }

def main():
    response = lambda_handler(None, None)
    print(response)


if __name__ == "__main__":
    main()

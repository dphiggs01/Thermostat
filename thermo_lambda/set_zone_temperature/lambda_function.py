import boto3
import json


def lambda_handler(event, context):
    set_point_temp = 60
    if event and 'set_point' in event:
        set_point_temp = event['set_point']
    client = boto3.client('iot-data', region_name='us-east-1')
    # Change topic, qos and payload
    response = client.publish(
        topic='$aws/things/Thermostat_pi/shadow/update',
        qos=1,
        payload=json.dumps({"state": {"desired": {"set_point": set_point_temp}}})
    )
    return response


def main():
    response = lambda_handler(None, None)
    print(response)


if __name__ == "__main__":
    main()

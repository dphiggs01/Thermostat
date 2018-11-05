import boto3
import json

def lambda_handler(event, context):
    away = False
    if event and 'away' in event:
        away = event['away']
    client = boto3.client('iot-data', region_name='us-east-1')
    # Change topic, qos and payload
    response = client.publish(
        topic='$aws/things/Thermostat_pi/shadow/update',
        qos=1,
        payload=json.dumps({"state": {"desired": {"away": away}}})
    )
    return response



def main():
    response = lambda_handler(None, None)
    print(response)


if __name__ == "__main__":
    main()

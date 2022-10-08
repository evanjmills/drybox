import datetime
import os
from time import sleep

import Adafruit_DHT
from twilio.rest import Client


ACCOUNT_TOKEN = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
GPIO_PIN = 17
RECEIVER_NUMBER = os.environ['RECEIVER_NUMBER']
SENDER_NUMBER = os.environ['SENDER_NUMBER']


def main():
    sensor = Adafruit_DHT.DHT11
    start = None
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_PIN)
        if humidity > 20:
            if start:
                diff = start - datetime.now()
                if diff.days > 2:
                    start = None
                    send_message()
            else:
                start = datetime.now()
        else:
            start = None

        sleep(30)


def send_message():
    client = Client(ACCOUNT_TOKEN, AUTH_TOKEN)
    client.message.create(
        body="The drybox storing your filliment is getting to be too humid. You may need to bake the silica packets to reduce the humidity.",
        from_=SENDER_NUMBER,
        to=RECEIVER_NUMBER,
    )


if __name__ == '__main__':
    main()
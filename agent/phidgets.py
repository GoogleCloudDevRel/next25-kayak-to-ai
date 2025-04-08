from Phidget22.Devices.DigitalInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import time
import json
import os

PHIDGET_ENABLED = os.environ.get("PHIDGET_ENABLED",0)

# load locations
with open("locations.json", "r") as file:
    locations = json.load(file)

def find_location(location_id:int):
    for l in locations:
        if l['location_id'] == location_id:
            return l
    
    raise ValueError(f"PhidgetController: location {location_id} not found")

def control_light(target_location_id: int):
    """
    Controls an LED connected to a Phidget VINT Hub.
    """

    location = find_location(target_location_id)
    
    LED_PORT = location["location_id"]

    if PHIDGET_ENABLED == 1:
        try:
            # Create your Phidget channels
            digitalOutput0 = DigitalOutput()
            digitalOutput0.setHubPort(0)
            digitalOutput0.setChannel(LED_PORT)
            digitalOutput0.openWaitForAttachment(5000)

            # Do stuff with your Phidgets here or in your event handlers.
            digitalOutput0.setDutyCycle(1)
            print("open")
            time.sleep(10)
            digitalOutput0.setDutyCycle(0)
            time.sleep(1)
            print("closed")
            digitalOutput0.close()

        except PhidgetException as e:
            print(f"Phidget Exception {e.code}: {e.details}")
            print(f"Exiting....")
            exit(1)
        except RuntimeError as e:
            print(f"Runtime Exception: {e}")
            print(f"Exiting....")
            exit(1)
    else:
        pass


if __name__ == "__main__":
    control_light(target_location="daniels_broiler")

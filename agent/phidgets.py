from Phidget22.Devices.DigitalOutput import *
from Phidget22.Net import *
import time
import json

# Replace with your VINT Hub's IP address or hostname if using a network connection
# If using a USB connection, leave this as None
HUB_IP_ADDRESS = None  # Example: "192.168.1.100"

# Replace with the serial number of your VINT Hub (optional, but recommended)
HUB_SERIAL_NUMBER = None  # Example: 654321

# load locations
with open('locations.json','r') as file:
    locations = json.load(file)

# Replace with the port number where your LED is connected
LED_PORT = 0

def control_light(location:str):
    """
    Controls an LED connected to a Phidget VINT Hub.
    """

    for location in locations:
        LED_PORT = location["location_id"]

    try:
        # Create a DigitalOutput object
        led = DigitalOutput()

        # Set the hub connection parameters if using a network connection
        if HUB_IP_ADDRESS:
            Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)
            led.setHubPort(LED_PORT)
            led.setDeviceSerialNumber(HUB_SERIAL_NUMBER)
            led.setHub(HUB_IP_ADDRESS)
        else:
            led.setHubPort(LED_PORT)
            if HUB_SERIAL_NUMBER:
                led.setDeviceSerialNumber(HUB_SERIAL_NUMBER)

        # Open the LED connection
        led.openWaitForAttachment(5000)  # Wait up to 5 seconds for connection

        print("LED connected successfully!")

        # Turn the LED on
        print("Turning LED on...")
        led.setDutyCycle(1)  # Set duty cycle to 1 (full on)
        time.sleep(2)  # Keep the LED on for 2 seconds

        # Turn the LED off
        print("Turning LED off...")
        led.setDutyCycle(0)  # Set duty cycle to 0 (off)
        time.sleep(2)  # Keep the LED off for 2 seconds

        # Close the connection
        led.close()
        print("LED connection closed.")

    except PhidgetException as e:
        print(f"Phidget Exception {e.code}: {e.details}")
        print(f"Exiting....")
        exit(1)
    except RuntimeError as e:
        print(f"Runtime Exception: {e}")
        print(f"Exiting....")
        exit(1)

if __name__ == "__main__":
    control_light()

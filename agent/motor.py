import pyfirmata2
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
# Modem Controller port for Arduino (modify for mac or Pi)
port = os.environ.get("ARDUINO_BOARD")

# Pin Mapping
dirYPin = 6
stepYPin = 3
dirXPin = 5
stepXPin = 2
enPin = 8
brakePin = 7

# High / Low controls
HIGH = True
LOW = False

# Define home location and distance per turn / duration for X vs Y controls

# load locations
with open('locations.json','r') as file:
    locations = json.load(file)

def reset_motor(location:str):
    pass


def move_motor(target_location:str):
    
    for l in locations:
        if l['location'] == target_location:
            location = l
        else:
            raise ValueError('location not found')

    # check current location:
    with open('current_location','r') as file:
        current_location = file.read()
    
    if location != current_location and current_location == 'reset':
        pass
    elif location == current_location:
        pass
    elif location != current_location and current_location != 'reset':
        reset_motor(location)

    # Instantiate motor
    board = pyfirmata2.Arduino(port)
    
    # d = digital, 13 = pin number, o = output

    enPin = board.get_pin(f'd:{enPin}:o')
    brakePin = board.get_pin(f'd:{brakePin}:o')
    dirYPin = board.get_pin(f'd:{dirYPin}:o')
    stepYPin = board.get_pin(f'd:{stepXPin}:o')
    dirXPin = board.get_pin(f'd:{dirXPin}:o')
    stepXPin = board.get_pin(f'd:{stepXPin}:o')
    print('Board Instantiated')

    # Prepare to move
    enPin.write(HIGH)
    time.sleep(.1)
    brakePin.write(HIGH)
    time.sleep(.1)
    print('Ready to move')
        
    # get the entry from path_maps
    for step in location['steps']:
        if step['dir'] == 'Y+':
            dirYPin.write(HIGH) # Left motor mount
            for i in range(step['duration']):
                stepYPin.write(HIGH)
                time.sleep(0.000005)
                stepYPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'Y-':
            dirYPin.write(LOW) # Left motor mount
            for i in range(step['duration']):
                stepYPin.write(HIGH)
                time.sleep(0.000005)
                stepYPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'X+':
            dirXPin.write(LOW) # RIGHT (bottom motor mount)
            for i in range(step['duration']):
                stepXPin.write(HIGH)
                time.sleep(0.000005)
                stepXPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'X-':
            dirXPin.write(HIGH) # LEFT (bottom motor mount)
            for i in range(step['duration']):
                stepXPin.write(HIGH)
                time.sleep(0.000005)
                stepXPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        else:
            raise ValueError('valid direction not found')
    
    print('Move Complete')

    # Lock location
    brakePin.write(LOW)
    time.sleep(.1)
    enPin.write(LOW)
    time.sleep(.1)
    print('Locked')

    # write current location
    with open('current_location','w') as file:
       file.write(location)
        

    board.exit()

# Reset controller should:
# instantiate the board
# get the current location
# perform the steps in reverse with opposite polarity
# confirm reset



if __name__ == "__main__":
    
    move_motor(location="daniels_broiler")


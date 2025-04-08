import pyfirmata2
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
# Modem Controller port for Arduino (modify for mac or Pi)
port = os.environ.get("ARDUINO_BOARD")

# Pin Mapping
def_dirYPin = 6
def_stepYPin = 3
def_dirXPin = 5
def_stepXPin = 2
def_enPin = 8
def_brakePin = 7

# High / Low controls
HIGH = True
LOW = False

# Define home location and distance per turn / duration for X vs Y controls

# load locations
with open('locations.json','r') as file:
    locations = json.load(file)

def find_location(location:str):
    for l in locations:
        if l['location'] == location:
            return l
    
    raise ValueError(f"location {location} not found")

def reset_motor(current_location:str):
    print('resetting')
    location = find_location(current_location)

    # Instantiate motor
    board = pyfirmata2.Arduino(port)
    
    # d = digital, 13 = pin number, o = output

    enPin = board.get_pin(f'd:{def_enPin}:o')
    brakePin = board.get_pin(f'd:{def_brakePin}:o')
    dirYPin = board.get_pin(f'd:{def_dirYPin}:o')
    stepYPin = board.get_pin(f'd:{def_stepYPin}:o')
    dirXPin = board.get_pin(f'd:{def_dirXPin}:o')
    stepXPin = board.get_pin(f'd:{def_stepXPin}:o')
    print('Board Instantiated')
        
    # Prepare to move
    enPin.write(HIGH)
    time.sleep(.1)
    brakePin.write(HIGH)
    time.sleep(.1)
    print('Ready to move')

    # get the entry from path_maps
    for step in reversed(location['steps']):
        print(step)
        if step['dir'] == 'Y+': 
            dirYPin.write(HIGH) # Left motor mount # reverse from y+ LOW
            print ('run Y+')
            for i in range(step['duration']):
                stepYPin.write(HIGH)
                time.sleep(0.000005)
                stepYPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'Y-':           
            dirYPin.write(LOW) # Left motor mount # reverse from y- HIGH
            print('run Y-')
            for i in range(step['duration']):
                stepYPin.write(HIGH)
                time.sleep(0.000005)
                stepYPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'X-':
            dirXPin.write(LOW) # RIGHT (bottom motor mount) # reverse from X- HIGH
            print ('run X-')
            for i in range(step['duration']):
                stepXPin.write(HIGH)
                time.sleep(0.000005)
                stepXPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'X+':
            dirXPin.write(HIGH) # LEFT (bottom motor mount) # reverse from X+ low
            print ('run X+')
            for i in range(step['duration']):
                stepXPin.write(HIGH)
                time.sleep(0.000005)
                stepXPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        else:
            raise ValueError('valid direction not found')
    
    print('Reset Complete')

    # Lock location
    brakePin.write(LOW)
    time.sleep(.1)
    enPin.write(LOW)
    time.sleep(.1)
    print('Locked')

    # write current location
    with open('current_location','w') as file:
       file.write(location['location'])
        

    board.exit()



def move_motor(target_location:str):
    
    location = find_location(target_location)

    # check current location:
    try:
        with open('current_location','r') as file:
            current_location = file.read()
    except FileNotFoundError:
        current_location = 'reset'
        

    if location['location'] == current_location:
        return  f"Kayak stayed at {location['location']}"
    elif location['location'] != current_location and current_location != 'reset':
        reset_motor(location)
    elif location['location'] != current_location and current_location == 'reset':
        print('continue to move')
        pass
    else:
        raise KeyError('unknown move handler')
        

    # Instantiate motor
    board = pyfirmata2.Arduino(port)
    
    # d = digital, 13 = pin number, o = output

    enPin = board.get_pin(f'd:{def_enPin}:o')
    brakePin = board.get_pin(f'd:{def_brakePin}:o')
    dirYPin = board.get_pin(f'd:{def_dirYPin}:o')
    stepYPin = board.get_pin(f'd:{def_stepYPin}:o')
    dirXPin = board.get_pin(f'd:{def_dirXPin}:o')
    stepXPin = board.get_pin(f'd:{def_stepXPin}:o')
    print('Board Instantiated')

    # Prepare to move
    enPin.write(HIGH)
    time.sleep(.1)
    brakePin.write(HIGH)
    time.sleep(.1)
    print('Ready to move')
        
    # get the entry from path_maps
    for step in location['steps']:
        print(step)
        if step['dir'] == 'Y+':
            dirYPin.write(LOW) # Left motor mount
            print ('run Y+')
            for i in range(step['duration']):
                stepYPin.write(HIGH)
                time.sleep(0.000005)
                stepYPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'Y-':           
            dirYPin.write(HIGH) # Left motor mount
            print('run Y-')
            for i in range(step['duration']):
                stepYPin.write(HIGH)
                time.sleep(0.000005)
                stepYPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'X-':
            dirXPin.write(HIGH) # RIGHT (bottom motor mount)
            print ('run X-')
            for i in range(step['duration']):
                stepXPin.write(HIGH)
                time.sleep(0.000005)
                stepXPin.write(LOW)
                time.sleep(0.000005)
            time.sleep(.1)
        elif step['dir'] == 'X+':
            dirXPin.write(LOW) # LEFT (bottom motor mount)
            print ('run X+')
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
       file.write(location['location'])
        

    board.exit()

    return f"Kayak Moved to {location['location']}"


if __name__ == "__main__":
    
    move_motor(target_location="daniels_broiler")


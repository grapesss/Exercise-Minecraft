# Requirements for this to work:
# ToggleWalk https://www.curseforge.com/minecraft/mc-mods/togglewalk
# Turn on the option to toggle sprint

import RPi.GPIO as GPIO # Python package to control the Raspberry Pi GPIO
from pynput import keyboard, mouse # Python package to control the keyboard and mouse
from datetime import datetime, timedelta # Python package to keep track of time
from keyboard import Key, Controller # To control the keyboard

mouse = mouse.Controller # Control the mouse with Python
keyboard = keyboard.Controller # Control the keyboard with Python
wheel = 17 # THe GPIO that is going to be used to keep track of the wheel speed
move_right = Button(22) # Control for moving right in the game
move_left = Button(23) # Control for moving left in the game
jump = Button(24) # Control for jumping in the game
inventory = Button(25) # Button for opening your invenotry in the game
walk_toggled = False
sprint_toggled = False

wheel_circumference = 111.53 # Circumference of my exercise machine wheel


def detect_wheel(): # Probably will not use this
    wheel_rotations = 0
    measure_time = datetime.now() + timedelta(seconds=0.25)
    while datetime.now() < measure_time: # This loop will detect how many times the wheel goes around every 
        if GPIO.input(wheel) == GPIO.HIGH: # quarter of a second
            wheel_rotations += 1

    total_inches = wheel_circumference * wheel_rotations # Inches traveled in quarter of a second
    total_feet = total_inches / 12 # Inches to feet
    total_miles = total_feet / 5280 # Feet to miles
    
def find_mph():
	start_time = datetime.now()
	while True: # This loop runs forever until it is broken
		if GPIO.input(wheel) == GPIO.HIGH:
			break # If the wheel finishes a rotation, break out of the
			# while loop
		if start_time - datetime.now() > 2:
			return 0
			
	time_between = start_time - datetime.now() # Time between when it started and now
	miles_per_hour = 5.68 * wheel_circumference / time_between
	# 5.68 * circumference / the time for one rotation is the Miles Per Hour
	return miles_per_hour
    

while True:
    mph = find_mph()

    if mph < 3: 
        keyboard.press('w')
        keyboard.release('w') 
        walk_toggled = True
    else:
        keyboard.press(Key.control)
        keyboard.release(Key.control)
        sprint_toggled = True
        
    if mph = 0:
		if walk_toggled: # Untoggle walk
			keyboard.press('w')
			keyboard.release('w')
			
		if sprint_toggled: # Untoggle sprint
			keyboard.press(Key.control)
			keyboard.release(Key.control)

# Requirements for this to work:
# ToggleWalk https://www.curseforge.com/minecraft/mc-mods/togglewalk
# Turn on the option to toggle sprint

import RPi.GPIO as GPIO # Python package to control the Raspberry Pi GPIO
from pynput import keyboard, mouse # Python package to control the keyboard and mouse
from datetime import datetime, timedelta # Python package to keep track of time
from keyboard import Key, Controller # To control the keyboard
import serial_with_arduino
import socket


mouse = mouse.Controller # Control the mouse with Python
keyboard = keyboard.Controller # Control the keyboard with Python
wheel = 2 # These are the GPIOs that are going to be matched with each control
attack = 3
right_click = 4 # In Minecraft, right click interacts with everything
move_right = 14 # These move the player
move_left = 15
inventory = 18 # Opens inventory | If double clicked, it will open the escape menu to exit or modify settings
hotbar = 17 # Scrolls through the hotbar
jump = 27 # When clicked once, it will jump. If clicked twice, it will drop an item
walk_backwards = 22

send_press_mode = False # If this is set to false, the keys will be pressed on the Pi
# If this is set to true, the keys will be sent to the laptop to be pressed

HOST = '127.0.0.1'
PORT = 25657

GPIO.setup(wheel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(attack, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_click, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(move_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(move_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(inventory, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(hotbar, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jump, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(walk_backwards, GPIO.IN, pull_up_down=GPIO.PUD_UP)

setupSerial(115200, "/dev/ttyACM0")
waitForArduino()

walk_toggled = False
sprint_toggled = False

wheel_circumference = 111.53 # Circumference of my exercise machine wheel

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

if not send_press_mode:
    while True:
        mph = find_mph()
        joystick_state = recvLikeArduino()
        joystickXY = joystick_state.split(',') # Splits the X and Y coordinates string into two different intergers: x and y

        if mph < 3:
            keyboard.press('w')
            keyboard.release('w')
            walk_toggled = True
        else:
            keyboard.press(Key.control)
            keyboard.release(Key.control)
            sprint_toggled = True

        if mph == 0:
            if walk_toggled: # Untoggle walk
                keyboard.press('w')
                keyboard.release('w')

            if sprint_toggled: # Untoggle sprint
                keyboard.press(Key.control)
                keyboard.release(Key.control)
        # Joystick
        if joystickXY[0] != 1 and joystickXY[1] != 1: # The farther you move away from the middle of the joystick, the higher speed the mouse goes
            if joystickXY[0] <= 128:
                mouse.move(5, 0)
            if joystickXY[1] <= 128:
                mouse.move(0, 5)

            if joystickXY[0] > 128 and joystickXY[0] <= 384:
                mouse.move(10, 0)
            if joystickXY[1] > 128 and joystickXY[1] <= 384:
                mouse.move(0, 10)
            if joystickXY[0] > 384:
                mouse.move(20, 0)
            if joystickXY[1] > 384:
                mouse.move(0, 20)

        if GPIO.input(attack) == GPIO.HIGH: # Attack button pressed
            mouse.click(mouse.Button.left)

        if GPIO.input(right_click) == GPIO.HIGH: # Interact button pressed
            mouse.click(mouse.Button.right)

        if GPIO.input(move_right) == GPIO.HIGH: # If move right button is pressed
            keyboard.press('d')
            keyboard.release('d')

        if GPIO.input(move_left) == GPIO.HIGH: # if move left button is pressed
            keyboard.press('a')
            keyboard.release('a')

        if GPIO.input(inventory) == GPIO.HIGH: # If inventory button is pressed | If double-pressed, will open esacpe menu
            inven_start_time = datetime.now()
            keyboard.press('e')
            if inven_start_time - datetime.now() <= 0.5:
                keyboard.press(keyboard.Key.escape)
                keyboard.release(keyboard.Key.escape)

        if GPIO.input(hotbar) == GPIO.HIGH: # Will scroll through items to the right
            mouse.scroll(0, 1)

        if GPIO.input(jump) == GPIO.HIGH: # Will make player jump | If double clicked, player drops an item
            jump_start_time = datetime.now()
            keyboard.press(keyboard.Key.space)
            keyboard.release(keyboard.Key.space)
            if jump_start_time - datetime.now() <= 0.5:
                keyboard.press('q')
                keyboard.release('q')


# This will send the right keypresses to another computer.
# That other computer will then actually press the keys.
# That way, I will get better Minecraft performance.
# This can be turned off by setting send_press_mode to False

# As of when this comment is here, this code is unfinished and unusable.
# I will finish it soon
# else:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM):
#         s.bind((HOST, PORT))
#         s.listen()
# 
#         conn, addr = s.accept()
#         with conn:
#             data = conn.recv(2048)
# 
#             if not data:
#                 break
# 
#             print("Connected to", addr)
#             while True:
#                 mph = find_mph()
#                 joystick_state = recvLikeArduino()
#                 joystickXY = joystick_state.split(',') # Splits the X and Y coordinates string into two different intergers: x and y
# 
#                 if mph < 3:
#                     conn.sendall('w'.encode('utf-8'))
#                     walk_toggled = True
#                 else:
#                     conn.sendall('ctrl'.encode('utf-8'))
#                     sprint_toggled = True
# 
#                 if mph == 0:
#                     if walk_toggled: # Untoggle walk
#                         conn.sendall('w'.encode('utf-8'))
#                     if sprint_toggled: # Untoggle sprint
#                         conn.sendall('ctrl'.encode('utf-8'))
#                 # Joystick
#                 if joystickXY[0] != 1 and joystickXY[1] != 1: # The farther you move away from the middle of the joystick, the higher speed the mouse goes
#                     if joystickXY[0] <= 128:
#                         # mouse.move(5, 0)
#                         msg = "move1"
#                         conn.sendall(msg.encode('utf-8'))
#                     if joystickXY[1] <= 128:
#                         # mouse.move(0, 5)
#                         msg = "move2"
#                         conn.sendall(msg.encode('utf-8'))
# 
#                     if joystickXY[0] > 128 and joystickXY[0] <= 384:
#                         # mouse.move(10, 0)
#                     if joystickXY[1] > 128 and joystickXY[1] <= 384:
#                         mouse.move(0, 10)
#                     if joystickXY[0] > 384:
#                         mouse.move(20, 0)
#                     if joystickXY[1] > 384:
#                         mouse.move(0, 20)
# 
#                 if GPIO.input(attack) == GPIO.HIGH: # Attack button pressed
#                     mouse.click(mouse.Button.left)
# 
#                 if GPIO.input(right_click) == GPIO.HIGH: # Interact button pressed
#                     mouse.click(mouse.Button.right)
# 
#                 if GPIO.input(move_right) == GPIO.HIGH: # If move right button is pressed
#                     keyboard.press('d')
#                     keyboard.release('d')
# 
#                 if GPIO.input(move_left) == GPIO.HIGH: # if move left button is pressed
#                     keyboard.press('a')
#                     keyboard.release('a')
# 
#                 if GPIO.input(inventory) == GPIO.HIGH: # If inventory button is pressed | If double-pressed, will open esacpe menu
#                     inven_start_time = datetime.now()
#                     keyboard.press('e')
#                     if inven_start_time - datetime.now() <= 0.5:
#                         keyboard.press(keyboard.Key.escape)
#                         keyboard.release(keyboard.Key.escape)
# 
#                 if GPIO.input(hotbar) == GPIO.HIGH: # Will scroll through items to the right
#                     mouse.scroll(0, 1)
# 
#                 if GPIO.input(jump) == GPIO.HIGH: # Will make player jump | If double clicked, player drops an item
#                     jump_start_time = datetime.now()
#                     keyboard.press(keyboard.Key.space)
#                     keyboard.release(keyboard.Key.space)
#                     if jump_start_time - datetime.now() <= 0.5:
#                         keyboard.press('q')
#                         keyboard.release('q')
# 

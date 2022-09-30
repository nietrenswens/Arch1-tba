import keyboard
import sys
import time
import random

def slow_type(t):
    speed = 100
    for l in t:
        rand = random.random()
        if not keyboard.is_pressed('space'):
            time.sleep(rand*10.0/speed)
        sys.stdout.write(l)
        sys.stdout.flush()

def clear():
    print("\033c", end="")
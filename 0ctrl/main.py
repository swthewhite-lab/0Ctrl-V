from wheel import zeroctrlwheel
import joystick
import time

import joystick

if __name__ == "__main__":
    joystick.read_joystick() 


wheel = zeroctrlwheel()

wheel.move(0.3,0.3)
time.sleep(0.5)
wheel.stop





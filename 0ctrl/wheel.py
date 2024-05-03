from jetbot import Robot
import time

class zeroctrlwheel:
    def __init__(self):
        self.robot = Robot()

    def stop(self):
        self.robot.stop()

    def move(self, leftSpeed, rightSpeed):
        self.robot.left_motor.value = leftSpeed
        self.robot.right_motor.value = rightSpeed

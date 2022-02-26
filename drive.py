"""
this module provides drive functionality for create
"""
from kipr import *
from time import time, sleep


def drive(l_speed: int, r_speed: int):
    """Drives left and right motor for values between -100 to 100"""
    create_drive_direct(int((r_speed * -5) * 0.95), l_speed * -5)


def drive_one():
    """Drives left and right motor for values between -100 to 100"""
    create_drive_direct(-125, -150)


def stop():
    """Stops robot"""
    create_stop()


def drive_timed(l_speed: int, r_speed: int, time: int):
    """Drives left and right for time milliseconds and motor values between -100 and 100"""
    drive(l_speed, r_speed)
    msleep(time)
    stop()


def drive_distance_straight(speed: int, distance: int):
    z = gyro_z()
    end_time = time() + int ((distance*25.4 / speed/5))
    r_speed = l_speed = speed
    #drive_one()
    while time() < end_time:
        msleep(100)
        drive(l_speed, r_speed)
        if gyro_z() - z > 10:
            r_speed += 1
            l_speed -= 1
        elif gyro_z() - z < -10:
            l_speed += 1
            r_speed -= 1

    #msleep(time)
    stop()


"""
this module provides drive functionality for create
"""
from kipr import *
from time import time, sleep
import constants as c

GYRO_OFFSET = 0


def drive(l_speed: int, r_speed: int):
    """Drives left and right motor for values between -100 to 100"""
    create_drive_direct(int((r_speed * -5) * c.ADJUST_SPEED), l_speed * -5)


def stop():
    """Stops robot"""
    create_stop()


def drive_timed(l_speed: int, r_speed: int, drive_time: int):
    """Drives left and right for time milliseconds and motor values between -100 and 100"""
    drive(l_speed, r_speed)
    msleep(drive_time)
    stop()


def calibrate_gyro():
    global GYRO_OFFSET
    total = 0
    for _ in range(100):
        total += gyro_z()
        msleep(10)
    GYRO_OFFSET = total / 100


def calibrated_gyro_z():
    return gyro_z() - GYRO_OFFSET


def drive_distance_straight(speed: int, distance: int):
    end_time = time() + abs(int(distance * 25.4 / speed / 5))
    r_speed = l_speed = speed
    while time() < end_time:
        msleep(100)
        drive(l_speed, r_speed)
        if calibrated_gyro_z() > 10:
            r_speed += 1
            l_speed -= 1
        elif calibrated_gyro_z() < -10:
            l_speed += 1
            r_speed -= 1
    stop()


def left_pivot(speed, drive_time):
    drive(0, speed)
    msleep(drive_time)
    stop()


def right_pivot(speed, drive_time):
    drive(speed, 0)
    msleep(drive_time)
    stop()


def spin(speed, drive_time):
    drive(speed, -speed)
    msleep(drive_time)
    stop()

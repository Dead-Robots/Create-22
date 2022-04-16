"""
this module provides drive functionality for create
"""
import math
from kipr import *
from time import time, sleep
import constants as c
from createserial.createCommands import create_dd, Encoders
from sensors import read_cliffs

GYRO_OFFSET = 0


def drive(l_speed: int, r_speed: int):
    """Drives left and right motor for values between -100 to 100"""
    create_dd(r_speed * -5, (int(l_speed * -5 * c.ADJUST_SPEED)))


def stop():
    """Stops robot"""
    drive(0, 0)


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


def drive_distance_straight(speed: int, distance):
    end_time = time() + abs(distance * 25.4 / speed / 5)
    print("drive time: ", abs(distance * 25.4 / speed / 5))
    r_speed = l_speed = speed

    while time() < end_time:
        msleep(10)
        drive(l_speed, r_speed)
        if calibrated_gyro_z() > 10:
            r_speed += 3
            l_speed -= 1
        elif calibrated_gyro_z() < -10:
            r_speed -= 3
            l_speed += 1
        else:
            r_speed = l_speed = speed
    stop()


def drive_distance_straight_2(speed: int, distance):
    end_time = time() + abs(distance * 25.4 / speed / 5)
    print("drive time: ", abs(distance * 25.4 / speed / 5))
    r_speed = l_speed = speed
    tot_offset = 0
    while time() < end_time:
        tot_offset += calibrated_gyro_z()
        drive(l_speed, r_speed)
        if tot_offset > 10:
            r_speed += 1
            l_speed -= 1
        elif tot_offset < -10:
            l_speed += 1
            r_speed -= 1
        else:
            r_speed = l_speed = speed
        msleep(10)
    stop()


def left_pivot(speed, drive_time):
    drive(0, speed)
    msleep(drive_time)
    stop()


def right_pivot(speed, drive_time):
    drive(speed, 0)
    msleep(drive_time)
    stop()


def pivot(speed, angle, stationary_wheel):
    arc_length = 2 * (angle * 9.25 * math.pi) / 360
    encoders = Encoders()
    left, right = encoders.values
    r_speed = l_speed = speed * 5
    inches = 0
    while abs(inches) < abs(arc_length):
        msleep(15)
        left, right = encoders.values
        if stationary_wheel == "left":
            inches = (right * (math.pi * 72 / 508.8) / 24.5)
            create_dd(0, r_speed)
        else:
            inches = (left * (math.pi * 72 / 508.8) / 24.5)
            create_dd(l_speed, 0)
        print("in loop", left, right, inches, l_speed, r_speed, arc_length)
    drive(0, 0)


def spin(speed, angle):
    arc_length = (angle * 9 * math.pi) / 360
    encoders = Encoders()
    left, right = encoders.values
    r_speed = l_speed = speed * 5
    inches = 0
    while abs(inches) < abs(arc_length):
        msleep(15)
        left, right = encoders.values
        inches = abs(right) * ((math.pi * 72 / 508.8) / 24.5) # + (abs(left) * (math.pi * 72 / 508.8) / 24.5)
        create_dd(-l_speed, r_speed)
        print("in loop", left, right, inches, l_speed, r_speed, arc_length)
    drive(0, 0)


def drive_until_black(speed):
    drive(speed, speed)
    rCliff, lCliff = read_cliffs()
    while rCliff > 1000 and lCliff > 1000:
        rCliff, lCliff = read_cliffs()
    drive(0, 0)


# encoder values to inches: n * (math.pi * 72 / 508.8) / 24.5 where n equals encoder values

def drive_straight(distance, speed):
    p = 0.25
    i = 0.05
    encoders = Encoders()
    left, right = encoders.values
    old_left, old_right = left, right
    r_speed = l_speed = speed * 5
    inches = 0
    create_dd(l_speed, r_speed)
    while abs(inches) < abs(distance):
        msleep(15)
        left, right = encoders.values
        inches = 0.5 * ((right * (math.pi * 72 / 508.8) / 24.5) + (left * (math.pi * 72 / 508.8) / 24.5))
        p_error = (right - old_right) - (left - old_left)  # short term
        i_error = right - left  # long term
        r_speed -= int(p * p_error + i * i_error)
        l_speed += int(p * p_error + i * i_error)
        create_dd(l_speed, r_speed)
        old_left = left
        old_right = right
        print("in loop", left, right, inches, l_speed, r_speed)
    drive(0, 0)

"""
this module provides drive functionality for create
"""
import math
from kipr import *
from time import time, sleep
import constants as c
import utilities as u
from createserial.commands import create_dd
from createserial.encoders import Encoders

import actions as a
from sensors import read_cliffs, on_white

GYRO_OFFSET = 0


def drive(l_speed: int, r_speed: int):
    """Drives left and right motor for values between -100 to 100"""
    create_dd(r_speed * -5, (int(l_speed * -5 * c.ADJUST_SPEED)))


def drive_timed(l_speed: int, r_speed: int, drive_time: int):
    """Drives left and right for time milliseconds and motor values between -100 and 100"""
    drive(l_speed, r_speed)
    msleep(drive_time)
    u.stop()


def drive_distance_default(speed: int, distance: float):
    converted = (speed * 5) / 25.4  # mm/sec to in/sec
    ms = abs(int((distance / converted) * 1000))
    drive_timed(speed, speed, ms)


def calibrate_gyro():
    global GYRO_OFFSET
    total = 0
    for _ in range(100):
        total += gyro_z()
        msleep(10)
    GYRO_OFFSET = total / 100


def calibrated_gyro_z():
    return gyro_z() - GYRO_OFFSET


def drive_distance_straight(speed: int, distance: float):
    end_time = time() + abs(distance * 25.4 / speed / 5)
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
    u.stop()


def drive_distance_straight_2(speed: int, distance):
    end_time = time() + abs(distance * 25.4 / speed / 5)
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
    u.stop()


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
        # print("in loop", left, right, inches, l_speed, r_speed, arc_length)
    drive(0, 0)


def spin(speed, angle):
    arc_length = (angle * 9 * math.pi) / 360
    encoders = Encoders()
    left, right = encoders.values
    right = -1 * right
    left = -1 * left
    r_speed = l_speed = speed * 5
    inches = 0
    create_dd(-l_speed, r_speed)
    while abs(inches) < abs(arc_length):
        # msleep(15)
        left, right = encoders.values
        inches = abs(right) * ((math.pi * 72 / 508.8) / 24.5)  # + (abs(left) * (math.pi * 72 / 508.8) / 24.5)
        # print("in loop", left, right, inches, l_speed, r_speed, arc_length)
    drive(0, 0)


def spin_to_black(speed):
    r_speed = l_speed = speed * 5
    while analog_et(0) < c.TOPHAT_THRESHOLD:
        msleep(15)
        create_dd(-l_speed, r_speed)
        # print(analog_et(0))
    drive(0, 0)


def spin_to_white(speed):
    r_speed = l_speed = speed * 5
    while analog_et(0) > c.TOPHAT_THRESHOLD:
        msleep(15)
        create_dd(-l_speed, r_speed)
        # print(analog_et(0))
    drive(0, 0)


def spin_to_black_2(speed):
    r_speed = l_speed = speed * 5
    if analog_et(0) < c.TOPHAT_THRESHOLD:
        print("on white, spinning to black")
        create_dd(-l_speed, r_speed)  # or drive ?
        while analog_et(0) < c.TOPHAT_THRESHOLD:
            pass
        # print(analog_et(0))
    drive(0, 0)


def spin_to_white_2(speed):
    r_speed = l_speed = speed * 5
    if analog_et(0) > c.TOPHAT_THRESHOLD:
        create_dd(-l_speed, r_speed)  # or drive ?
        while analog_et(0) > c.TOPHAT_THRESHOLD:
            pass
            # print(analog_et(0))
    drive(0, 0)


def drive_until_black(speed):
    drive(speed, int(speed * 0.80))  # 0.85 same for prime and clone?
    rCliff, lCliff = read_cliffs()
    while rCliff > 1500 and lCliff > 1000:
        rCliff, lCliff = read_cliffs()
    drive(0, 0)


def drive_until_black_square(speed):
    drive(speed, int(speed * 0.80))  # 0.85 same for prime and clone?
    l_speed = r_speed = speed
    while True:
        rCliff, lCliff = read_cliffs()
        if rCliff < u.pc(1500, 1700):
            r_speed = 0
            drive(l_speed, r_speed)
            # print("right on black")
        if lCliff < 1500:
            l_speed = 0
            drive(l_speed, r_speed)
            # print("left on black")
        if l_speed == 0 and r_speed == 0:
            break


def drive_until_white(speed):
    drive(speed, int(speed * 0.80))  # 0.85 same for prime and clone?
    rCliff, lCliff = read_cliffs()
    while rCliff < 1500 and lCliff < 1000:
        rCliff, lCliff = read_cliffs()
    drive(0, 0)


def arc_to_black(speed, direction):
    if direction == "r":
        l_speed = int(speed / 8)
        r_speed = speed
    if direction == "l":
        l_speed = speed
        r_speed = int(speed / 8)
    drive(l_speed, r_speed)
    while True:
        rCliff, lCliff = read_cliffs()
        if rCliff < 1500:
            r_speed = 0
            drive(l_speed, r_speed)
        if lCliff < 1500:
            l_speed = 0
            drive(l_speed, r_speed)
        if l_speed == 0 and r_speed == 0:
            break
    drive(0, 0)


def drive_with_line_follow(speed, distance):  # distance is in inches
    encoders = Encoders()
    right, left = encoders.values
    right = -1 * right
    left = -1 * left
    r_speed = l_speed = speed
    inches = 0
    create_dd(r_speed * -5, l_speed * -5)
    while abs(inches) < abs(distance):
        sensor_value = analog12(c.TOP_HAT)
        # print(sensor_value)
        # if sensor_value >= 1700:
        #     create_dd(((r_speed - 3) * -5), l_speed * -5)
        # elif 900 < sensor_value < 1700:
        #     create_dd(r_speed * -5, l_speed * -5)
        # else:
        #     create_dd(r_speed * -5, (l_speed - 3) * -5)

        val_difference = round((1050 - sensor_value) / 200)
        # print(val_difference)
        if 700 < sensor_value < 1400:
            # print("go straight")
            create_dd(r_speed * -5, l_speed * -5)
        else:
            if val_difference > 0:
                create_dd(r_speed * -5, int(l_speed - val_difference) * -5)
                # print("speed: ", int(l_speed - val_difference) * -5, "turn left")
            else:
                create_dd((int(r_speed - abs(val_difference)) * -5), l_speed * -5)
                # print("speed: ", (int(r_speed - abs(val_difference)) * -5), "turn right")

        right, left = encoders.values
        right = -1 * right
        left = -1 * left
        inches = 0.5 * ((right * (math.pi * 72 / 508.8) / 24.5) + (left * (math.pi * 72 / 508.8) / 24.5))
    drive(0, 0)


# encoder values to inches: n * (math.pi * 72 / 508.8) / 24.5 where n equals encoder values
def drive_straight(speed, distance: float):
    p = 0.25  # was p = 0.30
    i = 0.05  # was i = 0.05
    encoders = Encoders()
    right, left = encoders.values
    right = -1 * right
    left = -1 * left
    old_left, old_right = left, right
    r_speed = l_speed = speed
    inches = 0
    create_dd(r_speed * -5, int(l_speed * -5 * c.ADJUST_SPEED))
    while abs(inches) < abs(distance):
        # msleep(15)
        right, left = encoders.values
        right = -1 * right
        left = -1 * left
        inches = 0.5 * ((right * (math.pi * 72 / 508.8) / 24.5) + (left * (math.pi * 72 / 508.8) / 24.5))
        p_error = (right - old_right) - (left - old_left)  # short term
        i_error = right - left  # long term
        # print(p_error, i_error, p * p_error, i * i_error)
        r_speed -= int(p * p_error + i * i_error)
        l_speed += int(p * p_error + i * i_error)
        create_dd(r_speed * -5, int(l_speed * -5 * c.ADJUST_SPEED))
        old_left = left
        old_right = right
    drive(0, 0)

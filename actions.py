from kipr import create_connect_once, create_full, create_disconnect, msleep, enable_servos, disable_servos

import constants as c
from drive import drive, drive_timed, stop, spin
import motors
import servos


def debug():
    stop()
    msleep(1000)
    print("exited")
    exit(0)


# def some_action():
#     drive_distance_straight(30, 36)


def leave_start_box():
    servos.move_timed(c.WIPER, c.WIPER_MIDDLE, 250)
    drive_timed(40, 40, 1000)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 250)
    spin(20, 950)
    servos.move_timed(c.WIPER, c.WIPER_MIDDLE, 250)
    drive_timed(40, 40, 1000)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 250)
    debug()


def cross_board():
    drive_timed(40, 40, 4000)


def wiper_wiggle():
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 500)
    msleep(200)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 500)
    msleep(200)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 500)
    msleep(200)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 500)


def elevator_up():
    motors.move_timed(0, 50, 3000)


def elevator_down():
    motors.move_timed(0, -50, 3000)


def init():
    print("initing")
    if not create_connect_once():
        print("failed to connect")
        print("Is the create on?")
        exit()
    create_full()
    enable_servos()


def shut_down():
    print("shutting down")
    create_disconnect()
    disable_servos()
    print("Shut down")

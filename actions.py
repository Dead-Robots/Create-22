from kipr import create_connect_once, create_full, create_disconnect, msleep

import constants as c
from drive import drive, drive_timed, stop, drive_distance_straight


def debug():
    stop()
    msleep(1000)
    print("exited")
    exit(0)

def some_action():
    drive_distance_straight(30, 36)


def leave_start_box():
    drive_timed(40, 40, 2500)


def turn_right():
    drive_timed(40, -40, 950)


def cross_board():
    drive_timed(40, 40, 4000)


def init():
    print("initing")
    if not create_connect_once():
        print("failed to connect")
        print("Is the create on?")
        exit()
    create_full()


def shut_down():
    print("shutting down")
    create_disconnect()
    print("Shut down")

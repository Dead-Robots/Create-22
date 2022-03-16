from kipr import create_connect_once, create_full, create_disconnect, msleep, enable_servos, disable_servos, \
    enable_servo, push_button

import constants as c
from drive import drive, drive_timed, stop, spin, left_pivot, right_pivot
import motors
import servos


def init():
    print("initing")
    if not create_connect_once():
        print("failed to connect")
        print("Is the create on?")
        exit()
    create_full()
    enable_servo(c.WRIST)
    servos.move_timed(c.WRIST, c.WRIST_START, 500)
    enable_servo(c.ELBOW)
    servos.move_timed(c.ELBOW, c.ELBOW_START, 1000)
    enable_servo(c.WIPER)
    servos.move_timed(c.WIPER, c.WIPER_MIDDLE, 500)
    print("push button to continue")
    while not push_button():
        pass
    # POST()


def debug():
    stop()
    msleep(1000)
    print("exited")
    exit(0)


# def some_action():
# drive_distance_straight(30, 36)


def leave_start_box():
    drive_timed(40, 40, 900)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 250)
    drive_timed(40, -20, 700)  # left_pivot(-40, 500)
    drive_timed(40, 40, 200)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 250)
    drive_timed(40, 40, 800)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 250)
    spin(20, 400)
    # servos.move_timed(c.WIPER, c.WIPER_MIDDLE, 250)
    drive_timed(40, 40, 700)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 250)
    drive_timed(40, 40, 500)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 250)
    drive_timed(40, 40, 800)
    spin(30, 100)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 500)
    drive_timed(40, 40, 800)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT_CRUNCH, 500)
    # servos.move_timed(c.WIPER, c.WIPER_LEFT_CRUNCH, 700)
    # servos.move_timed(c.WRIST, c.WRIST_LIFT, 600)
    servos.move_timed(c.WRIST, 1800, 300)

    # To the airlock
    spin(20, 370)
    drive_timed(40, 40, 1500)
    servos.move_timed(c.WRIST, c.WRIST_START, 300)
    drive_timed(40, 40, 2000)
    spin(-20, 210)
    drive_timed(30, 30, 1650)
    drive_timed(-25, -25, 850)
    servos.move_timed(c.ELBOW, c.ELBOW_DELIVER, 1000)
    servos.move_timed(c.WRIST, c.WRIST_DELIVER, 700)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT_CRUNCH, 300)
    drive_timed(30, 30, 940)
    drive_timed(10, 10, 400)

    # make code for a touch sensor on the wiper to know the right time
    # to drop the poms in the airlock

    debug()

    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 250)
    spin(20, 450)
    drive_timed(40, 40, 800)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 250)
    drive_timed(40, 40, 750)
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 250)
    spin(20, 250)
    drive_timed(40, 40, 650)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 250)
    spin(-20, 100)
    drive_timed(40, 40, 750)
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
    motors.move_timed(0, -50, 2400)


def POST():
    # moves wiper
    servos.move_timed(c.WIPER, c.WIPER_RIGHT, 500)
    msleep(1000)
    servos.move_timed(c.WIPER, c.WIPER_LEFT, 500)
    msleep(1000)
    servos.move_timed(c.WIPER, c.WIPER_MIDDLE, 500)

    # moves elbow and wrist
    servos.move_timed(c.ELBOW, c.ELBOW_DELIVER, 1000)
    msleep(1000)
    servos.move_timed(c.WRIST, c.WRIST_DELIVER, 500)
    msleep(1000)
    servos.move_timed(c.WRIST, c.WRIST_START, 500)
    msleep(1000)
    servos.move_timed(c.ELBOW, c.ELBOW_START, 1000)


def shut_down():
    print("shutting down")
    create_disconnect()
    disable_servos()
    print("Shut down")

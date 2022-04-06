from kipr import create_connect_once, create_full, create_disconnect, msleep, enable_servo, disable_servo, \
    enable_servo, push_button, get_servo_position, disable_servos, get_create_lcliff, get_create_rcliff

import constants as c
from drive import drive, drive_timed, stop, spin, left_pivot, right_pivot, drive_distance_straight, calibrate_gyro, \
    drive_distance_straight_2
import motors
import servo

from createserial.createCommands import open_create, close_create
from createserial.myserial import open_serial, close_serial


def init():
    print("initing")
    # if not create_connect_once():
    #     print("failed to connect")
    #     print("Is the create on?")
    #     exit()
    # create_full()

    # Open a serial port connection to the Create
    open_serial()
    # Initialize the Create
    open_create()

    calibrate_gyro()

    servo.move(c.ARM, c.ARM_INIT)
    enable_servo(c.ARM)
    servo.move(c.WRIST, c.WRIST_INIT)
    enable_servo(c.WRIST)

    wait_for_button()

    servo.move(c.ARM, c.ARM_BOTGUY)
    servo.move(c.WRIST, c.WRIST_UP)

    spin(50, 1550)

    drive_timed(25, 25, 1500)

    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CENTER)
    enable_servo(c.LEFT_WIPER)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CENTER)
    enable_servo(c.RIGHT_WIPER)
    while not push_button():
        read_cliff_sensors()
        msleep(500)

    # POST()


def debug():
    stop()
    msleep(1000)

    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()

    print("exited")
    exit(0)


def wait_for_button():
    print("push button to continue")
    while not push_button():
        pass


def leave_start_box():
    servo.move(c.ARM, c.ARM_BOTGUY)
    servo.move(c.WRIST, c.WRIST_UP)
    wait_for_button()
    drive_timed(-70, -70, 3700)


def grab_botguy():
    spin(50, 780)
    drive_timed(70, 70, 1800)
    drive_timed(-25, -25, 800)
    spin(50, 200)

    wait_for_button()

    servo.move(c.WRIST, c.WRIST_BOTGUY)
    spin(-25, 1500)


def read_cliff_sensors():
    print("Left:", get_create_lcliff(), "; Right: ", get_create_rcliff())


def drive_to_poms():

    spin(50, 775)   # 90 degrees?


def collect_poms():
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CENTER)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CENTER)

'''
def deliver_to_airlock():
    drive_distance_straight(-50, 30)
    spin(50, 900)
    servo.move(c.ELBOW, c.ELBOW_DELIVER)
    drive_distance_straight(50, 20)
    right_pivot(50, 400)
    while not push_button():
        pass
    servo.move(c.WIPER, c.WIPER_MIDDLE, 500)


def sort_poms():
    servo.move(c.WIPER, c.WIPER_RIGHT)
    drive_timed(40, -20, 700)  # left_pivot(-40, 500)
    drive_timed(40, 40, 200)
    servo.move(c.WIPER, c.WIPER_LEFT)
    drive_timed(40, 40, 800)
    servo.move(c.WIPER, c.WIPER_RIGHT)
    spin(20, 400)
    # servo.move_timed(c.WIPER, c.WIPER_MIDDLE, 250)
    drive_timed(40, 40, 700)
    servo.move(c.WIPER, c.WIPER_LEFT)
    spin(20, 400)
    drive_timed(40, 40, 500)
    servo.move(c.WIPER, c.WIPER_RIGHT)
    drive_timed(40, 40, 800)
    spin(30, 100)
    servo.move(c.WIPER, c.WIPER_LEFT)
    drive_timed(40, 40, 800)
    servo.move(c.WIPER, c.WIPER_RIGHT_CRUNCH)
    # servo.move_timed(c.WIPER, c.WIPER_LEFT_CRUNCH, 700)
    # servo.move_timed(c.WRIST, c.WRIST_LIFT, 600)
    servo.move(c.WRIST, 1800)

    # To the airlock
    spin(20, 370)
    drive_timed(40, 40, 1500)
    servo.move(c.WRIST, c.WRIST_START)
    drive_timed(40, 40, 2000)
    spin(-20, 210)
    drive_timed(30, 30, 1650)
    drive_timed(-25, -25, 850)
    servo.move(c.ELBOW, c.ELBOW_DELIVER)
    servo.move(c.WRIST, c.WRIST_DELIVER)
    servo.move(c.WIPER, c.WIPER_RIGHT_CRUNCH)
    drive_timed(30, 30, 940)
    drive_timed(10, 10, 400)

    # make code for a touch sensor on the wiper to know the right time
    # to drop the poms in the airlock

    # THIS NEEDS TO BE REVISED
    servo.move(c.WIPER, c.WIPER_RIGHT)
    spin(20, 450)
    drive_timed(40, 40, 800)
    servo.move(c.WIPER, c.WIPER_LEFT)
    drive_timed(40, 40, 750)
    servo.move(c.WIPER, c.WIPER_RIGHT)
    spin(20, 250)
    drive_timed(40, 40, 650)
    servo.move(c.WIPER, c.WIPER_LEFT)
    spin(-20, 100)
    drive_timed(40, 40, 750)
    debug()


def cross_board():
    drive_timed(40, 40, 4000)


def wiper_wiggle():
    servo.move(c.WIPER, c.WIPER_RIGHT)
    msleep(200)
    servo.move(c.WIPER, c.WIPER_LEFT)
    msleep(200)
    servo.move(c.WIPER, c.WIPER_RIGHT)
    msleep(200)
    servo.move(c.WIPER, c.WIPER_LEFT)


def elevator_up():
    motors.move_timed(0, 50, 3000)


def elevator_down():
    motors.move_timed(0, -50, 2400)


def POST():
    # moves wiper
    servo.move(c.WIPER, c.WIPER_RIGHT)
    msleep(1000)
    servo.move(c.WIPER, c.WIPER_LEFT)
    msleep(1000)
    servo.move(c.WIPER, c.WIPER_MIDDLE)

    # moves elbow and wrist
    servo.move(c.ELBOW, c.ELBOW_DELIVER)
    msleep(1000)
    servo.move(c.WRIST, c.WRIST_DELIVER)
    msleep(1000)
    servo.move(c.WRIST, c.WRIST_START)
    msleep(1000)
    servo.move(c.ELBOW, c.ELBOW_START)
'''


def shut_down():
    print("shutting down")
    create_disconnect()
    disable_servos()
    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()
    print("shut down")

from kipr import create_disconnect, msleep, enable_servo, push_button, disable_servos

import constants as c
from drive import drive_timed, stop, spin, calibrate_gyro, drive_until_black, drive_straight, pivot, spin_to_black, \
    spin_to_white, drive, drive_distance_default
import servo
from sensors import read_cliffs

from createserial.commands import open_create, close_create
from createserial.serial import open_serial, close_serial


def init():
    print("initing")
    # if not create_connect_once():
    #     print("failed to connect")
    #     print("Is the create on?")
    #     exit()
    # create_full()

    open_serial()  # Open a serial port connection to the Create
    open_create()  # Initialize the Create
    calibrate_gyro()

    enable_servo(c.ARM)
    enable_servo(c.WRIST)
    enable_servo(c.RIGHT_WIPER)
    enable_servo(c.LEFT_WIPER)

    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)

    servo.move(c.WRIST, c.WRIST_POM)
    servo.move(c.ARM, c.ARM_DOWN)

    wait_for_button()


def collect_and_deliver_cubes():
    drive_straight(5, 1.25)  # was 1 inch last time
    msleep(250)

    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CUBES)
    servo.move(c.ARM, c.ARM_CUBES)
    servo.move(c.WRIST, c.WRIST_CUBES)
    spin(20, 70)

    servo.move(c.ARM, 1000)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)


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
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)

    spin(30, 90)
    drive_distance_default(40, 4)

    msleep(250)
    drive_straight(-60, 60)


def grab_botguy():
    msleep(250)
    drive_straight(-40, 54)
    spin(-50, 80)
    drive_straight(40, 25)
    msleep(250)
    drive_straight(-30, 4)
    spin(15, 50)
    drive_straight(30, 4)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CENTER)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CENTER)
    debug()
    servo.move(c.WRIST, c.WRIST_BOTGUY)
    spin(-25, 15)


def collect_poms():
    spin(40, 87)
    msleep(500)
    drive_until_black(-30)
    spin(-40, 79)  # was 83
    drive_distance_default(10, 3.5)  # was 3 inches
    # drive_straight(3, 10)

    # servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    # servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    # spin(20, 3)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.WRIST, c.WRIST_POM)
    servo.move(c.ARM, c.ARM_DOWN)

    drive_distance_default(25, 3)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + 100)

    spin_to_black(3)
    servo.move(c.ARM, c.ARM_DOWN)
    drive_distance_default(25, 5.2)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + 100)

    spin_to_white(-3)
    servo.move(c.ARM, c.ARM_DOWN)
    drive_distance_default(25, 5.2)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + 100)

    spin_to_black(3)
    servo.move(c.ARM, c.ARM_DOWN)
    drive_distance_default(25, 5) # slightly shorter drive
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + 100)

    spin_to_white(-3)
    servo.move(c.ARM, c.ARM_DOWN)
    drive_distance_default(25, 5)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + 100)

    spin_to_black(3)  # used to be spin(-5, 7), 3rd green pom, longer now
    servo.move(c.ARM, c.ARM_DOWN)
    drive_distance_default(25, 5)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + 100)

    spin_to_white(-3)
    servo.move(c.ARM, c.ARM_DOWN)
    drive_distance_default(25, 5.2)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + 100)

    spin_to_black(3)
    servo.move(c.ARM, c.ARM_DOWN)
    drive_distance_default(25, 3.5)


    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)

    servo.move(c.ARM, c.ARM_DOWN + 100)
    drive_distance_default(-25, 3)

    servo.move(c.ARM, c.ARM_BOTGUY)
    spin(-20, 8)
    drive_distance_default(50, 18)


def deliver_poms_to_transporter():
    drive_straight(-60, 70)
    spin(-30, 162)
    msleep(500)
    msleep(500)

    servo.move(c.ARM, c.ARM_DELIVER_LOW, 15)
    servo.move(c.WRIST, c.WRIST_DELIVER_LOW, 15)
    msleep(250)

    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)



def deliver_poms_to_airlock():
    drive_straight(-60, 60)
    spin(40, 90)
    msleep(500)
    drive_straight(30, 22)
    servo.move(c.ARM, c.ARM_DELIVER_HIGH, 15)
    drive_straight(-40, 6)

    spin(25, 90)
    msleep(500)
    servo.move(c.WRIST, c.WRIST_DELIVER_HIGH, 15)

    drive_straight(20, 14)
    msleep(500)
    spin(-10, 10)
    msleep(500)
    spin(10, 10)
    msleep(500)
    drive_straight(-20, 12)
    spin(-10, 10)
    servo.move(c.ARM, c.ARM_DELIVER_FINAL + 75, 10)
    drive_straight(10, 10)
    servo.move(c.ARM, c.ARM_DELIVER_FINAL, 10)
    spin(-10,3)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN, 15)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN, 15)
    #spin(5, 5)
    #servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN - 50, 15)
    #msleep(500)
    #spin(-5, 5)
    #servo.move(c.RIGHT_WIPER, c.LEFT_WIPER_OPEN + 50, 15)
    #msleep(500)



def shut_down():
    print("shutting down")
    create_disconnect()
    disable_servos()
    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()
    print("shut down")


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

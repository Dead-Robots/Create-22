import time
from kipr import create_disconnect, msleep, enable_servo, push_button, disable_servos, disable_servo, analog, analog_et
import constants as c
from drive import drive_timed, stop, spin, calibrate_gyro, drive_until_black, drive_straight, pivot, spin_to_black, \
    spin_to_white, drive, drive_distance_default, on_white, spin_to_white_2, spin_to_black_2
import servo
from sensors import read_cliffs, wait_4_light

from createserial.commands import open_create, close_create, reset_create
from createserial.serial import open_serial, close_serial

from createserial.shutdown import shutdown_create_in

t = 0


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create

    # calibrate_gyro()

    enable_servo(c.WRIST)
    servo.move(c.WRIST, c.WRIST_START)
    enable_servo(c.ARM)
    servo.move(c.ARM, c.ARM_DOWN)
    enable_servo(c.RIGHT_WIPER)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    enable_servo(c.LEFT_WIPER)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)

    power_on_self_test()

    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)

    servo.move(c.WRIST, c.WRIST_POM)
    servo.move(c.ARM, c.ARM_DOWN)

    # wait_for_button()
    wait_4_light()

    global t
    t = time.time()

    shutdown_create_in(119)


def power_on_self_test():
    print("starting power on self test")
    print("testing white")
    if analog(0) < c.TOPHAT_THRESHOLD:
        print("I see white.")
    else:
        print("uh oh")
        shut_down()

    print("lift arm")
    servo.move(c.ARM, c.ARM_DELIVER_HIGH, 25)

    print("testing black")
    if analog(0) > c.TOPHAT_THRESHOLD:
        print("I see black.")
    else:
        print("uh oh")
        shut_down()

    print("lift wrist")
    servo.move(c.WRIST, c.WRIST_UP, 25)

    print("open/close right wiper")
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN, 25)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED, 25)
    print("open/close left wiper")
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN, 25)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED, 25)

    print("driving forward (+)")
    drive_straight(35, 6)
    print("driving backward (-)")
    drive_straight(-35, 6)
    print("finished power on self test!")


def collect_and_deliver_cubes():
    drive_straight(5, pc(1.25, 2.5))  # was 1 inch last time
    msleep(250)

    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CUBES)
    servo.move(c.ARM, c.ARM_CUBES)
    servo.move(c.WRIST, c.WRIST_CUBES)
    spin(20, 70)

    servo.move(c.ARM, 1000)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)





def leave_start_box():
    servo.move(c.ARM, c.ARM_BOTGUY)
    servo.move(c.WRIST, c.WRIST_UP)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)

    spin(30, 95)
    drive_distance_default(40, pc(7, 6))

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
    drive_timed(-20, 20, pc(1650, 1400))
    msleep(500)
    drive_until_black(-30)
    msleep(7000)
    # if c.IS_PRIME:
    #     spin(-40, pc(79, 90))  # was 83 for prime and was 86 for clone
    # if c.IS_CLONE:
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.WRIST, c.WRIST_POM + 50)
    servo.move(c.ARM, c.ARM_DOWN + 25)  # lift higher, so wrist doesn't get snagged on the tape?

    spin_to_black_2(-3)

    spin_to_white_2(-3)

    if c.IS_PRIME:
        drive_timed(10, -10, 100)
    else:
        spin(-3, 1)

    if c.IS_CLONE:
        servo.move(c.ARM, c.ARM_DOWN + 50)

    drive_distance_default(10, pc(5.8, 5))  # was 3 inches for clone

    if c.IS_CLONE:
        servo.move(c.ARM, c.ARM_DOWN)

    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.WRIST, c.WRIST_POM)
    servo.move(c.ARM, c.ARM_DOWN)

    # drive_distance_default(10, pc(2, 0))
    print("picking up pom 1")
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    if not on_white():
        print("crossed the line! on black 1")
        spin_to_white_2(-3)

    if c.IS_CLONE:
        servo.move(c.ARM, c.ARM_DOWN + pc(100, 75), 10)
        spin_to_black_2(3)
        spin_to_white_2(-3)
    else:
        spin_to_black_2(3)
        spin_to_white_2(-3)
        wait_for_button()
        # wait_for_button()
        # drive_timed(-10, 10, 450)
        # wait_for_button()

    drive_distance_default(10, pc(4.3, 4.1))  # 5.2
    print("picking up pom 2")
    servo.move(c.ARM, c.ARM_DOWN, 15)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    # spin_to_white_2(-3)  # the problem
    spin(-10, pc(10, 7))  # blind spin
    servo.move(c.ARM, c.ARM_DOWN, 10)
    print("picking up pom 3")
    drive_distance_default(10, pc(4.6, 5.0))  # prime was 5.2
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    if not on_white():
        print("crossed the line! on black 3")
        spin_to_white_2(-3)

    spin_to_black_2(3)

    if c.IS_CLONE:
        # spin_to_white_2(-3)
        drive_timed(10, -10, 125)
    else:
        # spin(-10, 3) # 6
        drive_timed(10, -10, 125)

    servo.move(c.ARM, c.ARM_DOWN, 10)
    drive_distance_default(10, pc(4.5, 4.4))  # slightly shorter drive
    print("picking up pom 4")
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    # if c.IS_CLONE:
    #     if on_white():
    #         print("crossed the line! on white 4")
    #         spin_to_black_2(-3)
    #     spin_to_white_2(-3)

    spin_to_white_2(-3)
    drive_timed(10, -10, pc(200, 0))
    servo.move(c.ARM, c.ARM_DOWN, 10)
    drive_distance_default(10, pc(5.2, 4.4))
    print("picking up pom 5")
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    if c.IS_CLONE:
        if not on_white():
            print("crossed the line! on black 5")
            spin_to_white_2(-3)
        spin_to_black_2(3)

    spin_to_black_2(3)
    spin_to_white_2(-3)
    # drive_timed(10, -10, 125)  # used to be spin(-5, 7), 3rd green pom, longer now # 6
    servo.move(c.ARM, c.ARM_DOWN, 10)
    drive_distance_default(10, pc(4.5, 4.5))
    print("picking up pom 6")
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    # if c.IS_CLONE:
    #     if on_white():
    #         print("crossed the line! on white 6")
    #         spin_to_black_2(-3)
    #     spin_to_white_2(-3)

    spin_to_white_2(-3)
    spin(-10, pc(3, 0))
    servo.move(c.ARM, c.ARM_DOWN, 10)
    drive_distance_default(10, pc(5.2, 4.8))
    print("picking up pom 7")
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED - 170)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    if c.IS_CLONE:
        if not on_white():
            print("crossed the line! on black 7")
            spin_to_white_2(-3)
        spin_to_black_2(3)

    spin_to_black_2(3)
    # drive_timed(10, -10, 200)

    servo.move(c.ARM, c.ARM_DOWN, 10)

    drive_distance_default(10, pc(3.1, 2.9))

    print("picking up pom 8")
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED + 170)

    servo.move(c.ARM, c.ARM_DOWN + pc(100, 50), 10)

    for x in range(0):
        servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
        servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED + 100)
        servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
        servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED - 100)

    drive_distance_default(-25, 3)

    servo.move(c.ARM, c.ARM_BOTGUY)
    servo.move(c.WRIST, c.WRIST_DRIVE_UP, 15)
    spin(-20, 8)
    drive_distance_default(50, pc(18, 20))


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
    # spin(40, 90)
    drive_timed(-20, 20, pc(1520, 1400))
    # drive_straight(30, 22)
    drive_distance_default(30, 23)
    servo.move(c.ARM, c.ARM_DELIVER_HIGH, 15)
    drive_straight(-40, pc(5, 4.6))

    spin(25, 90)
    msleep(500)
    servo.move(c.WRIST, c.WRIST_DELIVER_HIGH, 15)

    drive_straight(40, pc(13.5, 13))
    msleep(500)
    spin(-10, 15)
    msleep(500)
    spin(10, 15)
    msleep(500)
    drive_distance_default(-10, pc(7, 10))  # FIND PRIME VALUE
    spin(-10, 8)
    servo.move(c.ARM, c.ARM_DELIVER_HIGH - pc(30, 30), 10)  # was 0
    servo.move(c.WRIST, c.WRIST_DELIVER_HIGH - pc(30, 60))  # was 0
    drive_distance_default(10, pc(7, 9))
    servo.move(c.ARM, c.ARM_DELIVER_FINAL, 10)
    servo.move(c.WRIST, c.WRIST_DELIVER_FINAL)  # prime doesn't need wrist adjustment here
    # spin(-10, 3)
    drive_timed(10, -10, 125)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_DELIVER_OPEN, 15)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_DELIVER_OPEN, 15)

    # spin(3, 5)
    drive_timed(-10, 10, 90)
    for x in range(0):
        servo.move(c.LEFT_WIPER, c.LEFT_WIPER_DELIVER_OPEN)
        servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    msleep(500)
    disable_servo(c.LEFT_WIPER)
    # spin(-3, 5)
    drive_timed(10, -10, 90)
    for x in range(0):
        servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_DELIVER_OPEN)
        servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    msleep(500)
    disable_servo(c.RIGHT_WIPER)
    # spin(3, 3)
    drive_timed(-10, 10, 90)
    servo.move(c.ARM, c.ARM_DELIVER_FINAL - 100, 10)  # places the arm completely down on the airlock


def shut_down():
    print("shutting down")
    create_disconnect()
    disable_servos()
    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()
    print("shut down", time.time() - t)


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

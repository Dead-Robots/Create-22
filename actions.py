import time
from kipr import create_disconnect, msleep, enable_servo, push_button, disable_servos, disable_servo, analog, analog_et, \
    motor, motor_power
import constants as c
import utilities
from drive import drive_timed, spin, calibrate_gyro, drive_until_black, drive_straight, pivot, spin_to_black, \
    spin_to_white, drive, drive_distance_default, on_white, spin_to_white_2, spin_to_black_2, drive_with_line_follow, \
    arc_to_black, drive_until_white, drive_until_black_square
import servo
from motors import move_motor_till_stall, move_motor_to_position
from sensors import read_cliffs, wait_4_light
from utilities import stop, pc, debug, wait_for_button

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

    power_on_self_test()

    move_motor_to_position(c.BOT_STICK, -40, c.BOT_STICK_START)

    wait_4_light(True)

    global t
    t = time.time()

    # shutdown_create_in(119)


def test_line_follow():
    wait_for_button()
    servo.move(c.ARM, c.ARM_DOWN + 100)
    drive_with_line_follow(10, 24)
    wait_for_button()


def power_on_self_test():
    print("starting power on self test")

    print("moving hook")
    move_motor_till_stall(c.BOT_STICK, 50)

    enable_servo(c.WRIST)
    servo.move(c.WRIST, c.WRIST_START)
    enable_servo(c.ARM)
    servo.move(c.ARM, c.ARM_DOWN)
    enable_servo(c.RIGHT_WIPER)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    enable_servo(c.LEFT_WIPER)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)

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

    servo.move(c.WRIST, c.WRIST_POM)
    servo.move(c.ARM, c.ARM_DOWN)

    print("driving forward (+)")
    drive_straight(35, 6)

    print("driving backward (-)")
    drive_straight(-35, 6)
    print("finished power on self test!")

    # move_motor_till_stall(c.BOT_STICK, -50)


def collect_and_deliver_cubes():
    wait_for_button()
    print("collect_and_deliver_cubes")
    move_motor_till_stall(c.BOT_STICK, 60)

    # drive_distance_default(5, 1)
    msleep(250)

    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN, 35)
    servo.move(c.ARM, c.ARM_MAX, 35) # was originally ARM_CUBES
    servo.move(c.WRIST, c.WRIST_UP, 35) # was originally WRIST_CUBES
    spin(50, 165) # was originally 20, 70

    # servo.move(c.ARM, 1000)
    # servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    motor_power(c.BOT_STICK, 0)


def leave_start_box():
    print("leave_start_box")

    print("leaving the start box")
    # servo.move(c.ARM, c.ARM_MAX)
    # servo.move(c.WRIST, c.WRIST_UP)
    # servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    # servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)

    # spin(30, 95)
    drive_distance_default(40, pc(6, 6)) # prime was originally 7

    msleep(250)

    drive_straight(-70, 49.5)  # was 44.5
    spin(-50, 75)
    msleep(250)

    print("going to knock off botguy")
    drive_straight(30, 20.5)  # was 19.5
    spin(-50, 80)
    msleep(250)
    drive_straight(-30, 5)

    print("spinning to knock off botguy")
    spin(-65, 175)
    msleep(250)

    print("preparing for picking up poms")
    drive_straight(-30, 15)
    spin(-50, 75)
    msleep(250)
    drive_until_black_square(-20)
    drive_straight(-30, 2)
    servo.move(c.WRIST, c.WRIST_CUBES)
    servo.move(c.ARM, c.ARM_CUBES)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    msleep(250)
    spin(30, 45)
    msleep(250)

    print("beginning of pom pickup")
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.WRIST, c.WRIST_POM - 25)
    servo.move(c.ARM, c.ARM_DOWN)  # lift higher, so wrist doesn't get snagged on the tape?
    msleep(500)
    spin_to_black_2(10)


def grab_botguy():
    wait_for_button()
    spin(-50, 180)
    drive_straight(40, 25)
    wait_for_button()
    msleep(250)
    drive_straight(-30, 4)
    spin(15, 50)
    wait_for_button()
    drive_straight(30, 4)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CENTER)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CENTER)
    servo.move(c.WRIST, c.WRIST_BOTGUY)
    spin(25, 15)


def collect_poms():
    print("collect_poms")
    # drive_timed(-20, 20, pc(1650, 1400))
    spin(30, 90)
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

    servo.move(c.ARM, c.ARM_MAX)
    servo.move(c.WRIST, c.WRIST_DRIVE_UP, 15)
    spin(-20, 8)
    drive_distance_default(50, pc(18, 20))


def collect_poms_new():
    print("collect_poms")

    print("line following!")
    servo.move(c.WRIST, c.WRIST_POM - 100)
    drive_with_line_follow(20, 6) 
    msleep(200)

    print("picking up pom 1")
    servo.move(c.ARM, c.ARM_DOWN + 50, 10)
    collect_red_pom(c.ARM_DOWN + 50, c.WRIST_POM)  # originally ARM_DOWN + 0

    print("picking up pom 2")
    # spin(-10, 5)  # was positive
    servo.move(c.ARM, c.ARM_DOWN + 75, 10)
    drive_distance_default(10, 3.5)
    collect_green_pom(c.ARM_DOWN - 50, c.WRIST_POM)

    print("picking up pom 3")
    drive_with_line_follow(10, 6)
    collect_red_pom(c.ARM_DOWN - 50, c.WRIST_POM)

    print("picking up pom 4")
    drive_with_line_follow(10, 6)
    collect_green_pom(c.ARM_DOWN, c.WRIST_POM)

    print("picking up pom 5")
    drive_with_line_follow(10, 6)
    collect_red_pom(c.ARM_DOWN, c.WRIST_POM)

    print("picking up pom 6")
    drive_with_line_follow(10, 6)
    collect_green_pom(c.ARM_DOWN, c.WRIST_POM)

    print("picking up pom 7")
    drive_with_line_follow(10, 6.5)  # was 6
    collect_red_pom(c.ARM_DOWN, c.WRIST_POM)

    print("picking up pom 8")
    servo.move(c.ARM, c.ARM_DOWN, 10)
    servo.move(c.WRIST, c.WRIST_POM, 10)
    drive_with_line_follow(10, 4.5)

    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.ARM, c.ARM_DOWN + 75, 10)

    drive_distance_default(-25, 3)

    servo.move(c.ARM, c.ARM_MAX)
    servo.move(c.WRIST, c.WRIST_DRIVE_UP, 15)
    drive_distance_default(50, pc(20, 20))  # prime was 18 for distance


def collect_red_pom(arm_height, wrist_height):
    servo.move(c.ARM, arm_height, 10)
    servo.move(c.WRIST, wrist_height, 10)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN)
    servo.move(c.ARM, arm_height + 50, 10)
    servo.move(c.WRIST, wrist_height + 25, 10)


def collect_green_pom(arm_height, wrist_height):
    servo.move(c.ARM, arm_height, 10)
    servo.move(c.WRIST, wrist_height, 10)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.ARM, arm_height + 50, 10)
    servo.move(c.WRIST, wrist_height + 25, 10)


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
    print("deliver poms to airlock")

    print("squaring up create")
    drive_straight(-60, 70)
    drive_timed(-20, 20, pc(1520, 1400))  # spin
    drive_straight(60, 19)
    drive_distance_default(35, 3)
    drive_straight(-40, pc(6, 4.6))  # Prime was originally 3

    spin(25, 90)
    msleep(500)

    drive_straight(60, pc(15, 13))  # prime was originally 13.5
    drive_distance_default(35, 3)
    msleep(500)

    print("moving airlock to proper position")
    drive_straight(-40, 15)
    servo.move(c.ARM, c.ARM_DELIVER_HIGH, 15)
    servo.move(c.WRIST, c.WRIST_DELIVER_HIGH)
    drive_timed(10, -10, 100)
    msleep(500)
    drive_straight(30, 9)
    msleep(500)
    spin(-5, 14)  # was originally 10
    msleep(500)

    print("moving claw to airlock")
    drive_timed(-10, 10, 200)
    msleep(250)
    servo.move(c.ARM, c.ARM_MAX)
    msleep(250)
    servo.move(c.WRIST, c.WRIST_MAX)
    msleep(250)
    drive_timed(10, -10, 750)
    msleep(250)
    drive_straight(-40, 8)
    msleep(250)

    print("delivering poms")
    servo.move(c.WRIST, c.WRIST_DELIVER_HIGH)  # was 0
    servo.move(c.ARM, c.ARM_DELIVER_HIGH, 10)  # was 0
    drive_distance_default(10, pc(2.5, 9))  # prime was 7
    msleep(250)
    servo.move(c.WRIST, c.WRIST_DELIVER_FINAL)  # prime doesn't need wrist adjustment here
    servo.move(c.ARM, c.ARM_DELIVER_FINAL, 10)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_DELIVER_OPEN, 15)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_DELIVER_OPEN, 15)

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
    # drive_timed(-10, 10, 90)
    servo.move(c.ARM, c.ARM_DELIVER_FINAL, 10)  # places the arm completely down on the airlock


def shut_down():
    print("shutting down")
    create_disconnect()
    disable_servos()
    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()
    print("shut down", time.time() - t)
    exit(0)


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

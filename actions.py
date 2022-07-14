import time
from kipr import create_disconnect, msleep, enable_servo, push_button, disable_servos, disable_servo, analog, analog_et, \
    motor, motor_power, set_servo_position
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
botguy_grab_time = 0


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create

    power_on_self_test()

    move_motor_to_position(c.BOT_STICK, -40, c.BOT_STICK_START)  # moves botstick down

    # wait_for_button()
    wait_4_light(False)

    global t  # to print out total time
    t = time.time()

    shutdown_create_in(119)


def test_line_follow():  # we don't use this right now
    wait_for_button()
    servo.move(c.ARM, c.ARM_DOWN + 100)
    drive_with_line_follow(10, 24)
    wait_for_button()


def power_on_self_test():
    print("starting power on self test")

    print("moving botstick")
    move_motor_till_stall(c.BOT_STICK, 50)  # swings botstick up

    enable_servo(c.WRIST)  # moving arm, wrist, and wipers into start position
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


def collect_cubes():  # was collect and deliver cubes
    print("collect_and_deliver_cubes")
    move_motor_till_stall(c.BOT_STICK, 60)  # first thing in routine, lifts botstick up and out of the way

    msleep(250)

    # drive_distance_default(5, 0.5)
    set_servo_position(c.RIGHT_WIPER, c.RIGHT_WIPER_GRAB)  # gripping cubes
    set_servo_position(c.LEFT_WIPER, c.LEFT_WIPER_GRAB)
    msleep(300)
    servo.move(c.ARM, c.ARM_MAX, 65)  # lifts up arm
    servo.move(c.WRIST, c.WRIST_UP, 65)  # lifts up wrist
    spin(50, 165)  # spin to wall, theoretically is a 180ish turn

    motor_power(c.BOT_STICK, 0)  # stops motor so that we don't burn out the motor


def collect_cubes_new():
    print("collect_and_deliver_cubes")
    move_motor_till_stall(c.BOT_STICK, 60)  # first thing in routine, lifts botstick up and out of the way

    msleep(250)

    motor_power(c.BOT_STICK, 0)  # stops motor so that we don't burn out the motor

    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN, 65)  # gripping cubes
    wait_for_button()
    servo.move(c.ARM, c.ARM_MAX, 65)  # lifts up arm
    wait_for_button()
    servo.move(c.WRIST, c.WRIST_UP, 65)  # lifts up wrist
    wait_for_button()
    drive_timed(-40, 40, 1000)
    #spin(50, 165)  # spin to wall, theoretically is a 180ish turn
    wait_for_button()
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)
    wait_for_button()

    drive_timed(40, -40, 1000)
    #spin(-50, 165)
    wait_for_button()
    servo.move(c.WRIST, c.WRIST_POM)
    wait_for_button()
    servo.move(c.ARM, c.ARM_DOWN)

    drive_distance_default(5, 0.5)
    wait_for_button()
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_OPEN, 65)  # gripping cubes
    wait_for_button()
    servo.move(c.ARM, c.ARM_MAX, 65)  # lifts up arm
    wait_for_button()
    servo.move(c.WRIST, c.WRIST_UP, 65)  # lifts up wrist
    wait_for_button()
    spin(50, 165)  # spin to wall, theoretically is a 180ish turn
    wait_for_button()



def leave_start_box_and_knock_off_botguy():  # was leave start box
    print("leaving the start box")

    drive_distance_default(50, pc(6, 6))  # squaring up against the wall
    msleep(250)

    # dropping cubes off the edge
    '''
    servo.move(c.WRIST, c.WRIST_DROP_CUBES, 65)
    msleep(100)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED, 65)
    msleep(100)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED, 65)
    msleep(100)
    servo.move(c.WRIST, c.WRIST_UP, 65)
    '''

    drive_straight(-90, pc(49.5, 50.5))  # drives almost all the way down the board
    msleep(250)
    spin(-50, pc(75, 88))  # spins so that its front is facing botguy
    msleep(250)

    print("going to knock off botguy")
    drive_straight(60, pc(20.5, 19.7))  # drives towards botguy
    spin(-50, pc(80, 85))  # spins to face transporter
    msleep(250)
    drive_straight(-60, pc(6, 7))  # drives backwards towards rings

    print("spinning to knock off botguy")
    spin(-55, pc(167, 175))  # the big spin to knock off botguy
    msleep(250)
    global botguy_grab_time  # records time that it takes to grab botguy
    botguy_grab_time = time.time() - t

    print("preparing for picking up poms")
    drive_straight(-30, 15)  # drives towards transporter
    spin(-50, pc(75, 93))  # spins to face other side
    msleep(250)
    drive_until_black_square(-20)  # drives backwards to black line
    drive_straight(-30, 2)  # drives back a little bit more

    # servo.move(c.WRIST, c.WRIST_CUBES)  # drops wrist down
    # servo.move(c.ARM, c.ARM_CUBES)  # drops arm down

    servo.move(c.WRIST, c.WRIST_POM) # drop wrist down to ground to release cubes
    servo.move(c.ARM, c.ARM_DOWN)

    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)  # lets go of cubes
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED)
    msleep(250)

    servo.move(c.ARM, c.ARM_CUBES, 65)
    servo.move(c.WRIST, c.WRIST_CUBES, 65)

    spin(30, 45)  # turn a bit towards the line
    msleep(250)

    print("beginning of pom pickup")
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED)  # preps wipers for pom pick up
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN)
    servo.move(c.WRIST, c.WRIST_POM - 25)
    servo.move(c.ARM, c.ARM_DOWN)
    msleep(500)
    spin_to_black_2(10)  # spins to black


def collect_poms_new():
    print("collect_poms")

    print("line following!")
    servo.move(c.WRIST, c.WRIST_POM - pc(100, 50))
    servo.move(c.ARM, c.ARM_DOWN + 70)  # was originally + 100, +50
    drive_with_line_follow(20, pc(7.2, 6))
    msleep(200)

    print("picking up pom 1")
    servo.move(c.ARM, c.ARM_DOWN + 100, 10)  # was originally + 50
    collect_red_pom(c.ARM_DOWN + 60, c.WRIST_POM)  # originally ARM_DOWN +50

    print("picking up pom 2")
    servo.move(c.ARM, c.ARM_DOWN + 60, 10)  # originally + 75
    drive_distance_default(10, 3.5)
    collect_green_pom(c.ARM_DOWN - pc(50, 25), c.WRIST_POM)  # clone used to be 0

    print("picking up pom 3")
    drive_with_line_follow(10, 6)
    collect_red_pom(c.ARM_DOWN - pc(50, 0), c.WRIST_POM)

    print("picking up pom 4")
    drive_with_line_follow(10, pc(6, 6.5))
    collect_green_pom(c.ARM_DOWN + pc(0, 30), c.WRIST_POM)

    print("picking up pom 5")
    drive_with_line_follow(10, pc(6, 6.3))
    collect_red_pom(c.ARM_DOWN + pc(0, 30), c.WRIST_POM)

    print("picking up pom 6")
    drive_with_line_follow(10, pc(6, 6.5))
    collect_green_pom(c.ARM_DOWN + pc(0, 30), c.WRIST_POM)

    print("picking up pom 7")
    drive_with_line_follow(10, 6.5)  # was 6
    collect_red_pom(c.ARM_DOWN + pc(0, 30), c.WRIST_POM)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_OPEN - 400)

    print("picking up pom 8")
    servo.move(c.ARM, c.ARM_DOWN + pc(0, 30), 10)
    servo.move(c.WRIST, c.WRIST_POM, 10)
    drive_with_line_follow(10, pc(5.3, 5))

    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_CLOSED - 100)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_CLOSED + 100)
    servo.move(c.ARM, c.ARM_DOWN + 75, 10)

    drive_distance_default(-25, 3)  # drives back a bit

    servo.move(c.ARM, c.ARM_MAX)  # moves arm up and out of the way
    servo.move(c.WRIST, c.WRIST_DRIVE_UP, 15)
    drive_distance_default(50, pc(20, 20))  # squares up create against the wall


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


def deliver_poms_to_airlock():
    print("deliver poms to airlock")

    print("squaring up create")
    drive_straight(-60, 70)  # drive almost all the way down the board
    drive_timed(-20, 20, pc(1520, 1400))  # spins 90 degrees towards the wall with rings
    drive_straight(60, 19)  # drives forward
    drive_distance_default(35, 3)  # slows down when squaring up against wall, so that wheel doesn't slip
    drive_straight(-40, pc(6.5, 6.5))  # backs up off the wall a bit, used to be 6 for both

    spin(25, 90)  # spins 90 degrees towards the airlock
    msleep(500)

    drive_straight(60, pc(15, 17))  # drives towards wall
    drive_distance_default(35, 3)  # slows down when squaring up against wall
    msleep(500)

    print("moving airlock to proper position")
    drive_straight(-40, pc(15, 16))  # back up far off the wall
    servo.move(c.ARM, c.ARM_DELIVER_HIGH, 15)  # raises arm to the horizontal plane of the airlock
    servo.move(c.WRIST, c.WRIST_DELIVER_HIGH)
    drive_timed(10, -10, 100)  # small spin to face the airlock at the correct angle
    msleep(500)
    drive_straight(30, 9)  # drives in to knock the airlock into place
    msleep(500)
    spin(-5, pc(14, 18))  # small spin towards airlock in order to fully straighten out the airlock
    msleep(500)

    print("moving claw to airlock")
    drive_timed(-10, 10, pc(200, 350))  # small spin away from the airlock
    msleep(250)
    servo.move(c.ARM, c.ARM_MAX)  # arm up so that it avoids hitting the airlock
    msleep(250)
    servo.move(c.WRIST, c.WRIST_MAX)
    msleep(250)
    drive_timed(10, -10, pc(700, 700))  # spin back so that the arm is over the airlock, pc(750, 900)
    msleep(250)
    drive_straight(-40, 8)  # back up away from the airlock
    msleep(250)

    print("delivering poms")
    servo.move(c.WRIST, c.WRIST_DELIVER_HIGH)
    servo.move(c.ARM, c.ARM_DELIVER_HIGH, 10)  # lowers arm
    drive_distance_default(10, pc(3.3, 3.6))  # drive in to deliver on airlock
    msleep(250)
    servo.move(c.WRIST, c.WRIST_DELIVER_FINAL)  # lowers arm and wrist so that it's sitting on the airlock
    servo.move(c.ARM, c.ARM_DELIVER_FINAL, 10)
    servo.move(c.LEFT_WIPER, c.LEFT_WIPER_DELIVER_OPEN, 15)
    servo.move(c.RIGHT_WIPER, c.RIGHT_WIPER_DELIVER_OPEN, 15)

    msleep(500)
    disable_servo(c.LEFT_WIPER)

    drive_timed(10, -10, 90)  # spins clockwise

    msleep(500)
    disable_servo(c.RIGHT_WIPER)

    servo.move(c.ARM, c.ARM_DELIVER_FINAL, 10)  # makes sure that arm is completely down on the airlock


def shut_down():
    print("shutting down")
    create_disconnect()
    disable_servos()
    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()
    print("botguy grab time", botguy_grab_time)
    print("shut down total time", time.time() - t)
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

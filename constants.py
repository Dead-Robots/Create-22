from kipr import digital

IS_PRIME = not digital(0)
IS_CLONE = not IS_PRIME

START_LIGHT = 1
START_LIGHT_THRESHOLD = 0

if IS_PRIME:
    print("I am prime")

    ADJUST_SPEED = 1.0

    # Servo Ports
    ARM = 0
    WRIST = 1
    RIGHT_WIPER = 2
    LEFT_WIPER = 3

    # Motor Ports

    # Servo Positions
    ARM_INIT = 1390
    ARM_START = 600
    ARM_BOTGUY = 2047
    ARM_DOWN = 325 + 25
    ARM_DELIVER_HIGH = 1700 + 70
    ARM_DELIVER_FINAL = 1620
    ARM_CUBES = 1330
    ARM_DELIVER_LOW = 700

    WRIST_START = 1950
    WRIST_UP = 940
    WRIST_BOTGUY = 500
    WRIST_POM = 1950
    WRIST_DELIVER_HIGH = 770
    WRIST_DELIVER_FINAL = 770
    WRIST_CUBES = 1245
    WRIST_DELIVER_LOW = 1800
    WRIST_DRIVE_UP = 1180 # value for wrist to pe perpendicular to ground when driving

    LEFT_WIPER_CLOSED = 400
    LEFT_WIPER_CENTER = 720
    LEFT_WIPER_OPEN = 1120
    LEFT_WIPER_CUBES = 1160
    LEFT_WIPER_DELIVER_OPEN = 700

    RIGHT_WIPER_CLOSED = 1000
    RIGHT_WIPER_CENTER = 800
    RIGHT_WIPER_OPEN = 450
    RIGHT_WIPER_DELIVER_OPEN = 700

    TOPHAT_THRESHOLD = 1000


elif IS_CLONE:
    print("I am clone")

    ADJUST_SPEED = 1.0  # Factor for left motor in drive function

    # Servo Ports
    ARM = 0
    WRIST = 1
    RIGHT_WIPER = 2
    LEFT_WIPER = 3

    # Servo Positions
    ARM_BOTGUY = 2047
    ARM_DOWN = 450 + 50
    ARM_DELIVER_HIGH = 1800
    ARM_DELIVER_FINAL = 1700
    ARM_CUBES = 1330
    ARM_DELIVER_LOW = 700

    WRIST_START = 2000
    WRIST_UP = 940
    WRIST_BOTGUY = 500
    WRIST_POM = 1900  # originally 1773
    WRIST_DELIVER_HIGH = 950 + 25
    WRIST_DELIVER_FINAL = 800
    WRIST_CUBES = 1245
    WRIST_DELIVER_LOW = 1800
    WRIST_DRIVE_UP = 1570 # value for wrist to pe perpendicular to ground when driving

    LEFT_WIPER_CLOSED = 175
    LEFT_WIPER_CENTER = 425
    LEFT_WIPER_OPEN = 860
    LEFT_WIPER_CUBES = 1000 + 100
    LEFT_WIPER_DELIVER_OPEN = 700

    RIGHT_WIPER_CLOSED = 1100
    RIGHT_WIPER_CENTER = 740
    RIGHT_WIPER_OPEN = 450
    RIGHT_WIPER_DELIVER_OPEN = 800

    TOPHAT_THRESHOLD = 1000


else:
    print("Houston, we've got a problem...")
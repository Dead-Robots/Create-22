from kipr import digital

IS_PRIME = not digital(0)
IS_CLONE = not IS_PRIME

START_LIGHT = 1
START_LIGHT_THRESHOLD = 0

# Servo Ports
ARM = 0
WRIST = 1
RIGHT_WIPER = 2
LEFT_WIPER = 3

# Motor Port
BOT_STICK = 3

TOP_HAT = 0

if IS_PRIME:
    print("I am prime")

    ADJUST_SPEED = 1.0

    # Servo Positions
    ARM_INIT = 1390
    ARM_START = 600
    ARM_BOTGUY = 2047
    ARM_DOWN = 475
    ARM_DELIVER_HIGH = 1800
    ARM_DELIVER_FINAL = 1700
    ARM_CUBES = 1330
    ARM_DELIVER_LOW = 700

    WRIST_START = 600
    WRIST_UP = 1955
    WRIST_BOTGUY = 1550
    WRIST_POM = 600
    WRIST_DELIVER_HIGH = 1075
    WRIST_DELIVER_FINAL = 1250
    WRIST_CUBES = 800
    WRIST_DELIVER_LOW = 258
    WRIST_DRIVE_UP = 525 # value for wrist to pe perpendicular to ground when driving

    LEFT_WIPER_CLOSED = 458
    LEFT_WIPER_CENTER = 800
    LEFT_WIPER_OPEN = 1290
    LEFT_WIPER_CUBES = 1170
    LEFT_WIPER_DELIVER_OPEN = 450

    RIGHT_WIPER_CLOSED = 990
    RIGHT_WIPER_CENTER = 740
    RIGHT_WIPER_OPEN = 225
    RIGHT_WIPER_DELIVER_OPEN = 990

    TOPHAT_THRESHOLD = 1000


elif IS_CLONE:
    print("I am clone")

    ADJUST_SPEED = 1.0  # Factor for left motor in drive function

    # Servo Positions
    ARM_BOTGUY = 2047
    ARM_DOWN = 450 + 25
    ARM_DELIVER_HIGH = 1800
    ARM_DELIVER_FINAL = 1700
    ARM_CUBES = 1330
    ARM_DELIVER_LOW = 700

    WRIST_START = 47
    WRIST_UP = 1100
    WRIST_BOTGUY = 1550
    WRIST_POM = 300  # originally 1773
    WRIST_DELIVER_HIGH = 1075
    WRIST_DELIVER_FINAL = 1250
    WRIST_CUBES = 800
    WRIST_DELIVER_LOW = 250
    WRIST_DRIVE_UP = 525  # value for wrist to pe perpendicular to ground when driving
    WRIST_SPIN_UP = 650

    LEFT_WIPER_CLOSED = 100
    LEFT_WIPER_CENTER = 425
    LEFT_WIPER_OPEN = 1325
    LEFT_WIPER_CUBES = 1190
    LEFT_WIPER_DELIVER_OPEN = 700

    RIGHT_WIPER_CLOSED = 1100
    RIGHT_WIPER_CENTER = 740
    RIGHT_WIPER_OPEN = 375
    RIGHT_WIPER_DELIVER_OPEN = 800

    TOPHAT_THRESHOLD = 1000


else:
    print("Houston, we've got a problem...")
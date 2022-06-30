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
    ARM_START = 600
    ARM_MAX = 2047
    ARM_DOWN = 380
    ARM_DELIVER_HIGH = 1660
    ARM_DELIVER_FINAL = 1425
    ARM_CUBES = 1165  # was originally 830
    ARM_DELIVER_LOW = 700

    WRIST_START = 600
    WRIST_UP = 1480
    WRIST_POM = 650
    WRIST_DELIVER_HIGH = 1825
    WRIST_DELIVER_FINAL = 1630
    WRIST_CUBES = 1375  # was originally 900
    WRIST_DELIVER_LOW = 258
    WRIST_DRIVE_UP = 525  # value for wrist to pe perpendicular to ground when driving
    WRIST_MAX = 1600

    LEFT_WIPER_CLOSED = 458
    LEFT_WIPER_CENTER = 800
    LEFT_WIPER_OPEN = 1290
    LEFT_WIPER_CUBES = 1170
    LEFT_WIPER_DELIVER_OPEN = 650 # was 450

    RIGHT_WIPER_CLOSED = 1024
    RIGHT_WIPER_CENTER = 740
    RIGHT_WIPER_OPEN = 225
    RIGHT_WIPER_DELIVER_OPEN = 790 # was 990

    TOPHAT_THRESHOLD = 1000

    BOT_STICK_START = -700


elif IS_CLONE:
    print("I am clone")

    ADJUST_SPEED = 1.0  # Factor for left motor in drive function

    # Servo Positions
    ARM_MAX = 2047
    ARM_DOWN = 430
    ARM_DELIVER_HIGH = 1800
    ARM_DELIVER_FINAL = 1700
    ARM_CUBES = 1330 # was originally 1600
    ARM_DELIVER_LOW = 700

    WRIST_START = 230
    WRIST_UP = 1100
    WRIST_BOTGUY = 1550
    WRIST_POM = 300
    WRIST_DELIVER_HIGH = 1075
    WRIST_DELIVER_FINAL = 1250
    WRIST_CUBES = 800
    WRIST_DELIVER_LOW = 250
    WRIST_DRIVE_UP = 525  # value for wrist to pe perpendicular to ground when driving

    LEFT_WIPER_CLOSED = 575
    LEFT_WIPER_CENTER = 875
    LEFT_WIPER_OPEN = 1475
    LEFT_WIPER_CUBES = 1190
    LEFT_WIPER_DELIVER_OPEN = 935 # originally 700

    RIGHT_WIPER_CLOSED = 1100
    RIGHT_WIPER_CENTER = 740
    RIGHT_WIPER_OPEN = 260 # originally 375
    RIGHT_WIPER_DELIVER_OPEN = 800

    TOPHAT_THRESHOLD = 1000

    BOT_STICK_START = -1000


else:
    print("Houston, we've got a problem...")
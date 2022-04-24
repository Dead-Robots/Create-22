IS_PRIME = True
IS_CLONE = not IS_PRIME


if IS_PRIME:
    print("I am prime")

    ADJUST_SPEED = 1.07

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
    ARM_DOWN = 400
    ARM_DELIVER = 1720
    ARM_CUBES = 1330

    WRIST_START = 2047
    WRIST_UP = 940
    WRIST_BOTGUY = 500
    WRIST_POM = 2020
    WRIST_DELIVER = 770
    WRIST_CUBES = 1245

    LEFT_WIPER_CLOSED = 400
    LEFT_WIPER_CENTER = 900
    LEFT_WIPER_OPEN = 1300
    LEFT_WIPER_CUBES = 1340

    RIGHT_WIPER_CLOSED = 1000
    RIGHT_WIPER_CENTER = 800
    RIGHT_WIPER_OPEN = 450


elif IS_CLONE:
    print("I am clone")

    ADJUST_SPEED = 1.0  # Factor for left motor

    # Servo Ports
    ELBOW = 1
    ARM = 2

    # Motor Ports

    # Servo Positions


else:
    print("Houston, we've got a problem...")
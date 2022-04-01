IS_PRIME = True
IS_CLONE = not IS_PRIME


if IS_PRIME:
    print("I am prime")

    ADJUST_SPEED = 0.94

    # Servo Ports
    ARM = 0
    WRIST = 1
    LEFT_WIPER = 2
    RIGHT_WIPER = 3

    # Motor Ports

    # Servo Positions
    ARM_START = 600
    ARM_BOTGUY = 2047

    WRIST_START = 2047
    WRIST_UP = 940
    WRIST_BOTGUY = 300

    LEFT_WIPER_CLOSED = 800
    LEFT_WIPER_CENTER = 1250
    LEFT_WIPER_OPEN = 1600

    RIGHT_WIPER_CLOSED = 550
    RIGHT_WIPER_CENTER = 250
    RIGHT_WIPER_OPEN = 0


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
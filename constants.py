IS_PRIME = True
IS_CLONE = not IS_PRIME


if IS_PRIME:
    print("I am prime")

    ADJUST_SPEED = 0.93

    # Servo Ports
    WRIST = 0
    WIPER = 1
    ELBOW = 2

    # Motor Ports
    ELEVATOR = 0

    # Servo Positions
    WIPER_LEFT = 100
    WIPER_MIDDLE = 1000
    WIPER_RIGHT = 1900
    WIPER_LEFT_CRUNCH = 0
    WIPER_RIGHT_CRUNCH = 2000

    WRIST_DELIVER = 706
    WRIST_START = 1550
    WRIST_LIFT = 2047
    WRIST_GRAB_BOTGUY = 215
    WRIST_DRIVE = 2000

    ELBOW_DELIVER = 1650
    ELBOW_START = 330
    ELBOW_HOVER = 400
    ELBOW_GRAB_BOTGUY = 2048




elif IS_CLONE:
    print("I am clone")

    ADJUST_SPEED = 0.95  # Factor for left motor

    # Servo Ports
    WRIST = 0
    WIPER = 1
    ELBOW = 2

    # Motor Ports
    ELEVATOR = 0

    # Servo Positions
    WIPER_LEFT = 500
    WIPER_MIDDLE = 1000
    WIPER_RIGHT = 1500

    WRIST_DELIVER = 0
    WRIST_START = 1550

    ELBOW_DELIVER = 1600
    ELBOW_START = 325


else:
    print("Houston, we've got a problem...")
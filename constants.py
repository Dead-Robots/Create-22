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
    WIPER_LEFT = 500
    WIPER_MIDDLE = 1000
    WIPER_RIGHT = 1500
    WIPER_LEFT_CRUNCH = 330
    WIPER_RIGHT_CRUNCH = 1650

    WRIST_DELIVER = 706
    WRIST_START = 1720
    WRIST_LIFT = 2047

    ELBOW_DELIVER = 1500
    ELBOW_START = 330


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
    WRIST_START = 1000

    ELBOW_DELIVER = 1500
    ELBOW_START = 330


else:
    print("Houston, we've got a problem...")
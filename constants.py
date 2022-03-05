IS_PRIME = False
IS_CLONE = not IS_PRIME


if IS_PRIME:
    ADJUST_SPEED = 1

    # Servo Ports
    WIPER = 0

    # Motor Ports
    ELEVATOR = 0

    # Servo Positions
    WIPER_LEFT = 500
    WIPER_MIDDLE = 1000
    WIPER_RIGHT = 1500


elif IS_CLONE:
    ADJUST_SPEED = 0.95  # Factor for left motor

    # Servo Ports
    WIPER = 0

    # Motor Ports
    ELEVATOR = 0

    # Servo Positions
    WIPER_LEFT = 500
    WIPER_MIDDLE = 1000
    WIPER_RIGHT = 1500


else:
    print("Houston, we've got a problem...")
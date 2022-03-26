from kipr import set_servo_position, msleep, get_servo_position


def move(port: int, end_position: int, speed: int = 25):
    """
    For speed, 1 is very slow, and 100 is very fast
    """
    speed = abs(speed)
    current_position = get_servo_position(port)
    if current_position > end_position:
        speed = -speed
    while current_position != end_position:
        if abs(speed) > abs(end_position - current_position):
            current_position = end_position
        else:
            current_position += speed
        set_servo_position(port, current_position)
        msleep(25)

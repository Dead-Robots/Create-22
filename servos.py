from kipr import set_servo_position, msleep, get_servo_position


def move_timed(servo, position, time):
    current_position = get_servo_position(servo)
    iterations = abs(position - current_position)//5
    if iterations == 0:
        print("Position is equal to current position")
        return
    time_per_loop = time//iterations
    for i in range(iterations):
        if current_position > position:
            current_position -= 5
        else:
            current_position += 5
        set_servo_position(servo, current_position)
        msleep(time_per_loop)
    set_servo_position(servo, position)

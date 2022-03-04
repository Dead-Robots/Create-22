from kipr import set_servo_position, msleep, get_servo_position


def move_timed(servo_num, position, time):
    current_position = get_servo_position(servo_num)
    iterations = abs(position - current_position)//5
    time_per_loop = time//iterations
    for i in range(iterations):
        if current_position > position:
            current_position -= 5
        else:
            current_position += 5
        set_servo_position(servo_num, current_position)
        msleep(time_per_loop)
    set_servo_position(servo_num, position)

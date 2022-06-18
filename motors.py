from kipr import motor_power, msleep, freeze, clear_motor_position_counter, get_motor_position_counter


def move_timed(motor_num, speed: int, time):
    motor_power(motor_num, speed)
    msleep(time)
    freeze(motor_num)


def move_motor_till_stall(motor_num, speed):
    clear_motor_position_counter(motor_num)
    motor_power(motor_num, speed)
    counter = 0
    last_position = get_motor_position_counter(motor_num)

    while counter < 4:
        if last_position == get_motor_position_counter(motor_num):
            counter += 1
        else:
            counter = 0
            last_position = get_motor_position_counter(motor_num)
        msleep(25)

    motor_power(motor_num, 0)
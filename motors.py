from kipr import motor_power, msleep, freeze, clear_motor_position_counter, get_motor_position_counter

from utilities import pc


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


def move_motor_to_position(motor_num, speed, position):
    clear_motor_position_counter(motor_num)
    motor_power(motor_num, speed)
    msleep(1000)

    while get_motor_position_counter(motor_num) > position + 200:
        pass
    motor_power(motor_num, pc(7, 6))
    print("reversing the power")

    while get_motor_position_counter(motor_num) > position:
        pass
    # motor_power(motor_num, 0)
    print("bot stick in position")

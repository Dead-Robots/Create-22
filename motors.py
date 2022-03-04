from kipr import motor_power, msleep, freeze


def move_timed(motor_num, speed: int, time):
    motor_power(motor_num, speed)
    msleep(time)
    freeze(motor_num)



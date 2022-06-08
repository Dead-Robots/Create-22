import time
from kipr import msleep, push_button
import constants as c

from createserial.commands import open_create, close_create, reset_create, create_dd
from createserial.serial import open_serial, close_serial
from createserial.shutdown import shutdown_create_in


def stop():
    """Stops robot"""
    create_dd(0, 0)


def wait_for_button():
    print("push button to continue")
    stop()
    while not push_button():
        pass


def debug():
    stop()
    msleep(1000)

    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()

    print("exited")
    exit(0)


def pc(p_value, c_value):
    return p_value if c.IS_PRIME else c_value


def wait_for_button():
    print("push button to continue")
    while not push_button():
        pass
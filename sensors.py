from kipr import analog, push_button, msleep, analog_et
from createserial.commands import read_cliff_signals
import constants as c
import actions as a


def read_cliffs():
    right_cliff_sig, left_cliff_sig = read_cliff_signals()
    print("Right: ", right_cliff_sig, "Left: ", left_cliff_sig)
    return right_cliff_sig, left_cliff_sig


def on_white():
    if analog_et(0) < c.TOPHAT_THRESHOLD:
        return True
    else:
        return False


def calibrate(port):
    print("Press button with light on")
    while not push_button():
        pass
    while push_button():
        pass
    light_on = analog(port)
    print("On value =", light_on)
    if light_on > 200:
        print("Bad calibration")
        return False
    msleep(1000)
    print("Press button with light off")
    while not push_button():
        pass
    while push_button():
        pass
    light_off = analog(port)
    print("Off value =", light_off)
    if light_off < 3000:
        print("Bad calibration")
        return False

    if (light_off - light_on) < 2000:
        print("Bad calibration")
        return False
    c.START_LIGHT_THRESHOLD = (light_off - light_on) / 2
    print("Good calibration! ", c.START_LIGHT_THRESHOLD)
    return True


def wait_4(port):
    print("waiting for light!! ")
    while analog(port) > c.START_LIGHT_THRESHOLD:
        pass


def wait_4_light(ignore=False):
    if ignore:
        a.wait_for_button()
        return
    while not calibrate(c.START_LIGHT):
        pass
    wait_4(c.START_LIGHT)

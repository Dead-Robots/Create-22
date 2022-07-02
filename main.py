#!/usr/local/bin/python3.10 -u
from kipr import msleep

import actions as a
import drive as d
from createserial.commands import open_create
from createserial.serial import open_serial

import utilities


def main():
    a.init()
    a.collect_and_deliver_cubes()
    a.leave_start_box()
    a.collect_poms_new()
    a.deliver_poms_to_airlock()
    a.shut_down()


if __name__ == '__main__':
    main()

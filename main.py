#!/usr/local/bin/python3.10 -u
from kipr import msleep

import actions as act


def main():
    act.init()
    # act.debug()
    act.leave_start_box()
    msleep(100)
    act.sort_poms()
    msleep(1000)
    # act.cross_board()
    # msleep(1000)
    # act.elevator_up()
    # msleep(1000)
    # act.elevator_down()
    act.shut_down()


if __name__ == '__main__':
    main()

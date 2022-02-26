#!/usr/local/bin/python3.10 -u
from kipr import msleep

import actions as act


def main():
    act.init()
    '''act.leave_start_box()
    msleep(1000)
    act.turn_right()
    act.cross_board()'''
    act.some_action()
    act.shut_down()


if __name__ == '__main__':
    main()

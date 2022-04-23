#!/usr/local/bin/python3.10 -u
from kipr import msleep

import actions as a
import drive as d


def main():
    a.init()
    # a.grab_botguy()
    a.leave_start_box()
    a.collect_poms()
    a.deliver_poms()
    a.shut_down()


if __name__ == '__main__':
    main()

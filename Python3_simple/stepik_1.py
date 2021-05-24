#!/usr/bin/env python
# -*- coding: utf-8 -*-

print('The programm will show how much nuts each squirrel gets')


def main():
    print('The entry may be only positive integers, not greater than 10000!!!')
    try:
        squirrels = int(input('Enter amount of the squirrels: '))
        nuts = int(input('Enter amount of the nuts: '))
    except (ValueError, TypeError):
        main()
    if check_input(squirrels, nuts):
        avg = nuts//squirrels
        print('Each squirrel will get {} nut'.format(avg))
    else:
        main()


def check_input(*args):
    '''Checks input conditions '''
    for i in args:
        if i <= 0 or i > 10000:
            return False
    return True

main()
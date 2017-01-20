#!/usr/bin/env python
# Usage: archive.py [rate]
#        rate: poll rate in seconds, defaults to 0.1
# vi: smartindent sw=4 ts=4 sts=4 expandtab

from __future__ import print_function
import sys
import epics
import time
import traceback

from config import (get_timestamp, status_pvname, position_pvnames)


pv_names = (status_pvname,
            ) + tuple(position_pvnames)


def test_archive(pv_names, rate=0.1):
    pv_list = tuple(epics.PV(pv, auto_monitor=False) for pv in pv_names)
    
    # dumb busy-loop implementation
    last_values = None
    while True:
        t0 = time.time()
        values = tuple(pv.get() for pv in pv_list)
        
        if values != last_values:
            if last_values is None:
                print('# {}'.format('\t'.join(pv_names)))
            last_values = values
            print('{}\t{}'.format(get_timestamp(),
                                  '\t'.join(str(val) for val in values)))

        dt = time.time() - t0
        time.sleep(max((rate - dt, 0)))


if __name__ == '__main__':
    try:
        rate = float(sys.argv[1])
    except IndexError:
        rate = 0.1
    
    if rate <= 0.0:
        raise ValueError('Invalid rate specified')
    
    print('# {} started recording'.format(get_timestamp()))
    while True:
        try:
            test_archive(pv_names, rate=rate)
        except KeyboardInterrupt:
            print('# Archive cancelled by user')
            break
        except Exception as ex:
            print('# Archive failed: ({0.__class__.__name__}) {0!s}'.format(ex))
            traceback.print_exc(file=sys.stderr)
            time.sleep(1.)

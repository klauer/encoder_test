#!/usr/bin/env python
# vi: smartindent sw=4 ts=4 sts=4 expandtab

from __future__ import print_function
import epics
import time
import datetime
import traceback

from config import (get_timestamp, 
                    power_on_pvname, power_off_pvname, 
                    position_pvnames,
                    )

pv_on = epics.PV(power_on_pvname, auto_monitor=False)
pv_off = epics.PV(power_off_pvname, auto_monitor=False)
position_pvs = [epics.PV(pvname, auto_monitor=False)
                for pvname in position_pvnames]


def test_incremental(start_delay=60, increment=90, on_time=60):
    off_time = start_delay
    print('# {}'.format('\t'.join(pv.pvname for pv in position_pvs)))
    while True:
        pv_on.put(1)
        print('# On for: {} s'.format(on_time))
        for i in range(on_time):
            print('{}\t{}'.format(get_timestamp(),
                                  '\t'.join(str(pv.get()) for pv in position_pvs)))
            time.sleep(1.0)

        pv_off.put(1)
        print('# Off for {} s'.format(off_time))
        time.sleep(off_time)

        off_time += increment


if __name__ == '__main__':
    while True:
        try:
            test_incremental()
        except KeyboardInterrupt:
            print('# Test cancelled by user')
            break
        except Exception as ex:
            print('# Test failed: ({0.__class__.__name__}) {0!s}'.format(ex))
            traceback.print_exc(file=sys.stderr)
            time.sleep(1.)

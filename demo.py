# Copyright (c) 2015-2016 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from isac import IsacNode, IsacValue

import signal
import sys
import time
from functools import partial
from isac.tools import zmq, green

# ISAC part

n = IsacNode('demo')
values = {}

def isac_update(iv, value, ts, tags):
    print '>>', iv.uri, value, ts, tags
    if value is not None:
        pub.send_multipart([iv.uri, value])
    else:
        pub.send(iv.uri)
    
def make_value(uri):
    values[uri] = IsacValue(n, uri, survey_last_value=False, survey_static_tags=False)
    values[uri].observers += isac_update
    
make_value('action://nucleo-sensor-demo/led/blue/toggle')
make_value('action://nucleo-sensor-demo/led/blue/on')
make_value('action://nucleo-sensor-demo/led/blue/off')

def sigterm_handler(node):
    node.shutdown()
    sys.exit(0)
    
green.signal(signal.SIGTERM, partial(sigterm_handler, n))

# contiki-zmtp part

ctx = zmq.Context()

pub = ctx.socket(zmq.PUB)
pub.setsockopt(zmq.IPV6, 1)
pub.connect('tcp://aaaa::600:fbff:a2df:5d20:8888')

time.sleep(1)

sub = ctx.socket(zmq.SUB)
sub.setsockopt(zmq.IPV6, 1)
sub.setsockopt(zmq.SUBSCRIBE, '')
sub.connect('tcp://aaaa::600:fbff:a2df:5d20:9999')

def read_sub():
    while True:
        data = sub.recv().split('\0')
        print '< ', data
        if data[0] not in values:
            make_value(data[0])
            
        if len(data) > 1:
            values[data[0]].value = data[1:]
        else:
            values[data[0]].value = 1
    
green.spawn(read_sub)

try:
    n.serve_forever()
except KeyboardInterrupt:
    n.shutdown()
    green.sleep(1)

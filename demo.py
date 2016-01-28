# Copyright 2016 - Alidron's authors
#
# This file is part of Alidron.
#
# Alidron is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alidron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Alidron.  If not, see <http://www.gnu.org/licenses/>.

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

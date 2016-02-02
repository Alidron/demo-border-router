# Copyright (c) 2015-2016 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM alidron/alidron-isac
MAINTAINER Axel Voitier <axel.voitier@gmail.com>

RUN apt-get update && apt-get install net-tools

WORKDIR /app
COPY tunslip6 /app/
COPY demo.py /app/

CMD ["/app/tunslip6", "-s", "/dev/ttyACM0", "aaaa::1/64"]

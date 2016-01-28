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

FROM alidron/alidron-isac
MAINTAINER Axel Voitier <axel.voitier@gmail.com>

RUN apt-get update && apt-get install net-tools

WORKDIR /app
COPY tunslip6 /app/
COPY demo.py /app/

CMD ["/app/tunslip6", "-s", "/dev/ttyACM0", "aaaa::1/64"]

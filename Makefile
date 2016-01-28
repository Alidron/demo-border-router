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

image_name = alidron/demo-border-router

container_name = demo-br

run_args = --net=host --device=/dev/ttyACM0:/dev/ttyACM0 --device=/dev/net/tun:/dev/net/tun --privileged

.PHONY: clean clean-dangling build run-bash run-router run-demo stop logs exec

clean:
	docker rmi $(image_name) || true

clean-dangling:
	docker rmi `docker images -q -f dangling=true` || true

build: clean-dangling
	docker build --force-rm=true -t $(image_name) .

run-bash:
	docker run -it --rm --name=$(container_name) $(run_args) $(image_name) bash

run-router:
	docker run -it --rm --name=$(container_name) $(run_args) $(image_name)

run-demo:
	docker exec -it $(container_name) python demo.py

stop:
	docker stop $(container_name)
	docker rm $(container_name)

logs:
	docker logs -f $(container_name)

exec:
	docker exec -it $(container_name) bash
	
	

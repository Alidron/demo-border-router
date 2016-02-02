# Copyright (c) 2015-2016 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
	
	

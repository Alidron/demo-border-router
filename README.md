Demo border router
==================

This is the border router used in the FOSDEM talk.

How to use
==========

```
$ make build
$ make run-router logs
```
At this point, do a reset of the border router board until you see the address of the router printed in the logs of the container. Then do in another terminal:
```
$ make run-demo
```
This will launch the bridge between pure ZeroMQ and Alidron ISAC.

License and contribution policy
===============================

This project is licensed under LGPLv3.

The border router binary tunslip6 comes from Contiki OS project.

To contribute, please, follow the [C4.1](http://rfc.zeromq.org/spec:22) contribution policy.

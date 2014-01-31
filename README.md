domosys_org
===========

DIY Home automation

-work in progress/dirty coder-

What is done/working :

My little house is an semi-ecologic (not so much money) wooden based one,
entirely 3D Blender conceptualized,
already built.
Dry toilets, cleaned 'grey waters' by plants.
Fisches borned in those resulting waters.

Hacked CMV arduino based
Hacked ventilator commanded through a Velleman Dimmer Kit (and Arduino PWM)
some strips LED installed (on Arduino PWM)
an XMPP bot (as Jabber Contact) -called 'Marvin' : see H2G2-
listening for commands, to send corresponding MQTT messages
We can, for now choose the ambiant light depending on what we're doing. 
(just arriving, eating, ... )


Now my goal, is to develop domotics for low Energy consumption 
(optimized low lighting with strip LEDs, 
optimized measures -temperatures, weather's previsions, sun local warming),
to choose between air renewal and kept warming, etc...)
Based on scenars evaluating Sensors, Actuators' status, hour, outdoor's light, temperature, etc...
to choose what is to be done : alert to light on the stove, change automaticaly ambiant lights
alert if the chicken have new eggs, and so on ... 

Having installed (and to install), some (a lot ! ^^') more Sensors and Actuators,
domosys_org is the base of the project,
domosys_web, the django based interface.

What's needed
=============
  * a working PostgreSQL database (with django user access)
  * a simple installation of mosquitto-server
  * some django dependencies (django-celery, ...)
  * pip install tornado

What in the future
==================
  * remove Sensors and Actuators from config page (let it to admin)
  * replace it with Scenars edition
  * Add Aliases system
  * Make Marvin listen to those Aliases
  * Store MQTT statuses
  * plans, materials choices, stove type, 3D, écolo-goals, ... on github (CC)

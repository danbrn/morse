# morse

## description

Simple morse LED blinker. Receives messages via MQTT (tested with Adafruit) and views the messages
by blinking the LoPy4's built-in RGB LED. Color can be specified by starting the message with !! and
a color code (capital R, O, Y, G, B, I, V or W), for example "!!GFrogs are nice." Ignores characters
it doesn't know.

I don't know python, and I don't know git, so... it is what it is.

## important stuff

Runs on the pybytes firmware version 1.20.2.rc7, but doesn't really use any pybytes specific stuff.
Should work on anything connected to WiFi.

Imports private.py which mostly contains info about the MQTT broker to use. Set client_id,
aio_server, aio_user, aio_pass and aio_feed to something usable.

The Morse constructor now takes an optional argument, and if present and not zero, it will output
a pulse-modulated wave on that pin while the LED is turned on (makes a passive piezoelectric buzzer
beep). E.g., if you give the constructor an 11, the program will try to output a 1500Hz PWM on
P11.

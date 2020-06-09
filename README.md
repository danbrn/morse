# morse

Simple morse LED blinker. Receives messages via MQTT (tested with Adafruit) and views the messages
by blinking the LoPy4's built-in RGB LED. Color can be specified by starting the message with !! and
a color code (capital R, O, Y, G, B, I, V or W), for example "!!GFrogs are nice." Ignores characters
it doesn't know.

I don't know python, and I don't know git, so... it is what it is.

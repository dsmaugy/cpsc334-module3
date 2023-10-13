# Lab 6

The ESP32 code sends UDP packets containing the readings from the photoresistor to my laptop on a custom UDP port.
The port, laptop IP, and wireless network information are hardcoded into the ESP32.

The Processing code opens a UDP socket at the specified custom port and transforms the packets into integers, using them to vary the alpha channel values in the shapes on the sketch.

Any firewalls on the laptop need to be disabled/reconfigured to allow the UDP packets to be captured by the socket.

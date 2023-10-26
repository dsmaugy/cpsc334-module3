from pythonosc import udp_client
from time import sleep

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

amen_filter = 200
increase = True

while True:
    if increase:
        amen_filter += 5
        if amen_filter >= 800:
            increase = False

    else:
        amen_filter -= 5
        if amen_filter <= 200:
            increase = True

    osc_client.send_message("/amen_synth", [0.8, 5000])
    sleep(0.01)

from pythonosc import udp_client
from time import sleep
from datetime import datetime, timedelta

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

amen_filter = 200
increase = True

start = datetime.now()

osc_client.send_message("/start_record", None)
while datetime.now() - start < timedelta(seconds=10):
    if increase:
        amen_filter += 5
        if amen_filter >= 800:
            increase = False

    else:
        amen_filter -= 5
        if amen_filter <= 200:
            increase = True

    osc_client.send_message("/amen_synth", [0.8, amen_filter])
    print("Sending amen_synth osc")
    sleep(0.01)

print("sending stop recording osc")
osc_client.send_message("/stop_record", None)



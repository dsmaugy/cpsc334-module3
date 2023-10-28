# The Jungle Lab
The Jungle Lab is an installation piece that allows users to experiment with jungle music/DnB/breakcore in an interactive and non-direct manner. There are two components to this piece, the jungle controller which is a cardboard enclosure featuring sensors and an ESP32, and a host device/RPi running SuperCollider and a PyGame application (pictured above). Approaching users can choose to listen to a previously made 10-second beat sequence, or to record a new one. If they choose to record a new one, they must interact with the device in order to modify the effects on the pre-recorded drum sequence. The audio is not heard immediately however, and can only be listened to once the recording process has finished, mystifying the process behind how the device can be interacted with in order to produce sounds and encouraging the user to experiment multiple times. 

This project is inspired by the [Jungle](https://en.wikipedia.org/wiki/Jungle_music) music genre and its iconic use of filter sweeps and other effects on drum loops.

## Demo

[Quick demo](https://www.youtube.com/watch?v=zphP_vRob-0)

## Relevant Files
`interface.py` - GUI for user interaction, controls recording and playback processes, receives/sends data to ESP32 to coordinate program.

`jungle_scd.scd` - SuperCollider program to generate the user-produced jungle beats. Receives data from ESP32.

`start_jungle.sh` - Bootup script to run all required programs.

## Requirements:
- SuperCollider
- Python
- PyGame

## Attributions:
- Drum Sample: [Amen Break](https://samplefocus.com/samples/breakbeat-vinyl-amen)
- Font: [Jungle Monkey by nailetter](https://www.dafont.com/jungle-monkey.font)
- Interface background: [Windows 95 Jungle Screensaver](https://www.youtube.com/watch?app=desktop&v=FUshV9d5Nq8)

## Writeup:
See [Notion writeup](writeup/The%20Jungle%20Lab.pdf)
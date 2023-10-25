
{SinOsc.ar(500)}.play();


(

var amenBuffer, amenSynth, amenOsc;

amenBuffer = Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "amen.wav");


SynthDef(\amen, {| out = 0, srate = 1, filterfreq = 500 |
    Out.ar(out,
		BPF.ar(PlayBuf.ar(2, b, srate, loop: 1), filterfreq)
    )
}).add();


amenSynth = Synth(\amen);

amenOsc = OSCFunc({ |msg, time, addr, recvPort|
	// srate, filter

	amenSynth.set(\srate, msg[1], \filterfreq, msg[2]);
}, '/amen_synth');
)

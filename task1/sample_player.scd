(

var amenBuffer, amenSynth, amenOsc;

amenBuffer = Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "samples/amen.wav"); // 175 BPM


SynthDef(\amen, {| out = 0, srate = 1, filterfreq = 500 |
    Out.ar(out,
		BPF.ar(PlayBuf.ar(2, amenBuffer, srate, loop: 1), filterfreq)
    )
}).add();




// s.sync; // wait for synthdefs to be added
amenSynth = Synth(\amen);

amenOsc = OSCFunc({ |msg, time, addr, recvPort|
	// srate, filter

	amenSynth.set(\srate, msg[1], \filterfreq, msg[2]);
	msg.postln;
}, '/amen_synth');
)

(
var vistaBuffer, vistaOsc, vistaSynth;

vistaBuffer = Buffer.readChannel(s, thisProcess.nowExecutingPath.dirname +/+ "samples/vista.wav", channels: 0);

SynthDef(\vista, {| out = 0, gate = 1, srate = 1, amp = 1, filterfreq = 500 |
    var env;

    env = EnvGen.kr(
        Env([0, 1, 0], [1, 1], \sin, 1),
        gate,
        levelScale: amp, doneAction: 0);
	Out.ar(out,
		BPF.ar(GrainBuf.ar(1, Impulse.kr(10), rate: srate, dur: 1, pos: 0.4, sndbuf: vistaBuffer, pos: LFNoise2.kr(0.1).range(0, 0.5)
		) * env, filterfreq

		)
	)
}).add();

vistaSynth = Synth(\vista);

vistaOsc = OSCFunc({ |msg, time, addr, recvPort|
	// srate, filter

	vistaSynth.set(\srate, msg[1], \filterfreq, msg[2]);
	// vistaSynth.set(\gate, 0);
	msg.postln;
}, '/amen_synth');

vistaSynth.nodeID.postln;
)



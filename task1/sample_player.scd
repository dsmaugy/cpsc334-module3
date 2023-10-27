(

var amenBuffer, amenSynth, amenOsc;

~currentDir = thisProcess.nowExecutingPath.dirname;
~recordBuffer = Buffer.alloc(s, s.sampleRate * 10, 2);
b = Buffer.read(s, ~currentDir +/+ "samples/amen.wav"); // 175 BPM


SynthDef(\amen, {| out = 0, srate = 1, filterfreq = 500, startPos = 0 |
	var audioOut;
	audioOut = BPF.ar(
			PlayBuf.ar(
				2, b, srate, startPos: startPos, loop: 1),
			filterfreq);

    RecordBuf.ar(audioOut,
		~recordBuffer
    );

	Out.ar(0, audioOut);
}).add();


OSCFunc({ |msg, time, addr, recvPort|
	// srate, filter
	~amenSynth.set(\srate, msg[1], \filterfreq, msg[2]);
}, '/amen_synth');


 OSCFunc({ |msg, time, addr, recvPort|
 	// srate, filter
	"started".postln;
	~amenSynth = Synth(\amen, [\startPos, ~amenBuffer.numFrames.rand]);
 }, '/start_record');



OSCFunc({ |msg, time, addr, recvPort|
	// srate, filter
	~amenSynth.free;
	~recordBuffer.write("/home/darwin/Documents/school/cpsc334/module3/task1/bingus.wav", "WAVE");
}, '/stop_record');

)











(
var yeahBuffer, yeahSynth, yeahOsc;

yeahBuffer = Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "samples/yeah.wav");

SynthDef(\yeah, {| out = 0|
    Out.ar(out,
		PlayBuf.ar(2, ~recordBuffer, 1))
}).add();

yeahSynth = Synth(\yeah);

)

(
var vistaBuffer, vistaOsc, vistaSynth;

vistaBuffer = Buffer.readChannel(s, thisProcess.nowExecutingPath.dirname +/+ "samples/vista.wav", channels: 0);

SynthDef(\vista, {| out = 0, gate = 1, srate = 1, amp = 1, filterfreq = 500 |
    var env;

    env = EnvGen.kr(
        Env.adsr(sustainLevel: 2, releaseTime: 1.5),
        gate, levelScale: amp, doneAction: Done.freeSelf);

	Out.ar(out,
		BPF.ar(GrainBuf.ar(1, Impulse.kr(3.5), rate: srate, dur: 1, pos: 0.4, sndbuf: vistaBuffer, pos: 0.5
		), 500

		) * env
	)
}).add();

~vistaSynth = Synth(\vista);

vistaOsc = OSCFunc({ |msg, time, addr, recvPort|
	// srate, filter

	vistaSynth.set(\srate, msg[1], \filterfreq, msg[2]);
	// vistaSynth.set(\gate, 0);
	msg.postln;
}, '/amen_synth');

p = Pbind(
    \instrument, \vista,
	\srate, Pseq([1.0, 1.0, 1.5, 0.9]),
	// \sustain, Pseq([2.0, 2.0, 0.25, 2.0]),
	\dur, Pseq([1.0, 0.5, 0.20, 1.0]),
	\amp, 5
).play;


)

~vistaSynth.set(\srate, 1.21)




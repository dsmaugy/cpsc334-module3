(

var amenBuffer, amenSynth, amenOsc;
~currentDir = thisProcess.nowExecutingPath.dirname;
~currentDir.postln;

s.waitForBoot({
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

		// Out.ar(0, audioOut);
	}).add();


	OSCFunc({ |msg, time, addr, recvPort|
		// srate, filter
		msg.postln;
		~amenSynth.set(\srate, msg[1], \filterfreq, msg[2]);
	}, '/amen_synth');


	OSCFunc({ |msg, time, addr, recvPort|
		"started".postln;
		~amenSynth = Synth(\amen, [\startPos, b.numFrames.rand]);
	}, '/start_record');



	OSCFunc({ |msg, time, addr, recvPort|
		"stopped".postln;
		~amenSynth.free;
		~recordBuffer.write("/home/darwin/Documents/school/cpsc334/module3/task1/produced_sound.wav", "WAVE");
	}, '/stop_record');

})

)
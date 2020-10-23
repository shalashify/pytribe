# pytribe
Use Korg Electribe 2 as Midi Sequencer to trigger samples from computer.

# Functions

Loads samples from source directory. The structure should be as follows:

<pre>
.
├── 228_Sample_Set_1
│   ├── 08_Kick.wav
│   ├── 09_Snare.wav
│   ├── 10_Shaker.wav
│   ├── 12_Closed_Hat.wav
│   ├── 13_Open_Hat.wav
│   ├── 14_Tom.wav
│   └── readme.txt
├── 229_Sample_Set_2
│   ├── 08_Kick.wav
│   ├── 09_Snare.wav
│   ├── 10_Shaker.wav
│   ├── 12_Closed_Hat.wav
│   ├── 13_Open_Hat.wav
│   ├── 14_Tom.wav
│   └── readme.txt

</pre>

Sample number corresponds to Electribe pad and thus to a Midi Channel.

Sample set number coresponds to Electribe preset number (currently it is not possible to change preset via Preset Knob, thus a default samples set parameter is used)

Midi signals from Electribe are used to trigger respectve samples.

Level knob controls the level of each sample.

Insert FX knob controls master reverb.

Dry and wet sound of the sequence can be recorded by pressing Rec on Electribe.

# Dependencies
- pyo
- mido

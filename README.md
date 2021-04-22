# pytribe
Use Korg Electribe 2 as MIDI Sequencer to trigger samples from computer.

# Functions

MIDI note_on messages from Electribe are used to trigger samples.

Samples are loaded from source directory (configure in .ini file).
Source directory can include multiple sets e.g.

<pre>
.
├── 100_Sample_Set_1
│   ├── 01_Kick.wav
│   ├── 02_Snare.wav
│   ├── 03_Shaker.wav
│   ├── 04_Closed_Hat.wav
│   ├── 05_Open_Hat.wav
│   └── 06_Tom.wav
├── 200_Sample_Set_2
│   ├── 09_Kick.wav
│   ├── 10_Snare.wav
│   ├── 14_Closed_Hat.wav
│   ├── 15_Open_Hat.wav
│   ├── 16_Tom.wav
│   └── readme.txt

</pre>

Number of the set (100, 200) can be selected via command prompt or set via .ini file.

Number of the sample (01, 02, 15) within the set corresponds to Electribe 2 pad number (upper row being 1-8, lower row 9-16).
Number of the sample is thus used to map a sample to a MIDI Channel. Only channels that have samples assigned to them will be treated as relevant. Thus it is possible to trigger samples at computer and play Electribe's own synths in parallel.

Level knob controls of the respective channel at Electribe controls the level of each sample.

# Dependencies
- pygame
- mido

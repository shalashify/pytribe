# pytribe

Use a MIDI Sequencer (tested with Korg Elecrtibe 2 and Teenage Engineering OP-Z) to trigger samples from computer.

Can be useful to arrange and test different sample sets before loading them to the Unit or use computer as a sample player in combination with Electribe synths.

# Functions

MIDI note_on messages are used to trigger samples.

Samples are loaded from source directory (configure in .ini file).
Source directory can include multiple sets e.g.

<pre>
Sample_Dir
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

Number of the sample (01, 02, 15) within the set corresponds to Electribe 2 pad number (upper row being 1-8, lower row 9-16) or OP-Zs track number. Number of the sample is thus used to map a sample to a MIDI Channel. Only channels that have samples assigned to them will be treated as relevant. Thus it is possible to trigger samples at computer and play Electribe's own synths in parallel.

Level knob of the respective channel controls the level of each sample. Make sure to set the level cc value for your device correctly via the .ini file.
Korg Electribe 2: 7
Teenage Engineering OP-Z: 16 

Other cc messages are not yet implemented. See https://teenage.engineering/guides/op-z/midi

# Example

```
amb:pytribe alec$ python3 pytribe.py alec.ini


               _____ ___ ___ ___ ___
      _ __ _  |_   _| _ \_ _| _ ) __|
     | '_ \ || || | |   /| || _ \ _|
     | .__/\_, ||_| |_|_\___|___/___|
     |_|   |__/



Directory: /Users/alec/Music Production/Tools/Samples/pytribe
Contains Sets
  /Users/alec/Music Production/Tools/Samples/pytribe/228_Vinyl_Set_1/
  /Users/alec/Music Production/Tools/Samples/pytribe/229_Vinyl_Set_2/
  /Users/alec/Music Production/Tools/Samples/pytribe/230_Standard_Set_1/
  /Users/alec/Music Production/Tools/Samples/pytribe/300_experiment/
  /Users/alec/Music Production/Tools/Samples/pytribe/232_Standard_Set_3/
  /Users/alec/Music Production/Tools/Samples/pytribe/231_Standard_Set_2/
Which set number to use? (default: 100) 228
Loading: /Users/alec/Music Production/Tools/Samples/pytribe/228_Vinyl_Set_1
   MIDI CHANNEL 09 --> 09_Kick.wav
   MIDI CHANNEL 10 --> 10_Snare.wav
   MIDI CHANNEL 11 --> 11_Shaker.wav
   MIDI CHANNEL 12 --> 12_Closed_Hat.wav
   MIDI CHANNEL 13 --> 13_Open_Hat.wav
   MIDI CHANNEL 15 --> 15_Tom.wav
Ready to rock! Start your Sequencer!
CTRL+C to exit
```

# Dependencies
- pygame
- mido

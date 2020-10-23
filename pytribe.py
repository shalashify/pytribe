"""
pytribe
Use Korg Electribe 2 as Midi Sequencer
to trigger samples from computer
"""

from __future__ import division
import os
import glob
import sys
import mido
import time

from pyo import *

s = Server().boot()
s.start()

do_play = True
do_record = False

samples_dir = "Samples/"
recording_dir = "Rec/"
default_samples_set = "228"

def load_samples(samples_path):
    global samples
    global effects

    default_sample_volumes = [0,0,0,0,0,0,0,30,40,100,100,100,100,30,100]
    default_effect_volume = 10
    samples = [None] * 16
    effects = [None] * 16
    is_loaded = False

    # Check if directory exists
    if(len(glob.glob(samples_path)) == 0):
        return False

    for i in range(15):
       sample_file = glob.glob(samples_path + str(i+1).zfill(2) + "_*.wav")
       if(len(sample_file)>0):
           # Load File into Table
           samples[i] = TableRead(table=SndTable(sample_file[0]), freq=SndTable(sample_file[0]).getRate(), loop=0, mul=float(default_sample_volumes[i]/127))
           # Set Track Effect
           effects[i] = Freeverb(samples[i], size=[.79,.8], damp=.9, bal=.3, mul=float(default_effect_volume/127))
           print("Loaded " + sample_file[0])
           is_loaded = True
    return is_loaded

def rec(recording_dir):
    global recordings
    global samples
    global effects

    recordings = [None] * 16
    for i in range(15):
        if(samples[i] != None):
            recordings[i] = Record(samples[i], recording_dir + str(i+1).zfill(2) + "_dry.wav")
    return True

def play():
    global do_play
    global do_record
    global samples
    global effects
    global recordings

    stop_pressed_times = 0
    inport =  mido.open_input()

    while do_play and inport.iter_pending():
        msg = inport.receive()

        if msg.type == "note_on" and msg.channel >= 8 : # Sequence
            if(samples[msg.channel-1] != None):
                samples[msg.channel-1].out()
                effects[msg.channel-1].out()
        elif msg.type == "control_change" and msg.control == 7 and msg.channel >= 8:  # Level
            samples[msg.channel-1].setMul(float(msg.value/127))
        elif msg.type == "control_change" and msg.control == 87: # master reverb ! not channel specific
            for i in range(15):
                if(effects[i] != None):
                    effects[i].setMul(float(msg.value/127))
        #elif(str(msg) != "clock time=0"):
        #    print(msg)
        elif msg.type == "program_change":
            # reconsider
            # samples_set = samples_dir + str(127 + 1 + msg.program + 1) + "_*/"
            print("RECONSIDER: Trying to load sample set " + str(127 + 1 + msg.program + 1))
            # doesnt work on the fly
            # load_samples(samples_set)
        elif(str(msg) == "stop time=0"):
            if(do_record):
                do_record = False
                for i in range(15):
                    if(recordings[i] != None):
                        recordings[i].stop()
            do_play = False
            print("Stop signal received")

def restart():
    global do_play
    restart = input('Restart? (default: Yes) ') or "Y"
    if(restart in ("Yes", "Y", "Yeah", "y", "yes")):
        do_play = True
        main()
    else:
        os._exit(1)

def main():
    global do_play
    global do_record
    global default_samples_set
    global sample_dir
    global recording_dir

    current_set = input('Sample Set Number? (default: 228) ') or default_samples_set
    samples_path = samples_dir + str(current_set) + "_*/"

    if(load_samples(samples_path)):
        if((input('Record? (default: No) ') or "No") in ("Yes", "Y", "Yeah", "y", "yes")):
            do_record = rec(recording_dir)
        do_play = True
        print('Rock On! Start your Electribe!')
        while do_play:
            play()
            print("Exiting to main, do_play = " + str(do_play) + ", do_record = " + str(do_record))
        restart()
    else:
        print("Samples could not be loaded from: " + samples_path)
        main()

if __name__ == "__main__":
    main()

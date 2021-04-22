"""
pytribe
Use Korg Electribe 2 as MIDI sequencer to trigger samples from computer
"""

from __future__ import division
import os
import glob
import sys
import mido
import time
import pygame
import configparser

pygame.init()
pygame.mixer.init()

do_play = True
midi_in = mido.open_input()

def load_samples(samples_path):
    global samples
    global channels
    global total_channels

    samples = [None] * (total_channels + 1)
    channels = [None] * (total_channels + 1)
    files = [None] * (total_channels + 1)

    is_loaded = False

    # Check if directory exists
    if(len(glob.glob(samples_path)) == 0):
        return False

    # Check wav files
    all_samples = glob.glob(samples_path + "[0-9][0-9]*.wav")

    for sample in all_samples:
        path, file = os.path.split(sample)
        channel = int(file.split("_")[0]) or -1
        if(channel > 0 and channel <= total_channels and len(sample) > 0):
           samples[channel] = pygame.mixer.Sound(sample)
           channels[channel] = pygame.mixer.Channel(channel)
           files[channel] = file
           is_loaded = True

    print("============================================================================")
    print('Loading sample set: ' + path)
    print('Mapped samples:')
    for i in range(len(samples)-1):
        if(files[i] != None):
            print("   MIDI CHANNEL " + str(i).zfill(2) + " --> " + str(files[i]))
    print("============================================================================")

    return is_loaded

def play():
    global do_play
    global samples
    global cc_level
    global midi_in

    while do_play and midi_in.iter_pending():
        msg = midi_in.receive()
        if msg.type == "note_on" :
            #print(msg.channel)
            if(samples[msg.channel + 1] != None):
                channels[msg.channel + 1].play(samples[msg.channel + 1])
        elif msg.type == "control_change":
            if msg.control == cc_level: # level
                if(channels[msg.channel + 1] != None):
                    channels[msg.channel + 1].set_volume(float(msg.value/127))
            else:
                pass # Future logic for other cc
        elif msg.type == "program_change":
            #print(msg.program)
            pass # Future program change logic
        elif(str(msg.type) == "stop"):
            #Possible logic to stop
            #do_play = False
            #print(msg.type)
            pass
        elif(msg.type not in ("note_on", "clock", "note_off")):
            #way to monitor remaining messages
            #print(msg.type)
            pass

def load_config(config_file):
    config = configparser.ConfigParser()

    if(not os.path.isfile(config_file)):
        print("Config file not found " + config_file)
        exit()

    config.read(config_file)

    samples_dir = config['samples'].get('samples_dir', 'Samples')
    default_samples_set = config['samples'].get('default_set', '100')
    total_channels = int(config['midi'].get('total_channels', '[16]'))
    cc_level = int(config['midi'].get('cc_level', '7'))

    return samples_dir, default_samples_set, total_channels, cc_level

def restart():
    global do_play
    restart = input('Load another sample set? (default: Yes) ') or "Y"
    if(restart in ("Yes", "Y", "Yeah", "y", "yes")):
        do_play = True
        main()
    else:
        os._exit(1)

def main():
    global do_play
    global total_channels
    global cc_level

    try:
        if(len(sys.argv) > 1):
            config_file = sys.argv[1] or 'default.ini'
        else:
            config_file = 'default.ini'

        samples_dir, default_samples_set, total_channels, cc_level = load_config(config_file)

        print("============================================================================")
        print("Samples Directory: " + samples_dir)
        print("Following Sets Found: ")
        sample_sets = glob.glob(samples_dir + "/*/")
        for sample_set in sample_sets:
            print("  " + sample_set)

        current_set = input('Which set number to use? (default: ' + default_samples_set + ') ') or default_samples_set
        samples_path = samples_dir + "/" + str(current_set) + "_*/"

        pygame.mixer.set_num_channels(total_channels + 1)

        if(load_samples(samples_path)):
            do_play = True
            print('Ready to rock! Start your Sequencer!')
            print('CTRL+C to exit')
            try:
                play()
            except KeyboardInterrupt:
                restart()
        else:
            print("No samples could be loaded from: " + samples_path)
            main()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

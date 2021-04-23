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

_do_play = True
_midi_in = mido.open_input()

def load_samples(_samples_path):
    global _samples
    global _channels
    global _total_channels

    _samples = [None] * (_total_channels + 1)
    _channels = [None] * (_total_channels + 1)
    _files = [None] * (_total_channels + 1)

    _is_loaded = False

    # Check if directory exists
    if(len(glob.glob(_samples_path)) == 0):
        return False

    # Check wav files
    _all_samples = glob.glob(_samples_path + "[0-9][0-9]*.wav")

    for _sample in _all_samples:
        _path, _file = os.path.split(_sample)
        _channel = int(_file.split("_")[0]) or -1
        if(_channel > 0 and _channel <= _total_channels and len(_sample) > 0):
           _samples[_channel] = pygame.mixer.Sound(_sample)
           _channels[_channel] = pygame.mixer.Channel(_channel)
           _files[_channel] = _file
           _is_loaded = True

    print('Loading: ' + _path)
    for _i in range(len(_samples)):
        if(_files[_i] != None):
            print("   MIDI CHANNEL " + str(_i).zfill(2) + " --> " + str(_files[_i]))

    return _is_loaded

def _play():
    global _do_play
    global _samples
    global _cc_level
    global _midi_in

    while _do_play and _midi_in.iter_pending():
        _msg = _midi_in.receive()
        if _msg.type == "note_on" :
            #print(msg.channel)
            if(_samples[_msg.channel + 1] != None):
                _channels[_msg.channel + 1].play(_samples[_msg.channel + 1])
        elif _msg.type == "control_change":
            if _msg.control == cc_level: # level
                if(_channels[_msg.channel + 1] != None):
                    _channels[_msg.channel + 1].set_volume(float(_msg.value/127))
            else:
                pass # Future logic for other cc
        elif _msg.type == "program_change":
            #print(msg.program)
            pass # Future program change logic
        elif(str(_msg.type) == "stop"):
            #Possible logic to stop
            #do_play = False
            #print(msg.type)
            pass
        elif(_msg.type not in ("note_on", "clock", "note_off")):
            #way to monitor remaining messages
            #print(msg.type)
            pass

def _load_config(_config_file):
    _config = configparser.ConfigParser()

    if(not os.path.isfile(_config_file)):
        print("Config file not found " + _config_file)
        exit()

    _config.read(_config_file)

    _samples_dir = _config['samples'].get('samples_dir', 'Samples')
    _default_samples_set = _config['samples'].get('default_set', '100')
    _total_channels = int(_config['midi'].get('total_channels', '[16]'))
    _cc_level = int(_config['midi'].get('cc_level', '7'))

    return _samples_dir, _default_samples_set, _total_channels, _cc_level

def _restart():
    global _do_play
    _restart = input('Load another sample set? (default: Yes) ') or "Y"
    if(_restart in ("Yes", "Y", "Yeah", "y", "yes")):
        _do_play = True
        _main()
    else:
        os._exit(1)

def _hello():
    #https://patorjk.com/software/taag/#p=display&f=Small&t=pyTRIBE
    _hello = """

               _____ ___ ___ ___ ___
      _ __ _  |_   _| _ \_ _| _ ) __|
     | '_ \ || || | |   /| || _ \ _|
     | .__/\_, ||_| |_|_\___|___/___|
     |_|   |__/


    """
    print(_hello)

def _main():
    global _do_play
    global _total_channels
    global _cc_level
    global _output_line
    try:
        if(len(sys.argv) > 1):
            _config_file = sys.argv[1] or 'default.ini'
        else:
            _config_file = 'default.ini'

        _samples_dir, _default_samples_set, _total_channels, _cc_level = _load_config(_config_file)
        _sample_sets = glob.glob(_samples_dir + "/[0-9]*/")

        print("Directory: " + _samples_dir)
        if(len(_sample_sets) > 0) :
            print("Contains Sets ")
            for _sample_set in _sample_sets:
                print("  " + _sample_set)

            _current_set = input('Which set number to use? (default: ' + _default_samples_set + ') ') or _default_samples_set
            _samples_path = _samples_dir + "/" + str(_current_set) + "_*/"

            pygame.mixer.set_num_channels(_total_channels + 1)

            if(load_samples(_samples_path)):
                _do_play = True
                print('Ready to rock! Start your Sequencer!')
                print('CTRL+C to exit')
                try:
                    _play()
                except KeyboardInterrupt:
                    _restart()
            else:
                print("No samples could be loaded from " + _samples_path)
                _main()
        else:
            print("No sample sets found!")
            print("Naming pattern for a set should be /[0-9]*/ (e.g. 100_set)")
            print("Either correct a path in the ini file or put some sets in")
            os._exit(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    _hello()
    _main()

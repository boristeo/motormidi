#!/usr/bin/env python3

# Code generator for compact MIDI messages to be stored on MCU 
# Run this script on a multichannel (but monophonic) MIDI file
# to get the initializers. note_off represented as note=0

import sys

if '--gen-note-lut' in sys.argv:
  # Microseconds period for MIDI notes
  for i in range(128):
    print(int(1000000 / (440.0 * (2 ** ((i - 69) / 12)))), end=',')
  exit()

import mido
from collections import defaultdict

mid = mido.MidiFile(sys.argv[-1])

playing = defaultdict(bool)
time = 0
output_size = 0

for i, msg in enumerate(mid):
  time += msg.time
  millitime = int(1000 * msg.time)
  if msg.type == 'note_on':
    assert msg.channel <= 7
    print(f'{{{millitime},{msg.note},{msg.channel}}}', end=',')
    if playing[msg.channel]:
      raise RuntimeError(f'polyphony detected in {time} {i}: {msg}')
    playing[msg.channel] = True
    output_size += 1
  elif msg.type == 'note_off':
    print(f'{{{millitime},0,{msg.channel}}}', end=',')
    playing[msg.channel] = False
    output_size += 1

print(output_size, file=sys.stderr)
  

  


  

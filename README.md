# Soundy
Funny little step sequencer thing that uses Tkinter and Simpleaudio!

![image](https://github.com/Prezzodaman/soundy/assets/76560493/0d7dc571-fe90-4283-832e-a60dc26f7418)

## Features
* Sequencing of one-shot sounds
* Very wonky timing that depends on how many sounds are playing at once
* A layering/phasing option for each sound, allowing for the same sound to be played numerous times on each step
* Mutes and unmutes
* A monophonic mode for each sound which almost works (because when the sound plays again, it doesn't cut out immediately)
* Extremely naive "overflow" feature that attempts to stop too many sounds playing at once (which can still happen, crashing the sound driver)

Thus, based on these features, Soundy is a highly professional music tool that's useful for all occasions.

## Usage
`python3 soundy.py <path to sounds> <number of steps>`

If the path contains sounds with an odd sample rate, they will be excluded. If there are more than 16 sounds, a random selection is used instead. That's so it doesn't fill up the display with a large amount of sounds! The amount of steps can range from 8 to 64.

This has only been tested on Debian 12 with PulseAudio. Your mileage may vary with other OSes and sound drivers!

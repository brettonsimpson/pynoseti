print('\nWelcome to PyNOSETI!\n')
print('1: Generate a video file for a PANOSETI recording')
print('2: Generate a log of photoelectron events')
print('3: Preprocess a directory of .pcapng files\n')
input = int(input('Enter the integer corresponding to the action you would like to do: '))

from functions import *
from playback import playback_function

if input == 1:
    playback_function()

elif input == 2:
    exit()

elif input == 3:
    exit()
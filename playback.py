import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import subprocess
from functions import *
import reader

'''
with open('reader.py') as reader:
    script = reader.read()

exec(script)

image_list = reader_function()
'''



image_list = reader_function

fig, ax = plt.subplots()
im = ax.imshow(image_list[0], cmap='viridis', vmin=0)
cbar = fig.colorbar(im, ax=ax, orientation='vertical')
title = ax.set_title('Frame 0 of '+str(len(image_list)))

def animate(i):
    im.set_array(image_list[i])
    ax.set_title(f'Frame {i} of '+str(len(image_list)))
    im.set_array(image_list[i])
    return [im, ax]
animation_test = animation.FuncAnimation(fig, animate, frames=len(image_list), interval=50, blit=False)
plt.show()

'''

else:
quabo_list = []
for address in quabo_address_list:
    quabo_list.append(Quabo(address, []))

i=0
temp_list = []
bar = progressbar.ProgressBar(max_value=len(packet_array)-1)
for packet in packet_array:

    if get_image_source_ip(packet) in quabo_address_list:
        temp_list.append(row_splitter(packet))

    bar.update(i)
    i+=1

'''

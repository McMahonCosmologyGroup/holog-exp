'''
Functions for operating two synthesizers via USB connection for holography experiment. 

Grace E. Chesmore
July 19, 2021
'''

import usb.core
import usb.util
import time
import numpy as np
import struct

def set_RF_output(device,state): #for state, e.g. '1' for command '0x02' will turn ON the RF output. 
    print('Setting RF output')
    n_bytes = 2 #number of bytes remaining in the packet
    n_command = 0x02 #the command number, such as '0x02' for RF output control.
    data=bytearray(64)
    data[0]=ENDPOINT_HEX # I do think this has to be included and here, because excluding endpoint as data[0] makes the synth not change its draw of current. 
    data[1]=n_bytes
    data[2]=n_command
    data[3]=state
    LOs[int(device)].write(ENDPOINT_DEC,data)
    return

def reset_RF(state): #for state, e.g. '1' for command '0x02' will turn ON the RF output. 
    print('Resetting RF')
    n_bytes = 2 #number of bytes remaining in the packet
    n_command = 0x03 #the command number, such as '0x02' for RF output control.
    data=bytearray(64)
    data[0]=ENDPOINT_HEX
    data[1]=n_bytes
    data[2]=n_command
    data[3]=0x00#state
    dev.write(ENDPOINT_DEC,data)
    return

def set_100_output(state): #for state, e.g. '1' for command '0x02' will turn ON the RF output. 
    print('Setting 100MHz output to state '+str(state)) 
    n_bytes = 2 #number of bytes remaining in the packet
    n_command=0x58 #the command number, such as '0x02' for RF output control.
    data=bytearray(64)
    data[0]=ENDPOINT_HEX#chr(ENDPOINT)
    data[1]=n_bytes
    data[2]=0x1e#n_command
    data[3]=state
    dev.write(ENDPOINT_DEC,str(data))
    return

def set_f(device,f): #sets frequency output of synth
    print('Setting frequency to '+str(f)+' MHz')
    n_bytes = 6 #number of bytes remaining in the packet
    n_command = 0x01 #the command number, such as '0x02' for RF output control.
    bytes = [hex(ord(b)) for b in struct.pack('>Q',(f*1.E6))]#Q is unsigned long long and has std size 8, we only ever use last 5 elements. 
    data=bytearray(64)
    data[0]=ENDPOINT_HEX
    data[1]=n_bytes
    data[2]=n_command
    ISTRT=3
    print('in set_f, bytes = :'+str(bytes))
    ii = 0
    while (ii < 5):
        data[int(ii+ISTRT)]=int(bytes[ii+ISTRT],16)
        ii=ii+1

    LOs[int(device)].write(ENDPOINT_DEC,data)
    return

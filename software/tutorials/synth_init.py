'''
Initializing two synthesizers via USB connection for holography experiment. 

Grace E. Chesmore
July 19, 2021
'''

import usb.core
import numpy as np
import synth

ENDPOINT_DEC=2 # always 2 according to user manual. 
ENDPOINT_HEX=0x02

N = 9
F_TEST = 90 # GHz
F_OFFSET = 10 # MHz
F =int(F_TEST.*1000./N) # MHz 

# Contact the synthesizer USB ports
LOs = tuple(usb.core.find(find_all=True, idVendor=0x10c4, idProduct=0x8468))
print(LOs)
print LOs[0].bus, LOs[0].address
print LOs[1].bus, LOs[1].address

# Was device found?
if ((LOs[0] is None) or (LOs[1] is None)):
    raise ValueError('Device not found.')
else:
    print(str(np.size(LOs))+' device(s) found:')

ii=0
while (ii< np.size(LOs)):
    LOs[ii].reset()
    reattach = False #Make sure the USB device is ready to receive commands.
    if LOs[ii].is_kernel_driver_active(0):
        reattach = True
        LOs[ii].detach_kernel_driver(0)
    LOs[ii].set_configuration()
    ii=ii+1

synth.set_RF_output(0,1) #Turn on the RF output. (device,state)
synth.set_RF_output(1,1)

synth.set_f(0,F) #Set the frequency of the RF output, in MHz. (device, state) You must have the device's RF output in state (1) before doing this. 
synth.set_f(1,int(F+F_OFFSET))

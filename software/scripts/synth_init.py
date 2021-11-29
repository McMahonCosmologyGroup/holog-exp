import usb.core
import usb.util
import time
import numpy as np
import struct
import synth
# Note for Shreya: things to change: N, F = int(x. * 1000. / N)
N = 8
# ENDPOINT_DEC=2 #, always. according to user manual.
# ENDPOINT_HEX=0x02
F_OFFSET = 10#in MHz
F =int(90.*1000./N) #MHz

LOs = tuple(usb.core.find(find_all=True, idVendor=0x10c4, idProduct=0x8468))
print(LOs)
print(LOs[0].bus, LOs[0].address)
print(LOs[1].bus, LOs[1].address)

#dev = usb.core.find(idVendor=0x10c4, idProduct=0x8468) #Values from Syntonic user manual, in decimal. VID = hex(4292) PID = hex(33896)
#Was device found?
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

synth.set_RF_output(0,0,LOs) #Turn on the RF output. (device,state)
synth.set_RF_output(1,0,LOs)
synth.set_f(0,F,LOs)

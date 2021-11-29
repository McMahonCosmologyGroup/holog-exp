import struct
import usb.core
import numpy as np

class SynthOpt:
    ENDPOINT_DEC=2 #, always. according to user manual.
    ENDPOINT_HEX=0x02
    IGNORE_PEAKS_BELOW = int(655)
    IGNORE_PEAKS_ABOVE = int(660)
    F_OFFSET = 10

def set_RF_output(device,state,LOs): #for state, e.g. '1' for command '0x02' will turn ON the RF output.
	print('Setting RF output')
	n_bytes = 2 #number of bytes remaining in the packet
	n_command = 0x02 #the command number, such as '0x02' for RF output control.
	data=bytearray(64)
	data[0]=SynthOpt.ENDPOINT_HEX # I do think this has to be included and here, because excluding SynthOpt.ENDPOINT as data[0] makes the synth not change its draw of current.
	data[1]=n_bytes
	data[2]=n_command
	data[3]=state

	LOs[int(device)].write(SynthOpt.ENDPOINT_DEC,data)
	return

def reset_RF(state): #for state, e.g. '1' for command '0x02' will turn ON the RF output.
	print('Resetting RF')
	n_bytes = 2 #number of bytes remaining in the packet
	n_command = 0x03 #the command number, such as '0x02' for RF output control.
	data=bytearray(64)
	data[0]=SynthOpt.ENDPOINT_HEX
	data[1]=n_bytes
	data[2]=n_command
	data[3]=0x00#state
	dev.write(SynthOpt.ENDPOINT_DEC,data)
	return

def set_f(device,f,LOs): #sets frequency output of synth
	# print('Setting frequency to '+str(f)+' MHz')
	n_bytes = 6 #number of bytes remaining in the packet
	n_command = 0x01 #the command number, such as '0x02' for RF output control.
	bytes = [hex(ord(b)) for b in struct.pack('>Q',(f*1.E6))]#Q is unsigned long long and has std size 8, we only ever use last 5 elements.

	data=bytearray(64)
	data[0]=SynthOpt.ENDPOINT_HEX
	data[1]=n_bytes
	data[2]=n_command
	ISTRT=3
	# print('in set_f, bytes = :'+str(bytes))
	ii = 0
	while (ii < 5):
		data[int(ii+ISTRT)]=int(bytes[ii+ISTRT],16)
		# print(data[int(ii+ISTRT)])
		ii=ii+1

	LOs[int(device)].write(SynthOpt.ENDPOINT_DEC,data)
	return

def get_LOs():
    ### #prepare synths ###
    LOs = tuple(usb.core.find(find_all=True, idVendor=0x10c4, idProduct=0x8468))
    print(LOs[0].bus, LOs[0].address)
    print(LOs[1].bus, LOs[1].address)
    if ((LOs[0] is None) or (LOs[1] is None)): #Was device found?
        raise ValueError('Device not found.')
    else:
        print(str(np.size(LOs))+' device(s) found:')

    ii=0
    while (ii< np.size(LOs)): #Make sure the USB device is ready to receive commands
        LOs[ii].reset()
        reattach = False
        if LOs[ii].is_kernel_driver_active(0):
            reattach = True
            LOs[ii].detach_kernel_driver(0)
        LOs[ii].set_configuration()
        ii=ii+1
    return LOs

def read_f(device,LOs): #sets frequency output of synth
	# print('Setting frequency to '+str(f)+' MHz')
	# n_bytes = 6 #number of bytes remaining in the packet
	# n_command = 0x01 #the command number, such as '0x02' for RF output control.
	# bytes = [hex(ord(b)) for b in struct.pack('>Q',(f*1.E6))]#Q is unsigned long long and has std size 8, we only ever use last 5 elements.
	# data=bytearray(64)
	# data[0]=SynthOpt.ENDPOINT_HEX
	# data[1]=n_bytes
	# data[2]=n_command
    print(LOs[int(device)])
    print(LOs[int(device)].read(SynthOpt.ENDPOINT_DEC))
    return

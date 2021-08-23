import casperfpga
import time
import numpy
import struct
import sys
import logging
import array
import os
import numpy as np
import datetime
import serial
import usb.core
import usb.util
import datetime
import getpass
import matplotlib
matplotlib.use('TkAgg') # do this before importing pylab
import matplotlib.pyplot as plt
import xy_agent.xy_connect as stage
stage_xy = stage.XY_Stage.latrt_xy_stage()

stage_xy.enable()

steps_per_cm = 1574.80316

def running_mean(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]
   
def beam2d(fre,angle,step,label):

    stage_xy.position = [0,0]

    now = datetime.datetime.now()
    today = str(now.day) + '-' +str(now.month) + '-'+str(now.year)

    def running_mean(x, N):
        return np.convolve(x, np.ones((N,))/N)[(N-1):]

    L_MEAN = 1
    NREP = 1
    N_TO_AVG = 1
    N_MULT = 8
    F_START= int(fre*1000./N_MULT) #in MHz
    F_STOP = F_START
    F_OFFSET = 10 #in MHz
    freq = F_STOP
    DELTA_T_USB_CMD = 0.5
    IGNORE_PEAKS_BELOW = int(655)
    IGNORE_PEAKS_ABOVE = int(660)
    #IGNORE_PEAKS_BELOW = int(986)
    #IGNORE_PEAKS_ABOVE = int(990)
    T_BETWEEN_DELTA_F = 0.5
    T_BETWEEN_SAMP_TO_AVG = 0.5
    T_TO_MOVE_STAGE = 1
    DELTA_T_VELMEX_CMD = 0.25
    ENDPOINT_DEC=2 #, always. according to syntonic user manual. 
    ENDPOINT_HEX=0x02
    
    DELTA_X_Y = step*np.round(steps_per_cm)/steps_per_cm
    X_MIN_ANGLE = -angle*DELTA_X_Y/step
    X_MAX_ANGLE = angle*DELTA_X_Y/step
    Y_MIN_ANGLE = -angle*DELTA_X_Y/step
    Y_MAX_ANGLE = angle*DELTA_X_Y/step
    PHI_MIN_ANGLE =0
    PHI_MAX_ANGLE = 0#90.
    DELTA_PHI = 90
  
    N_CHANNELS= 21 
    
    N_PTS = (X_MAX_ANGLE - X_MIN_ANGLE)/DELTA_X_Y +1
    
    prodX = prodY = prodPHI = 0
    if X_MIN_ANGLE == X_MAX_ANGLE:
        prodX = 1
    else:
        prodX = int(abs(X_MAX_ANGLE - X_MIN_ANGLE)/DELTA_X_Y +1)
    if Y_MIN_ANGLE == Y_MAX_ANGLE:
        prodY = 1
    else:
        prodY = int(abs(Y_MAX_ANGLE - Y_MIN_ANGLE)/DELTA_X_Y +1)
    if PHI_MIN_ANGLE == PHI_MAX_ANGLE:
        prodPHI = 1
    else:
        prodPHI = 1 #int(abs(PHI_MAX_ANGLE - PHI_MIN_ANGLE)/DELTA_PHI + 1)

    nfreq = int(abs(F_START - F_STOP)*10 + 1)
    nsamp = int( prodX * prodY * prodPHI )

    print('nsamp = '+str(nsamp)) 
    STR_FILE_OUT = '../Data/1D_Beam_Map/'+str(fre)+'GHz_'+str(angle)+'deg_2D_'+label+today+'.txt'
    arr2D_all_data=np.zeros((nsamp,(4*N_CHANNELS+7)))#, where the 7 extra are f,x,y,phi,... x_cur,y_cur, index_signal of peak cross power in a single bin (where phase is to be measured)

    REGISTER_LO_1 = 5000 #Labjack register number for the Labjack DAC0 output, which goes to LO_1.
    REGISTER_LO_2 = 5002 #Labjack register number for the Labjack DAC1 output, which goes to LO_2.
    ################################################################## 
    # 	Roach Definitions
    ##################################################################
    F_CLOCK_MHZ = 500
    f_max_MHz = (F_CLOCK_MHZ/4)
    KATCP_PORT=7147

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


    def set_f(device,ff): #sets frequency output of synth
        #print('Setting frequency to '+str(int(ff*N_MULT)/1000.)+' GHz, raw of this is: '+str(ff)+' MHz')
        n_bytes = 6 #number of bytes remaining in the packet
        n_command = 0x01 #the command number, such as '0x02' for RF output control.
        bytes = [hex(ord(b)) for b in struct.pack('>Q',(ff*1.E6))]#Q is unsigned long long and has std size 8, we only ever use last 5 elements. 	
        data=bytearray(64)
        data[0]=ENDPOINT_HEX
        data[1]=n_bytes
        data[2]=n_command
        ISTRT=3
        #print('in set_f, bytes = :'+str(bytes))
        ii = 0
        while (ii < 5):
            data[int(ii+ISTRT)]=int(bytes[ii+ISTRT],16)
            ii=ii+1

        LOs[int(device)].write(ENDPOINT_DEC,data)
        return


    def exit_fail():
        print 'FAILURE DETECTED. Log entries:\n',lh.printMessages()
        try:
            fpga.stop()
        except: pass
        raise
        exit()

    def exit_clean():
        try:
            fpga.stop()
        except: pass
        exit()

    def get_data(baseline):
        #print('   start get_data function')
        acc_n = fpga.read_uint('acc_num')
        print '   Grabbing integration number %i'%acc_n

        #get cross_correlation data...    
        a_0r=struct.unpack('>512l',fpga.read('dir_x0_%s_real'%baseline,2048,0))
        a_1r=struct.unpack('>512l',fpga.read('dir_x1_%s_real'%baseline,2048,0))
        a_0i=struct.unpack('>512l',fpga.read('dir_x0_%s_imag'%baseline,2048,0))
        a_1i=struct.unpack('>512l',fpga.read('dir_x1_%s_imag'%baseline,2048,0))
        b_0i=struct.unpack('>512l',fpga.read('dir_x0_%s_imag'%baseline,2048,0))
        b_1i=struct.unpack('>512l',fpga.read('dir_x1_%s_imag'%baseline,2048,0))
        b_0r=struct.unpack('>512l',fpga.read('dir_x0_%s_real'%baseline,2048,0))
        b_1r=struct.unpack('>512l',fpga.read('dir_x1_%s_real'%baseline,2048,0))
        interleave_cross_a=[]
        interleave_cross_b=[]

        #get auto correlation data (JUST the A, B inputs)...
        a_0=struct.unpack('>512l',fpga.read('dir_x0_bb_real',2048,0))
        a_1=struct.unpack('>512l',fpga.read('dir_x1_bb_real',2048,0))
        b_0=struct.unpack('>512l',fpga.read('dir_x0_dd_real',2048,0))
        b_1=struct.unpack('>512l',fpga.read('dir_x1_dd_real',2048,0))
        interleave_auto_a=[]
        interleave_auto_b=[]


        #interleave cross-correlation and auto correlation data.
        for i in range(512):
            #cross
            interleave_cross_a.append(complex(a_0r[i], a_0i[i]))
            interleave_cross_a.append(complex(a_1r[i], a_1i[i]))
            interleave_cross_b.append(complex(b_0r[i], b_0i[i]))#For phase, new, test.
            interleave_cross_b.append(complex(b_1r[i], b_1i[i]))#For phase, new, test

            #auto
            interleave_auto_a.append(a_0[i])#'interleave' even and odd timestreams back into the original timestream (b.c. sampling rate is 2x your FPGA clock). 
            interleave_auto_a.append(a_1[i])
            interleave_auto_b.append(b_0[i])#'interleave' even and odd timestreams back into the original timestream (b.c. sampling rate is 2x your FPGA clock). 
            interleave_auto_b.append(b_1[i])

        #print('   end get_data function')
        return acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b

    def drawDataCallback(baseline):
        #print('running get_data  function from drawDataCallback')
        acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b= get_data(baseline)
        val=running_mean(np.abs(interleave_cross_a),L_MEAN)
        val[int(IGNORE_PEAKS_ABOVE):]=0
        val[: int(IGNORE_PEAKS_BELOW)]=0
        arr_index_signal = np.argpartition(val, -2)[-2:]
        index_signal = arr_index_signal[1]
        # IS THIS NECESSARY? Probably not here, at least. freq = numpy.linspace(0,f_max_MHz,len(numpy.abs(interleave_cross_a)))
        arr_ab = (np.abs(interleave_cross_a))
        arr_phase = (180./np.pi)*np.unwrap((np.angle(interleave_cross_b)))
        phase_signal = arr_phase[index_signal]
        arr_aa = (np.abs(interleave_auto_a))
        arr_bb = (np.abs(interleave_auto_b))

        #Only record relevant channels, right around peak:
        arr_aa = arr_aa[(index_signal - (N_CHANNELS/2)) : (1+index_signal + (N_CHANNELS/2))]
        arr_bb = arr_bb[(index_signal - (N_CHANNELS/2)) : (1+index_signal + (N_CHANNELS/2))]
        arr_ab = arr_ab[(index_signal - (N_CHANNELS/2)) : (1+index_signal + (N_CHANNELS/2))]
        arr_phase = arr_phase[(index_signal - (N_CHANNELS/2)) : (1+index_signal + (N_CHANNELS/2))]

        return running_mean(arr_aa,L_MEAN),running_mean(arr_bb,L_MEAN),running_mean(arr_ab,L_MEAN), arr_phase, index_signal

    def TakeAvgData():
        arr_phase= np.zeros((N_CHANNELS,1))
        arr_aa= np.zeros((N_CHANNELS,1))
        arr_bb= np.zeros((N_CHANNELS,1))
        arr_ab= np.zeros((N_CHANNELS,1))
        arr_index =np.zeros((1,1))

        arr2D_phase= np.zeros((N_TO_AVG,N_CHANNELS))#array of phase data, which I will take the mean of
        arr2D_aa=np.zeros((N_TO_AVG,N_CHANNELS))
        arr2D_bb=np.zeros((N_TO_AVG,N_CHANNELS))
        arr2D_ab=np.zeros((N_TO_AVG,N_CHANNELS))
        arr2D_index= np.zeros((N_TO_AVG,1))
        j = 0
        #to average according to each unique index of peak signal, rather than taking mean at the mean value of index of peak signal
        arr_var_unique =np.zeros((N_TO_AVG,1)) # A test to see how well we can use mean data over 'N_TO_AVG'. 
        while (j < N_TO_AVG):
            #print('In TakeAvgData(), j = ('+str(j)+'/N_TO_AVG)'+' and we are about to drawDataCallback')
            arr2D_aa[j],arr2D_bb[j],arr2D_ab[j],arr2D_phase[j], arr2D_index[j]=drawDataCallback(baseline) 
            #^^^^take in data from the roach. see function "drawDataCallback" above for how this works. "arr2D" array take in data across all frequency bins of the roach. 
            j = j+1    

        arr_phase=arr2D_phase.mean(axis=0)
        arr_aa=arr2D_aa.mean(axis=0)
        arr_bb=arr2D_bb.mean(axis=0)
        arr_ab=arr2D_ab.mean(axis=0)
        arr_index=arr2D_index.mean(axis=0)

        return arr_aa, arr_bb, arr_ab, arr_phase, arr_index
    def MakeBeamMap(i_f, f):
        i=0
        print('begin MakeBeamMap() for f = '+str(f))
        set_f(0,f)
        set_f(1,f + F_OFFSET)

        #phi = 0
        #In the future, possibly add min/max angle control for this, but first
        #need to change the code to modify the move commands at the beginning
        #and end for leaving and returning to the home position
        arr_phase= np.zeros((N_CHANNELS,1))
        arr_aa= np.zeros((N_CHANNELS,1))
        arr_bb= np.zeros((N_CHANNELS,1))
        arr_ab= np.zeros((N_CHANNELS,1))
        index_signal = 0
        #arr_real = numpy.zeros((N_CHANNELS,1))
        #arr_im = numpy.zeros((N_CHANNELS,1))

        print(' move x to minimum angle')
        if X_MIN_ANGLE != 0:
            stage_xy.move_x_cm(X_MIN_ANGLE,1) #Move motor 1 (our x axis) by X_MIN_ANGLE degrees.
            stage_xy.wait()
        print(' move y to minimum angle')
        if Y_MIN_ANGLE !=0:
            stage_xy.move_y_cm(Y_MIN_ANGLE,1) #Move motor 1 (our y axis) by Y_MIN_ANGLE degrees.
            stage_xy.wait()
        for y in np.linspace(Y_MIN_ANGLE,Y_MAX_ANGLE, int(N_PTS)):    
                for x in np.linspace(X_MIN_ANGLE,X_MAX_ANGLE, int(N_PTS)):
                    
                    # Read out current x y position
                    position = np.array(stage_xy.position)
                    x_cur = position[0]
                    y_cur = position[1]
                    
                    phi = 90
                    print(' Recording data: f: '+str(f)+'), x: ('+str(x)+'/'+str(X_MAX_ANGLE)+'), y: ('+str(y)+'/'+str(Y_MAX_ANGLE)+',...')
                    arr_aa, arr_bb, arr_ab, arr_phase,index_signal = TakeAvgData()
                    arr2D_all_data[i] = ([f]+[x]+[y]+[x_cur]+[y_cur]+[phi]+[index_signal]+arr_aa.tolist()+arr_bb.tolist()+arr_ab.tolist()+arr_phase.tolist())
                    i = i+1
                    print('    ...done. ('+str(i)+'/'+str(nsamp)+')')

                    if (x < X_MAX_ANGLE):
                        print('moving x forward')
                        if abs(DELTA_X_Y) !=0:
                            stage_xy.move_x_cm(DELTA_X_Y,1) #Move motor 1 (our x axis) by X_MIN_ANGLE degrees.
                            stage_xy.wait()
                
                print('moving x backward.')
                if abs(X_MAX_ANGLE-X_MIN_ANGLE) != 0: 
                    pos = stage_xy.position
                    desired_x_pos = X_MIN_ANGLE
                    move_x = pos[0]-desired_x_pos
                    stage_xy.move_x_cm(-move_x,1) #Move motor 1 (our x axis) by X_MIN_ANGLE degrees.
                    stage_xy.wait()
                if (y < Y_MAX_ANGLE):
                    print('moving y forward')
                    stage_xy.move_y_cm(DELTA_X_Y,1) #Move motor 1 (our x axis) by X_MIN_ANGLE degrees.
                    stage_xy.wait()
        
        print(' returning y home')
        if abs(Y_MAX_ANGLE) != 0: 
            pos = stage_xy.position
            desired_y_pos = 0
            move_y = pos[1]-desired_y_pos
            stage_xy.move_y_cm(-move_y,1) #Move motor 1 (our x axis) by X_MIN_ANGLE degrees.
            stage_xy.wait()
        print(' returning x home')
        if abs(X_MAX_ANGLE) != 0: 
            pos = stage_xy.position
            desired_x_pos = 0
            move_x = pos[0]-desired_x_pos
            stage_xy.move_x_cm(-move_x,1) #Move motor 1 (our x axis) by X_MIN_ANGLE degrees.
            stage_xy.wait()

        print(' end f = '+str(f))

    # debug log handler
    class DebugLogHandler(logging.Handler):
        """A logger for KATCP tests."""

        def __init__(self,max_len=100):
            """Create a TestLogHandler.
                @param max_len Integer: The maximum number of log entries
                                        to store. After this, will wrap.
            """
            logging.Handler.__init__(self)
            self._max_len = max_len
            self._records = []

        def emit(self, record):
            """Handle the arrival of a log message."""
            if len(self._records) >= self._max_len: self._records.pop(0)
            self._records.append(record)

        def clear(self):
            """Clear the list of remembered logs."""
            self._records = []

        def setMaxLen(self,max_len):
            self._max_len=max_len

        def printMessages(self):
            for i in self._records:
                if i.exc_info:
                    print '%s: %s Exception: '%(i.name,i.msg),i.exc_info[0:-1]
                else:    
                    if i.levelno < logging.WARNING: 
                        print '%s: %s'%(i.name,i.msg)
                    elif (i.levelno >= logging.WARNING) and (i.levelno < logging.ERROR):
                        print '%s: %s'%(i.name,i.msg)
                    elif i.levelno >= logging.ERROR: 
                        print '%s: %s'%(i.name,i.msg)
                    else:
                        print '%s: %s'%(i.name,i.msg)
    ################################
    # MAIN
    ################################

    if __name__ == '__main__':
        from optparse import OptionParser

        p = OptionParser()
        p.set_usage('poco_init_new.py')
        p.set_description(__doc__)
        p.add_option('-c', '--cross', dest='cross', type='str',default='bd',
            help='Plot this cross correlation magnitude and phase. default: bd')
        roach='192.168.4.20'
        baseline='bd'

    try:
        loggers = []
        lh=DebugLogHandler()
        logger = logging.getLogger(roach)
        logger.addHandler(lh)
        logger.setLevel(10)

        print('Connecting to server %s ... '%(roach)),
        fpga = casperfpga.katcp_fpga.KatcpFpga(roach)
        time.sleep(1)

        if fpga.is_connected():
            print 'ok\n'
        else:
            print 'ERROR connecting to server %s.\n'%(roach)
            exit_fail()

        ### #prepare synths ###
        LOs = tuple(usb.core.find(find_all=True, idVendor=0x10c4, idProduct=0x8468))
        print LOs[0].bus, LOs[0].address
        print LOs[1].bus, LOs[1].address
        if ((LOs[0] is None) or (LOs[1] is None)): #Was device found?
            raise ValueError('Device not found.')
        else:
            print(str(numpy.size(LOs))+' device(s) found:')

        ii=0
        while (ii< numpy.size(LOs)): #Make sure the USB device is ready to receive commands
            LOs[ii].reset()
            reattach = False
            if LOs[ii].is_kernel_driver_active(0):
                reattach = True
                LOs[ii].detach_kernel_driver(0)
            LOs[ii].set_configuration()
            ii=ii+1

        set_RF_output(0,1) #Turn on the RF output. (device,state)
        set_RF_output(1,1)
        ### end synth prep ###

        i = 0

        while (i < nfreq):

            f_sample = F_START#(((VfreqSet-1.664)/dv_over_df)*(12.0) + 120.0)
            print('Begining step '+str(i)+' of '+str(nfreq)+', where frequency = '+str(f_sample))
            time.sleep(T_BETWEEN_DELTA_F)
            #Now is time to take a beam map
            MakeBeamMap(i, f_sample)
            i = i+1

        ##
        print('Beam Map Complete.')

        arr2D_all_data = np.around(arr2D_all_data,decimals=3)
        print('Saving data...')
        np.savetxt(STR_FILE_OUT,arr2D_all_data,fmt='%.3e',header=('f_sample(GHz), x, y, phi, index_signal of peak cross power, and '+str(N_CHANNELS)+' points of all of following: aa, bb, ab, phase (deg.)'))

        print('Done. Exiting.')  
        print(stage_xy.position)

    except KeyboardInterrupt:
        exit_clean()
    except:
        exit_fail()
       

    return STR_FILE_OUT
    
span = 25
res = .5
str_out = beam2d(115,span,res,'co_') 
str_out = beam2d(110,span,res,'co_') 
str_out = beam2d(105,span,res,'co_') 
str_out = beam2d(100,span,res,'co_') 
str_out = beam2d(95,span,res,'co_') 
str_out = beam2d(90,span,res,'co_') 
str_out = beam2d(85,span,res,'co_') 
str_out = beam2d(80,span,res,'co_') 

stage_xy.disable()

DATA_1 = np.loadtxt(str_out,skiprows=1)
DATA = []
L_MEAN = 1
N_INDIV = 7

line_size = np.size(DATA_1[0])
nsamp =  np.size(DATA_1,0)
arr_x = np.zeros(nsamp)
arr_y = np.zeros(nsamp)
arr_phi = np.zeros(nsamp)
amp_cross=np.zeros(nsamp)
amp_AA=np.zeros(nsamp)
amp_BB=np.zeros(nsamp)
amp_var=np.zeros(nsamp)
phase=np.zeros(nsamp)

i_AA_begin = int(N_INDIV + (1-1)*(line_size-N_INDIV)/4)
i_AA_end= int(N_INDIV + (2-1)*(line_size-N_INDIV)/4) -1
i_BB_begin = int(N_INDIV + (2-1)*(line_size-N_INDIV)/4)
i_BB_end= int(N_INDIV + (3-1)*(line_size-N_INDIV)/4) -1
i_AB_begin = int(N_INDIV + (3-1)*(line_size-N_INDIV)/4)
i_AB_end= int(N_INDIV + (4-1)*(line_size-N_INDIV)/4) -1
i_phase_begin = int(N_INDIV + (4-1)*(line_size-N_INDIV)/4)
i_phase_end= int(N_INDIV + (5-1)*(line_size-N_INDIV)/4) -1

i=int(0)

jj =1
while (jj <= 1):
	i = int(0)
	if jj == 1: 
		str_data = 'Dataset 1'
		DATA = DATA_1
	else: 
		DATA = DATA_2
		str_data = 'Dataset 2'
	while (i < (nsamp)):
		#take in raw DATA
		arr_x[i] = DATA[i][1]
		arr_y[i] = DATA[i][2]
		arr_phi[i] = DATA[i][3]
		index_signal = DATA[i][4] # use same index singal for both datasets. keep it simple for now. 
		arr_AA = np.array(running_mean(DATA[i][i_AA_begin : i_AA_end],L_MEAN))
		arr_BB = np.array(running_mean(DATA[i][i_BB_begin : i_BB_end],L_MEAN))
		arr_AB = np.array(running_mean(DATA[i][i_AB_begin : i_AB_end],L_MEAN))
		arr_phase = np.array( DATA[i][i_phase_begin : i_phase_end] )
		n_channels = np.size(arr_AB)
	
		#make amplitude arrays, in case they need to be plotted.
		amp_cross[i] = np.power(arr_AB[int(n_channels/2)], 1)
		amp_var[i] = np.power( np.divide(arr_AB[int(n_channels/2)],arr_AA[int(n_channels/2)]) , 2)
		amp_AA[i] = arr_AA[int(n_channels/2)]
		amp_BB[i] = arr_BB[int(n_channels/2)]
		phase[i] = np.remainder(arr_phase[int(n_channels/2)],360.)
		#print('phase[i] = '+str(phase[i]))
		i = i+1

	amp = amp_var
	amp = np.divide(amp, np.max(amp))
	arr_x = np.unique(arr_x)
	arr_y = np.unique(arr_y)
	X,Y = np.meshgrid(arr_x,arr_y)
	P = amp_cross.reshape(len(arr_x),len(arr_y))
	Z = phase.reshape(len(arr_x),len(arr_y))

	jj = jj +1

beam_complex = P * np.exp(Z * np.pi / 180. *np.complex(0,1))
#Z = np.transpose(Z)
#beam_complex = np.transpose(beam_complex)

plt.figure()
plt.subplot(1,2,1)
plt.pcolormesh(X,Y,Z)
plt.title("Phase")
plt.xlabel('x (cm.)')
plt.ylabel('y (cm.)')
plt.colorbar(label = 'Phase')
plt.axis("equal")
plt.subplot(1,2,2)
plt.pcolormesh(X,Y,20*np.log10(abs(beam_complex)/np.max(abs(beam_complex))))
plt.title("Power [dB]")
plt.xlabel('x (cm.)')
plt.ylabel('y (cm.)')
plt.colorbar(label = 'Power')
plt.axis("equal")
plt.show()

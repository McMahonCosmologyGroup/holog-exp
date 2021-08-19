"""
Functions used to grab data from a wideband
Pocket correlator and plotting it using numpy/pylab.
Designed for use with TUT4 at the 2009 CASPER workshop.
Grace E. Chesmore, August 2021
"""

import struct
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import synth
import time
import sys
from optparse import OptionParser

plt.style.use('ggplot')

def running_mean(x, N):
    return np.convolve(x, np.ones((N,)) / N)[(N - 1) :]

class RoachOpt:
    '''
    ROACH2 configuration settings.
    '''
    BITSTREAM='t4_roach2_noquant_fftsat.fpg'
    f_clock_MHz = 500
    f_max_MHz = (f_clock_MHz/4)
    katcp_port=7147
    ip ='192.168.4.20'
    N_CHANNELS = 21
    L_MEAN = 1
    N_TO_AVG = 1
    window = 1

def get_data(baseline,fpga):
    '''
    Read out data from ROACH2 FPGA.
    '''
    acc_n = fpga.read_uint('acc_num')
    # print 'Grabbing integration number %i'%acc_n

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
        interleave_cross_b.append(complex(b_1r[i], b_1i[i]))#For phase, new, test.

        #auto
        interleave_auto_a.append(a_0[i])
        interleave_auto_a.append(a_1[i])
        interleave_auto_b.append(b_0[i])
        interleave_auto_b.append(b_1[i])

    return acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b

def roach2_init():

    p = OptionParser()
    p.set_usage("poco_init.py")
    p.set_description(__doc__)
    # here is where we can change integration time
    p.add_option(
        "-l",
        "--acc_len",
        dest="acc_len",
        type="int",
        default=2
        * (2 ** 28)
        / 2048,# for low pass filter and
            # amplifier this seems
            # like a good value, though
            # not tested with sig. gen.
            # 25 jan 2018: 0.01
        help="Set the number of vectors to accumulate between dumps. default is 2*(2^28)/2048.",
    )  # for roach full setup.
    p.add_option(
        "-g",
        "--gain",
        dest="gain",
        type="int",
        default=2,
        help="Set the digital gain (4bit quantisation scalar). default is 2.",
    )
    p.add_option(
        "-s",
        "--skip",
        dest="skip",
        action="store_true",
        help="Skip reprogramming the FPGA and configuring EQ.",
    )
    p.add_option(
        "-f",
        "--fpg",
        dest="fpgfile",
        type="str",
        default="",
        help="Specify the bof file to load",
    )
    opts, args = p.parse_args(sys.argv[1:])
    roach = RoachOpt.ip

    if opts.fpgfile != "":
        BIT_S = opts.fpgfile
    else:
        BIT_S = RoachOpt.BITSTREAM
    return roach,opts,BIT_S

def data_callback_peak(baseline,fpga,syn,LOs):
    '''
    Print real-time signal measurement from ROACH.
    '''
    l_mean = RoachOpt.L_MEAN
    window = RoachOpt.window
    # Set the frequency of the RF output, in MHz.
    # (device, state) You must have the device's
    # RF output in state (1) before doing this.

    synth.set_f(0,syn.freq,syn,LOs)
    synth.set_f(1,int(syn.freq+syn.freq_offset),syn,LOs)

    IGNORE_PEAKS_BELOW = int(600)
    IGNORE_PEAKS_ABOVE = int(700)

    acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b= get_data(baseline,fpga)

    arr_index_signal=[]
    interleave_cross_a = np.array(interleave_cross_a)
    valab = running_mean(np.abs(interleave_cross_a),l_mean)

    val_copy_i_eval = np.array(valab)
    val_copy_i_eval[int(IGNORE_PEAKS_ABOVE):]=0
    val_copy_i_eval[: int(IGNORE_PEAKS_BELOW)]=0

    arr_index_signal = np.argpartition(val_copy_i_eval, -2)[-2:]
    
    # Grab the indices of the two largest signals.
    #Find peak cross signal, print value and the freq. at which it occurs:
    if arr_index_signal[1] != 0 and arr_index_signal[1] != 1 and arr_index_signal[1] != 2 and arr_index_signal[1] != 3:
        index_signal = arr_index_signal[1]
    else:
        index_signal = arr_index_signal[0]
        
    return index_signal

def draw_data_callback(baseline,fpga,syn,LOs,fig):
    '''
    Print real-time signal measurement from ROACH.
    '''
    l_mean =1
    window = 1
    # Set the frequency of the RF output, in MHz.
    # (device, state) You must have the device's
    # RF output in state (1) before doing this.

    synth.set_f(0,syn.freq,syn,LOs)
    synth.set_f(1,int(syn.freq+syn.freq_offset),syn,LOs)

    IGNORE_PEAKS_BELOW = int(0)
    IGNORE_PEAKS_ABOVE = int(1090)
    matplotlib.pyplot.clf()
    time.sleep(0.75)
    acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b= get_data(baseline,fpga)
    freq = np.linspace(0,RoachOpt.f_max_MHz,len(np.abs(interleave_cross_a)))
    x_index = np.linspace(0,1024,len(np.abs(interleave_cross_a)))

    arr_index_signal=[]

    interleave_auto_a = np.array(interleave_auto_a)
    interleave_auto_b = np.array(interleave_auto_b)
    interleave_cross_a = np.array(interleave_cross_a)
    valaa = running_mean(np.abs(interleave_auto_a),l_mean)
    valbb = running_mean(np.abs(interleave_auto_b),l_mean)
    valab = running_mean(np.abs(interleave_cross_a),l_mean)

    val_copy_i_eval = np.array(valab)
    val_copy_i_eval[int(IGNORE_PEAKS_ABOVE):]=0
    val_copy_i_eval[: int(IGNORE_PEAKS_BELOW)]=0

    # Here is where we plot the signal.
    matplotlib.pyplot.semilogy(x_index,valaa,color = 'b',label = 'aa',alpha = .5)
    matplotlib.pyplot.semilogy(x_index,valbb,color = 'r',label = 'bb',alpha = .5)
    plt.semilogy(x_index,valab,color = 'g',label = 'cross')
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)

    plt.ylim(1e3,1e10)
    plt.xlim(500,800)
    plt.ylabel('Running Power: Cross')
    plt.title('Integration number %i \n%s'%(acc_n,baseline))
    fig.canvas.manager.window.after(100, draw_data_callback,baseline,fpga,syn,LOs,fig)
    plt.show()

def TakeAvgData(baseline,fpga):
    N_CHANNELS = RoachOpt.N_CHANNELS
    N_TO_AVG = RoachOpt.N_TO_AVG
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
        arr2D_aa[j],arr2D_bb[j],arr2D_ab[j],arr2D_phase[j], arr2D_index[j]=drawDataCallback(baseline,fpga) 
        #^^^^take in data from the roach. see function "drawDataCallback" above for how this works. "arr2D" array take in data across all frequency bins of the roach. 
        j = j+1    

    arr_phase=arr2D_phase.mean(axis=0)
    arr_aa=arr2D_aa.mean(axis=0)
    arr_bb=arr2D_bb.mean(axis=0)
    arr_ab=arr2D_ab.mean(axis=0)
    arr_index=arr2D_index.mean(axis=0)

    return arr_aa, arr_bb, arr_ab, arr_phase, arr_index

def drawDataCallback(baseline,fpga):
    IGNORE_PEAKS_BELOW = int(655)
    IGNORE_PEAKS_ABOVE = int(660)

    N_CHANNELS = RoachOpt.N_CHANNELS
    N_TO_AVG = RoachOpt.N_TO_AVG
    L_MEAN = RoachOpt.L_MEAN
    #print('running get_data  function from drawDataCallback')
    acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b= get_data(baseline,fpga)
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

def get_data(baseline,fpga):
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

"""
Functions used to grab data from a wideband Pocket correlator and plotting it using numpy/pylab. Designed for use with TUT4 at the 2009 CASPER workshop.
Grace E. Chesmore, August 2021
"""

import struct
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import synth
matplotlib.use('TkAgg')

class roach:
    '''
    ROACH2 configuration settings.
    '''
    bitstream='t4_roach2_noquant_fftsat.fpg'
    f_clock_MHz = 500
    f_max_MHz = (f_clock_MHz/4)
    katcp_port=7147
    ip ='192.168.4.20'

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

# def draw_data_callback(baseline,fpga,syn,LOs):
#     '''
#     Print real-time signal measurement from ROACH.
#     '''
#     l_mean =1
#     window = 1
#     # Set the frequency of the RF output, in MHz.
#     # (device, state) You must have the device's
#     # RF output in state (1) before doing this.

#     synth.set_f(0,F,syn,LOs)
#     synth.set_f(1,int(F+F_OFFSET),syn,LOs)

#     IGNORE_PEAKS_BELOW = int(0)
#     IGNORE_PEAKS_ABOVE = int(1090)
#     matplotlib.pyplot.clf()
#     time.sleep(0.75)
#     acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b= get_data(baseline,fpga)
#     freq = np.linspace(0,roach.f_max_MHz,len(np.abs(interleave_cross_a)))
#     x_index = np.linspace(0,1024,len(np.abs(interleave_cross_a)))

#     #matplotlib.pyplot.subplot(111)
#     which = 0
#     val=[]
#     val_b=[]
#     arr_index_signal=[]

#     interleave_auto_a = np.array(interleave_auto_a)
#     interleave_auto_b = np.array(interleave_auto_b)
#     interleave_cross_a = np.array(interleave_cross_a)
#     valaa = running_mean(np.abs(interleave_auto_a),l_mean)
#     valbb = running_mean(np.abs(interleave_auto_b),l_mean)
#     valab = running_mean(np.abs(interleave_cross_a),l_mean)

#     val_copy_i_eval = np.array(valab)
#     val_copy_i_eval[int(IGNORE_PEAKS_ABOVE):]=0
#     val_copy_i_eval[: int(IGNORE_PEAKS_BELOW)]=0

#     # Here is where we plot the signal.
#     #matplotlib.pyplot.semilogy(x_index,valaa,color = 'b',label = 'aa')
#     #matplotlib.pyplot.semilogy(x_index,valbb,color = 'r',label = 'bb')
#     plt.semilogy(x_index,valab,color = 'g',label = 'cross')
#     plt.legend()

#     plt.ylim(ylim_lo, ylim_hi)
#     plt.xlim(xlim_lo,xlim_hi)

#     arr_index_signal = np.argpartition(val_copy_i_eval, -2)[-2:]
#     # grab the indices of the two largest signals.

#     plt.grid(which="major")
#     plt.ylabel('Running Power: Cross')
#     plt.title('Integration number %i \n%s'%(acc_n,baseline))

#     #Find peak cross signal, print value and the freq. at which it occurs
#     if arr_index_signal[1] != 0 and arr_index_signal[1] != 1 and arr_index_signal[1] != 2 and arr_index_signal[1] != 3:
#         index_signal = arr_index_signal[1]
#     else:
#         index_signal = arr_index_signal[0]

#     power_cross = (np.abs(interleave_cross_a))[index_signal]
#     arr_phase = np.degrees(np.angle(interleave_cross_a))

#     power_auto_a = (np.abs(interleave_auto_a))[index_signal]
#     power_auto_b = (np.abs(interleave_auto_b))[index_signal]

#     if (index_signal <= window/2) and index_signal <=2:
#         print('ERROR: your window size is too large. subtracting half of it from index will throw you outside array. Window/2 = '+str(window/2)+', index_signal = '+str(index_signal))
#     else:
#         max_cross_pwr = np.max( (np.abs(interleave_cross_a))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE] )
#         max_auto_A_pwr = np.max( (np.abs(interleave_auto_a))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE]    )
#         max_auto_B_pwr = np.max( (np.abs(interleave_auto_b))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE]    )
#         index_cross = np.argmax( (np.abs(interleave_cross_a))[IGNORE_PEAKS_BELOW:IGNORE_PEAKS_ABOVE])+ IGNORE_PEAKS_BELOW
#         index_AA = np.argmax( (np.abs(interleave_auto_a))[IGNORE_PEAKS_BELOW: IGNORE_PEAKS_ABOVE])+IGNORE_PEAKS_BELOW
#         index_BB = np.argmax( (np.abs(interleave_auto_b))[IGNORE_PEAKS_BELOW:IGNORE_PEAKS_ABOVE])+IGNORE_PEAKS_BELOW

#         max_mean_cross_pwr = np.max( (running_mean(np.abs(interleave_cross_a),l_mean))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE] )
#         max_mean_auto_A_pwr = np.max( (running_mean(np.abs(interleave_auto_a),l_mean))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE]    )
#         max_mean_auto_B_pwr = np.max( (running_mean(np.abs(interleave_auto_b),l_mean))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE]    )
#         index_mean_cross = np.argmax( (running_mean(np.abs(interleave_cross_a),l_mean))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE] )+IGNORE_PEAKS_BELOW
#         index_mean_AA = np.argmax( (running_mean(np.abs(interleave_auto_a),l_mean))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE] )+IGNORE_PEAKS_BELOW
#         index_mean_BB = np.argmax( (running_mean(np.abs(interleave_auto_b),l_mean))[IGNORE_PEAKS_BELOW : IGNORE_PEAKS_ABOVE] )+IGNORE_PEAKS_BELOW

#     # this might be wrong
#     fig.canvas.manager.window.after(100, drawDataCallback,baseline,fpga)
#     plt.show()

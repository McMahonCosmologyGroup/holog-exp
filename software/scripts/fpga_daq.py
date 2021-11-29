import numpy as np
import struct
import sys
import matplotlib
matplotlib.use('TkAgg') # do this before importing pylab
import matplotlib.pyplot as plt

def running_mean(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

class RoachOpts:
    N_CHANNELS = 21
    N_TO_AVG = 1
    L_MEAN = 1

def exit_fail(fpga,lh):
    print 'FAILURE DETECTED. Log entries:\n',lh.printMessages()
    try:
        fpga.stop()
    except: pass
    raise
    exit()

def exit_clean(fpga):
    try:
        fpga.stop()
    except: pass
    exit()

def get_data(baseline,fpga):

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
        interleave_cross_b.append(complex(b_1r[i], b_1i[i]))#For phase, new, test

	#auto
	interleave_auto_a.append(a_0[i])
        interleave_auto_a.append(a_1[i])
        interleave_auto_b.append(b_0[i])
        interleave_auto_b.append(b_1[i])

    return acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b

def drawDataCallback(baseline,fpga,synth_settings):
    #print('running get_data  function from drawDataCallback')
    acc_n,interleave_cross_a,interleave_cross_b,interleave_auto_a,interleave_auto_b= get_data(baseline,fpga)
    val=running_mean(np.abs(interleave_cross_a),RoachOpts.L_MEAN)
    val[int(synth_settings.IGNORE_PEAKS_ABOVE):]=0
    val[: int(synth_settings.IGNORE_PEAKS_BELOW)]=0
    arr_index_signal = np.argpartition(val, -2)[-2:]
    index_signal = arr_index_signal[1]
    # IS THIS NECESSARY? Probably not here, at least. freq = numpy.linspace(0,f_max_MHz,len(numpy.abs(interleave_cross_a)))
    arr_ab = (np.abs(interleave_cross_a))
    arr_phase = (180./np.pi)*np.unwrap((np.angle(interleave_cross_b)))
    phase_signal = arr_phase[index_signal]
    arr_aa = (np.abs(interleave_auto_a))
    arr_bb = (np.abs(interleave_auto_b))

    #Only record relevant channels, right around peak:
    arr_aa = arr_aa[(index_signal - (RoachOpts.N_CHANNELS/2)) : (1+index_signal + (RoachOpts.N_CHANNELS/2))]
    arr_bb = arr_bb[(index_signal - (RoachOpts.N_CHANNELS/2)) : (1+index_signal + (RoachOpts.N_CHANNELS/2))]
    arr_ab = arr_ab[(index_signal - (RoachOpts.N_CHANNELS/2)) : (1+index_signal + (RoachOpts.N_CHANNELS/2))]
    arr_phase = arr_phase[(index_signal - (RoachOpts.N_CHANNELS/2)) : (1+index_signal + (RoachOpts.N_CHANNELS/2))]

    return running_mean(arr_aa,RoachOpts.L_MEAN),running_mean(arr_bb,RoachOpts.L_MEAN),running_mean(arr_ab,RoachOpts.L_MEAN), arr_phase, index_signal

def TakeAvgData(baseline,fpga,synth_settings):
    arr_phase= np.zeros((RoachOpts.N_CHANNELS,1))
    arr_aa= np.zeros((RoachOpts.N_CHANNELS,1))
    arr_bb= np.zeros((RoachOpts.N_CHANNELS,1))
    arr_ab= np.zeros((RoachOpts.N_CHANNELS,1))
    arr_index =np.zeros((1,1))

    arr2D_phase= np.zeros((RoachOpts.N_TO_AVG,RoachOpts.N_CHANNELS))#array of phase data, which I will take the mean of
    arr2D_aa=np.zeros((RoachOpts.N_TO_AVG,RoachOpts.N_CHANNELS))
    arr2D_bb=np.zeros((RoachOpts.N_TO_AVG,RoachOpts.N_CHANNELS))
    arr2D_ab=np.zeros((RoachOpts.N_TO_AVG,RoachOpts.N_CHANNELS))
    arr2D_index= np.zeros((RoachOpts.N_TO_AVG,1))
    j = 0
    #to average according to each unique index of peak signal, rather than taking mean at the mean value of index of peak signal
    arr_var_unique =np.zeros((RoachOpts.N_TO_AVG,1)) # A test to see how well we can use mean data over 'RoachOpts.N_TO_AVG'.
    while (j < RoachOpts.N_TO_AVG):
        #print('In TakeAvgData(), j = ('+str(j)+'/RoachOpts.N_TO_AVG)'+' and we are about to drawDataCallback')
        arr2D_aa[j],arr2D_bb[j],arr2D_ab[j],arr2D_phase[j], arr2D_index[j]=drawDataCallback(baseline,fpga,synth_settings)
        #^^^^take in data from the roach. see function "drawDataCallback" above for how this works. "arr2D" array take in data across all frequency bins of the roach.
        j = j+1

    arr_phase=arr2D_phase.mean(axis=0)
    arr_aa=arr2D_aa.mean(axis=0)
    arr_bb=arr2D_bb.mean(axis=0)
    arr_ab=arr2D_ab.mean(axis=0)
    arr_index=arr2D_index.mean(axis=0)

    return arr_aa, arr_bb, arr_ab, arr_phase, arr_index

def roach2_init():
    from optparse import OptionParser
    p = OptionParser()
    p.set_usage('poco_init_no_quant.py')
    p.set_description(__doc__)
    p.add_option('-s', '--skip', dest='skip', action='store_true',
        help='Skip reprogramming the FPGA and configuring EQ.')
    p.add_option('-l', '--acc_len', dest='acc_len', type='int',default=.5*(2**28)/2048, #for low pass filter and amplifier this seems like a good value, though not tested with sig. gen. #	25 jan 2018: 0.01
        help='Set the number of vectors to accumulate between dumps. default is 2*(2^28)/2048.')#for roach full setup.

    p.add_option('-c', '--cross', dest='cross', type='str',default='bd',
        help='Plot this cross correlation magnitude and phase. default: bd')
    p.add_option('-g', '--gain', dest='gain', type='int',default=2,
        help='Set the digital gain (4bit quantisation scalar). default is 2.')
    p.add_option('-f', '--fpg', dest='fpgfile', type='str', default='',
        help='Specify the bof file to load')


    opts, args = p.parse_args(sys.argv[1:])
    roach='192.168.4.20'
    BIT_S=opts.cross

    return roach,opts,BIT_S

def plot_data(str_out):
    DATA_1 = np.loadtxt(str_out,skiprows=1)
    DATA = []
    RoachOpts.L_MEAN = 1
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
    		arr_AA = np.array(running_mean(DATA[i][i_AA_begin : i_AA_end],RoachOpts.L_MEAN))
    		arr_BB = np.array(running_mean(DATA[i][i_BB_begin : i_BB_end],RoachOpts.L_MEAN))
    		arr_AB = np.array(running_mean(DATA[i][i_AB_begin : i_AB_end],RoachOpts.L_MEAN))
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

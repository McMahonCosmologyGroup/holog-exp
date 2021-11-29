#!/usr/bin/env python
'''

'''

#TODO: add support for coarse delay change
#TODO: add support for ADC histogram plotting.
#TODO: add support for determining ADC input level

import casperfpga
import time
import sys
import logging
import numpy as np
import usb.core
import usb.util
import poco
import fpga_daq

katcp_port=7147
bitstream='t4_roach2_noquant_fftsat.fpg'


if __name__ == '__main__':
    from optparse import OptionParser

    p = OptionParser()
    p.set_usage('poco_init_no_quant.py')
    p.set_description(__doc__)
# here is where we can change integration time
    p.add_option('-l', '--acc_len', dest='acc_len', type='int',default=.5*(2**28)/2048, #for low pass filter and amplifier this seems like a good value, though not tested with sig. gen. #	25 jan 2018: 0.01
        help='Set the number of vectors to accumulate between dumps. default is 2*(2^28)/2048.')#for roach full setup.
    p.add_option('-g', '--gain', dest='gain', type='int',default=2,
        help='Set the digital gain (4bit quantisation scalar). default is 2.')
    p.add_option('-s', '--skip', dest='skip', action='store_true',
        help='Skip reprogramming the FPGA and configuring EQ.')
    p.add_option('-f', '--fpg', dest='fpgfile', type='str', default='',
        help='Specify the bof file to load')
    opts, args = p.parse_args(sys.argv[1:])
    roach='192.168.4.20'

    if opts.fpgfile != '':
        bitstream = opts.fpgfile
    else:
        bitstream = bitstream

try:

    loggers = []
    lh=poco.DebugLogHandler()
    logger = logging.getLogger(roach)
    logger.addHandler(lh)
    logger.setLevel(10)

    print('Connecting to server %s ... ' %(roach)),
    fpga = casperfpga.katcp_fpga.KatcpFpga(roach)
    #fpga = casperfpga.CasperFpga(roach)
    time.sleep(1)

    if fpga.is_connected():
        print('ok\n')
    else:
        print('ERROR connecting to server %s.\n'%(roach))
        fpga_daq.exit_fail(fpga,lh)

    print('------------------------')
    print('Programming FPGA...')
    if not opts.skip:
        sys.stdout.flush()
        fpga.upload_to_ram_and_program(bitstream)
        time.sleep(10)
        print('done')
    else:
        print('Skipped.')

    print('Configuring fft_shift...')
    fpga.write_int('fft_shift',(2**32)-1)
    print('done')

    print('Configuring accumulation period...')
    fpga.write_int('acc_len',opts.acc_len)
    print('done')

    print('Resetting board, software triggering and resetting error counters...')
    fpga.write_int('ctrl',0)
    fpga.write_int('ctrl',1<<17) #arm
    fpga.write_int('ctrl',0)
    fpga.write_int('ctrl',1<<18) #software trigger
    fpga.write_int('ctrl',0)
    fpga.write_int('ctrl',1<<18) #issue a second trigger
    print('done')

    #EQ SCALING!
    # writes only occur when the addr line changes value.
    # write blindly - don't bother checking if write was successful. Trust in TCP!
    #print 'Setting gains of all channels on all inputs to %i...'%opts.gain,
    #fpga.write_int('quant0_gain',opts.gain) #write the same gain for all inputs, all channels
    #fpga.write_int('quant1_gain',opts.gain) #write the same gain for all inputs, all channels
    #fpga.write_int('quant2_gain',opts.gain) #write the same gain for all inputs, all channels
    #fpga.write_int('quant3_gain',opts.gain) #write the same gain for all inputs, all channels
    print('flushing channels...')
    for chan in range(1024):
        #print '%i...'%chan,
        sys.stdout.flush()
        #for input in range(4):
        #    fpga.blindwrite('quant%i_addr'%input,struct.pack('>I',chan))
    print('done')

    print("All set up. Try plotting using plot_cross_phase_no_quant.py")

#    time.sleep(2)
#
#   prev_integration = fpga.read_uint('acc_num')
#   while(1):
#       current_integration = fpga.read_uint('acc_num')
#       diff=current_integration - prev_integration
#       if diff==0:
#           time.sleep(0.01)
#       else:
#           if diff > 1:
#               print 'WARN: We lost %i integrations!'%(current_integration - prev_integration)
#           prev_integration = fpga.read_uint('acc_num')
#           print 'Grabbing integration number %i'%prev_integration
#
#           if opts.auto:
#               plot_autos()
#           else:
#               plot_cross(opts.cross)
#
except KeyboardInterrupt:
    fpga_daq.exit_clean(fpga)

fpga_daq.exit_clean(fpga)

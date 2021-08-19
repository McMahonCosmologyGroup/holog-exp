#!/usr/bin/env python
"""
This script demonstrates grabbing data from a wideband Pocket correlator and plotting it using numpy/pylab. Designed for use with TUT4 at the 2009 CASPER workshop.
\n\n 
Author: Jason Manley, August 2009.
Modified: Tyrone van Balla, November 2015
Modified: Grace E. Chesmore, August 2021
"""


import time
import sys
import logging
from optparse import OptionParser
import usb.core
import matplotlib
matplotlib.use("TkAgg")  # do this before importing pylab
import matplotlib.pyplot as plt
import casperfpga
import synth
import fpga_daq
import poco

# Added by Charlie 2019-11-04
YLIM_LO = 1.0e8
YLIM_HI = 1.0e10
XLIM_LO = 650
XLIM_HI = 800

sys.setrecursionlimit(3000)  # by ATJ, to get longer recursion time.

N = 8
F = int(115.0 * 1000.0 / N)  # MHz
synth.SynthOpt.F = F


if __name__ == "__main__":

    p = OptionParser()
    p.set_usage("poco_init.py")
    p.set_description(__doc__)
    p.add_option(
        "-s",
        "--skip",
        dest="skip",
        action="store_true",
        help="Skip reprogramming the FPGA and configuring EQ.",
    )
    p.add_option(
        "-l",
        "--acc_len",
        dest="acc_len",
        type="int",
        default=0.5
        * (2 ** 28)
        / 2048,  # for low pass filter and amplifier this seems like a good value, though not tested with sig. gen. #	25 jan 2018: 0.01
        help="Set the number of vectors to accumulate between dumps. default is 2*(2^28)/2048.",
    )  # for roach full setup.

    p.add_option(
        "-c",
        "--cross",
        dest="cross",
        type="str",
        default="bd",
        help="Plot this cross correlation magnitude and phase. default: bd",
    )
    p.add_option(
        "-g",
        "--gain",
        dest="gain",
        type="int",
        default=2,
        help="Set the digital gain (4bit quantisation scalar). default is 2.",
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
    roach = fpga_daq.RoachOpt.ip
    baseline = opts.cross

try:
    loggers = []
    lh = poco.debug_loghandler()
    logger = logging.getLogger(roach)
    logger.addHandler(lh)
    logger.setLevel(10)

    print("Connecting to server %s ... " % (roach)),

    # fpga = casperfpga.CasperFpga(roach)
    fpga = casperfpga.katcp_fpga.KatcpFpga(roach)

    time.sleep(5)

    if fpga.is_connected():
        print("ok\n")
    else:
        print("ERROR connecting to server %s.\n" % (roach))
        poco.exit_fail(fpga)
        
    ### prepare synths ###
    LOs = tuple(usb.core.find(find_all=True, idVendor=0x10C4, idProduct=0x8468))
    print("LO1 bus: %d, address: %d" %(LOs[0].bus, LOs[0].address))
    print("LO2 bus: %d, address: %d" %(LOs[1].bus, LOs[1].address))

    if (LOs[0] is None) or (LOs[1] is None):  # Was device found?
        raise ValueError("Device not found.")
    for ID in range(len(LOs)):
        LOs[ID].reset()
        reattach = False  # Make sure the USB device is ready to receive commands.
        if LOs[ID].is_kernel_driver_active(0):
            reattach = True
            LOs[ID].detach_kernel_driver(0)
        LOs[ID].set_configuration()
            
    synth.set_rf_output(
        0, 1, synth.SynthOpt, LOs
    )  # Turn on the RF output. (device,state,synth options,LOs)
    synth.set_rf_output(1, 1, synth.SynthOpt, LOs)
    ### end synth prep ###
    peak = fpga_daq.data_callback_peak(baseline,fpga,synth.SynthOpt,LOs)
    print(peak)
    # set up the figure with a subplot for each polarisation to be plotted
    fig = plt.figure()

    # start the process    (this also might be wrong)
    fig.canvas.manager.window.after(
        100, fpga_daq.draw_data_callback, baseline, fpga, synth.SynthOpt, LOs,fig
    )
    plt.xlim(peak-100,peak+100)
    plt.show()
    print("Plotting complete. Exiting...")

except KeyboardInterrupt:
    poco.exit_clean(fpga)

poco.exit_clean(fpga)

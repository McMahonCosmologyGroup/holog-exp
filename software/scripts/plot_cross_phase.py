#!/usr/bin/env python
"""
This script demonstrates grabbing data from a wideband Pocket correlator and plotting it using numpy/pylab. Designed for use with TUT4 at the 2009 CASPER workshop.
\n\n 
Author: Jason Manley, August 2009.
Modified: Tyrone van Balla, November 2015
Modified: Grace E. Chesmore, October 2020
"""

import casperfpga
import time
import struct
import sys
import logging
import numpy as np
import usb.core
import matplotlib

matplotlib.use("TkAgg")  # do this before importing pylab
import matplotlib.pyplot as plt
import synth
import fpga_daq
import poco
from optparse import OptionParser

# Added by Charlie 2019-11-04
ylim_lo = 1.0e8
ylim_hi = 1.0e10
xlim_lo = 950
xlim_hi = 1000

sys.setrecursionlimit(3000)  # by ATJ, to get longer recursion time.

N = 12
F_OFFSET = 10  # MHz
F = int(135.0 * 1000.0 / N)  # MHz


def running_mean(x, N):
    return np.convolve(x, np.ones((N,)) / N)[(N - 1) :]


if __name__ == "__main__":

    p = OptionParser()
    p.set_usage("poco_init_no_quant.py")
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
    roach = fpga_daq.roach.ip
    baseline = opts.cross

try:
    loggers = []
    lh = poco.DebugLogHandler()
    logger = logging.getLogger(roach)
    logger.addHandler(lh)
    logger.setLevel(10)

    print ("Connecting to server %s ... " % (roach)),

    # fpga = casperfpga.CasperFpga(roach)
    fpga = casperfpga.katcp_fpga.KatcpFpga(roach)

    time.sleep(5)

    if fpga.is_connected():
        print "ok\n"
    else:
        print "ERROR connecting to server %s.\n" % (roach)
        poco.exit_fail(fpga)
    ### #prepare synths ###
    LOs = tuple(usb.core.find(find_all=True, idVendor=0x10C4, idProduct=0x8468))
    print LOs[0].bus, LOs[0].address
    print LOs[1].bus, LOs[1].address

    if (LOs[0] is None) or (LOs[1] is None):  # Was device found?
        raise ValueError("Device not found.")
    else:
        print (str(np.size(LOs)) + " device(s) found:")

    ii = 0
    while ii < np.size(LOs):
        LOs[ii].reset()
        reattach = False  # Make sure the USB device is ready to receive commands.
        if LOs[ii].is_kernel_driver_active(0):
            reattach = True
            LOs[ii].detach_kernel_driver(0)
        LOs[ii].set_configuration()
        ii = ii + 1
    synth.set_RF_output(
        0, 1, synth.synth_opt, LOs
    )  # Turn on the RF output. (device,state,synth options,LOs)
    synth.set_RF_output(1, 1, synth.synth_opt, LOs)
    ### end synth prep ###

    # set up the figure with a subplot for each polarisation to be plotted
    fig = matplotlib.pyplot.figure()

    # start the process    (this also might be wrong)
    fig.canvas.manager.window.after(
        100, drawDataCallback, baseline, fpga, synth.synth_opt, LOs
    )
    matplotlib.pyplot.show()
    print "Plotting complete. Exiting..."

except KeyboardInterrupt:
    poco.exit_clean(fpga)

poco.exit_clean(fpga)

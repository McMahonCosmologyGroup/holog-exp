#!/usr/bin/env python
"""
This script demonstrates grabbing data from a wideband Pocket
correlator and plotting it using numpy/pylab.
Designed for use with TUT4 at the 2009 CASPER workshop.

Author: Jason Manley, August 2009.
Modified: Tyrone van Balla, November 2015
Modified: Grace E. Chesmore, August 2021
"""


import sys
import time

import matplotlib
import usb.core

matplotlib.use("TkAgg")  # do this before importing pylab
import casperfpga
import fpga_daq
import matplotlib.pyplot as plt
import poco
import synth

# Added by Charlie 2019-11-04
YLIM_LO = 1.0e8
YLIM_HI = 1.0e10
XLIM_LO = 650
XLIM_HI = 800

sys.setrecursionlimit(3000)  # by ATJ, to get longer recursion time.

synth.SynthOpt.N = 8
freq = int(95.0 * 1000.0 / synth.SynthOpt.N)  # MHz
synth.SynthOpt.freq = freq

roach, opts, BIT_S = fpga_daq.roach2_init()
ROACH_IP = fpga_daq.RoachOpt.ip
baseline = opts.cross

try:

    # Connect to ROACH2 FPGA
    fpga = fpga_daq.roach2_connect(ROACH_IP)
    # Connect to synthesizers
    LOs = synth.synth_connect()

    synth.set_rf_output(
        0, 1, synth.SynthOpt, LOs
    )  # Turn on the RF output. (device,state,synth options,LOs)
    synth.set_rf_output(1, 1, synth.SynthOpt, LOs)
    ### end synth prep ###
    peak = fpga_daq.data_callback_peak(baseline, fpga, synth.SynthOpt, LOs)
    print(peak)
    # set up the figure with a subplot for each polarisation to be plotted
    fig = plt.figure()

    # start the process    (this also might be wrong)
    fig.canvas.manager.window.after(
        100, fpga_daq.draw_data_callback, baseline, fpga, synth.SynthOpt, LOs, fig
    )
    print(peak - 100)
    plt.xlim(peak - 100, peak + 100)
    plt.show()
    print("Plotting complete. Exiting...")

except KeyboardInterrupt:
    poco.exit_clean(fpga)

poco.exit_clean(fpga)

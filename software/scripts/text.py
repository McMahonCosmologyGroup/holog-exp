import array
import datetime
import getpass
import logging
import os
import struct
import sys
import time

import casperfpga
import matplotlib
import numpy
import numpy as np
import serial
import usb.core
import usb.util

matplotlib.use("TkAgg")  # do this before importing pylab
from optparse import OptionParser

import fpga_daq
import matplotlib.pyplot as plt
import poco
import synth

# import xy_agent.xy_connect as stage
# from xy_agent.xy_scan import XY_Scan

# import scipy.interpolate as spint
# import argparse
# stage_xy = stage.XY_Stage.latrt_xy_stage()
# stage_xy.enable()

# SETUP AND CONNECT TO FPGA
p = OptionParser()
p.set_usage("poco_init.py")
p.set_description(__doc__)
p.add_option(
    "-c",
    "--cross",
    dest="cross",
    type="str",
    default="bd",
    help="Plot this cross correlation magnitude and phase. default: bd",
)
roach = fpga_daq.RoachOpt.ip
baseline = "bd"
loggers = []
lh = poco.DebugLogHandler()
logger = logging.getLogger(roach)
logger.addHandler(lh)
logger.setLevel(10)

print ("Connecting to server %s ... " % (roach)),
fpga = casperfpga.katcp_fpga.KatcpFpga(roach)
time.sleep(1)

if fpga.is_connected():
    print "ok\n"
else:
    print "ERROR connecting to server %s.\n" % (roach)
    poco.exit_fail(fpga, lh)

# PREPARE SYNTHESIZERS
LOs = tuple(usb.core.find(find_all=True, idVendor=0x10C4, idProduct=0x8468))
print LOs[0].bus, LOs[0].address
print LOs[1].bus, LOs[1].address
if (LOs[0] is None) or (LOs[1] is None):  # Was device found?
    raise ValueError("Device not found.")
else:
    print (str(numpy.size(LOs)) + " device(s) found:")

ii = 0
while ii < numpy.size(LOs):  # Make sure the USB device is ready to receive commands
    LOs[ii].reset()
    reattach = False
    if LOs[ii].is_kernel_driver_active(0):
        reattach = True
        LOs[ii].detach_kernel_driver(0)
    LOs[ii].set_configuration()
    ii = ii + 1

synth.set_rf_output(0, 1, synth.SynthOpt, LOs)  # Turn on the RF output. (device,state)
synth.set_rf_output(1, 1, synth.SynthOpt, LOs)


nsamp = 5
arr2D_all_data = np.zeros((nsamp, (4 * fpga_daq.RoachOpt.N_CHANNELS + 5)))
# where the 7 extra are f,phi,... x_cur,y_cur,
# index_signal of peak cross power in a single bin (where phase is to be measured).


def before():
    ii = 0
    ff = 90  # GHz
    N = 8
    f = int(ff * 1000 / N)  # MHz
    synth.set_f(0, f, synth.SynthOpt, LOs)
    synth.set_f(1, f + synth.SynthOpt.freq_offset, synth.SynthOpt, LOs)


def during():
    phi = 90
    position = scan.stage_xy.position
    x_cur = positiion[0]
    y_cur = positiion[1]
    arr_aa, arr_bb, arr_ab, arr_phase, index_signal = fpga_daq.TakeAvgData(
        baseline, fpga
    )
    arr2D_all_data[ii] = (
        [f]
        + [x_cur]
        + [y_cur]
        + [phi]
        + [index_signal]
        + arr_aa.tolist()
        + arr_bb.tolist()
        + arr_ab.tolist()
        + arr_phase.tolist()
    )
    ii += 1
    print (" end f = " + str(f))


def after():
    """Function to call at the end of the scan"""
    print ("Beam Map Complete.")

    arr2D_all_data = np.around(arr2D_all_data, decimals=3)
    print ("Saving data...")
    np.savetxt(
        STR_FILE_OUT,
        arr2D_all_data,
        fmt="%.3e",
        header=(
            "f_sample(GHz), x, y, phi, index_signal of peak cross power, and "
            + str(N_CHANNELS)
            + " points of all of following: aa, bb, ab, phase (deg.)"
        ),
    )
    print ("Done. Exiting.")
    time.sleep(2)


scan = XY_Scan(with_ocs=False)

scan.setup_scan(
    total_distance_x=10,
    total_distance_y=10,
    N_pts_x=3,
    N_pts_y=3,
    x_vel=1,
    y_vel=1,
    scan_dir="x",
    step_raster=True,
)

scan.set_before_scan_function(before)
scan.set_during_scan_function(during)
scan.set_after_scan_function(after)
scan.execute()

"""
Initialization script for the CASPER ROACH2.
Grace E. Chesmore
July 19, 2021
"""


import logging
import sys
import time

import casperfpga
import fpga_daq
import poco

roach, opts, BIT_S = fpga_daq.roach2_init()

try:

    loggers = []
    lh = poco.DebugLogHandler()
    logger = logging.getLogger(roach)
    logger.addHandler(lh)
    logger.setLevel(10)

    print("Connecting to server %s ... " % (roach))
    fpga = casperfpga.katcp_fpga.KatcpFpga(roach)
    # fpga = casperfpga.CasperFpga(roach)
    time.sleep(1)

    if fpga.is_connected():
        print("ok\n")
    else:
        print("ERROR connecting to server %s.\n" % (roach))
        poco.exit_fail(fpga, lh)

    print("------------------------")
    print("Programming FPGA...")
    if not opts.skip:
        sys.stdout.flush()
        fpga.upload_to_ram_and_program(BIT_S)
        time.sleep(10)
        print("done")
    else:
        print("Skipped.")

    print("Configuring fft_shift...")
    fpga.write_int("fft_shift", (2 ** 32) - 1)
    print("done.")
    print("Configuring accumulation period...")
    fpga.write_int("acc_len", opts.acc_len)
    print("done")

    print("Resetting board, software triggering and resetting error counters...")
    fpga.write_int("ctrl", 0)
    fpga.write_int("ctrl", 1 << 17)  # arm
    fpga.write_int("ctrl", 0)
    fpga.write_int("ctrl", 1 << 18)  # software trigger
    fpga.write_int("ctrl", 0)
    fpga.write_int("ctrl", 1 << 18)  # issue a second trigger
    print("done")

    print("flushing channels...")
    for chan in range(1024):
        sys.stdout.flush()

    print("done")

    print("Casper ROACH2 FPGA is set up.")

except KeyboardInterrupt:
    poco.exit_clean(fpga)

poco.exit_clean(fpga)

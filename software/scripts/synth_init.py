"""
Initializing two synthesizers via USB connection for holography experiment.
Grace E. Chesmore
July 19, 2021
"""

import usb.core
import numpy as np
import synth


N = 9
F_TEST = 95  # GHz
F_OFFSET = 10  # MHz
F = int(F_TEST * 1000.0 / N)  # MHz

# Contact the synthesizer USB ports

LOs = synth.synth_connect()
# LOs = tuple(usb.core.find(find_all=True, idVendor=0x10C4, idProduct=0x8468))
# print(LOs)
# print(LOs[0].bus, LOs[0].address)
# print(LOs[1].bus, LOs[1].address)

# # Was device found?
# if (LOs[0] is None) or (LOs[1] is None):
#     raise ValueError("Device not found.")

# NUM = 0
# while NUM < np.size(LOs):
#     LOs[NUM].reset()
#     REATTACH = False  # Make sure the USB device is ready to receive commands.
#     if LOs[NUM].is_kernel_driver_active(0):
#         REATTACH = True
#         LOs[NUM].detach_kernel_driver(0)
#     LOs[NUM].set_configuration()
#     NUM = NUM + 1

synth.set_rf_output(0, 1, synth.SynthOpt, LOs)
# Turn on the RF output (device,state).
synth.set_rf_output(1, 1, synth.SynthOpt, LOs)
synth.set_f(0, F, synth.SynthOpt, LOs)
# Set the frequency of the RF output, in MHz. (device, state).
# You must have the device's RF output in state (1) before doing this.
synth.set_f(1, int(F + F_OFFSET), synth.SynthOpt, LOs)

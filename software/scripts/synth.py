"""
Functions for operating two synthesizers via USB connection for holography experiment.
Grace E. Chesmore
July 19, 2021
"""
import struct

import numpy as np
import synth
import usb.core


class SynthOpt:
    """
    Syntonic Synthesizer settings specified by manual.
    """

    endpoint_dec = 2  # always 2 according to user manual.
    endpoint_hex = 0x02
    freq = 0
    freq_offset = 5  # MHz
    N = 0


def set_rf_output(device, state, syn, los):
    """
    for state, e.g. '1' for command '0x02' will turn ON the RF output.
    """
    print("Setting RF output")
    n_bytes = 2  # number of bytes remaining in the packet
    n_command = 0x02  # the command number, such as '0x02' for RF output control.
    data = bytearray(64)
    data[0] = syn.endpoint_hex
    data[1] = n_bytes
    data[2] = n_command
    data[3] = state
    los[int(device)].write(syn.endpoint_dec, data)


def reset_rf(device, syn):
    """
    for state, e.g. '1' for command '0x02' will turn ON the RF output.
    """
    print("Resetting RF")
    n_bytes = 2  # number of bytes remaining in the packet
    n_command = 0x03  # the command number, such as '0x02' for RF output control.
    data = bytearray(64)
    data[0] = syn.endpoint_hex
    data[1] = n_bytes
    data[2] = n_command
    data[3] = 0x00  # state
    device.write(syn.endpoint_dec, data)


def set_100_output(device, state, syn):
    """
    for state, e.g. '1' for command '0x02' will turn ON the RF output.
    """
    print("Setting 100MHz output to state " + str(state))
    n_bytes = 2  # number of bytes remaining in the packet
    n_command = 0x1E  # the command number, such as '0x02' for RF output control.
    data = bytearray(64)
    data[0] = syn.endpoint_hex  # chr(ENDPOINT)
    data[1] = n_bytes
    data[2] = n_command
    data[3] = state
    device.write(syn.endpoint_dec, str(data))


def synth_connect():

    LOs = tuple(usb.core.find(find_all=True, idVendor=0x10C4, idProduct=0x8468))
    print("LO1 bus: %d, address: %d" % (LOs[0].bus, LOs[0].address))
    print("LO2 bus: %d, address: %d" % (LOs[1].bus, LOs[1].address))

    if (LOs[0] is None) or (LOs[1] is None):  # Was device found?
        raise ValueError("Device not found.")

    for ID, lo_num in enumerate(LOs):
        #     for ID in range(len(LOs)):
        LOs[ID].reset()
        REATTACH = False  # Make sure the USB device is ready to receive commands.
        if LOs[ID].is_kernel_driver_active(0):
            REATTACH = True
            LOs[ID].detach_kernel_driver(0)
        LOs[ID].set_configuration()

    return LOs


def set_f(device, freq, syn, los):
    """
    sets frequency output of synth to specified freq. in MHz.
    """
    # print("Setting frequency to " + str(freq/1e3) + " GHz")
    n_bytes = 6  # number of bytes remaining in the packet
    n_command = 0x01  # the command number, such as '0x02' for RF output control.
    bytes = [
        hex(ord(b)) for b in struct.pack(">Q", (freq * 1.0e6))
    ]  # Q is unsigned long long and has std size 8, we only ever use last 5 elements.
    data = bytearray(64)
    data[0] = syn.endpoint_hex
    data[1] = n_bytes
    data[2] = n_command
    i_strt = 3

    for index in range(5):
        data[int(index + i_strt)] = int(bytes[index + i_strt], 16)

    los[int(device)].write(syn.endpoint_dec, data)

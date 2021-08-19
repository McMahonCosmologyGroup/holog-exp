"""
Functions for operating two synthesizers via USB connection for holography experiment.
Grace E. Chesmore
July 19, 2021
"""
import struct
from dataclasses import dataclass

@dataclass

class SynthOpt:
    """
    high level support for doing this and that.
    """
    endpoint_dec = 2  # always 2 according to user manual.
    endpoint_hex = 0x02
    freq = 0
    freq_offset = 10 # MHz

def set_rf_output(device, state, syn, los):
    """
    for state, e.g. '1' for command '0x02' will turn ON the RF output.
    """
    print("Setting RF output")
    n_bytes = 2  # number of bytes remaining in the packet
    n_command = 0x02  # the command number, such as '0x02' for RF output control.
    data = bytearray(64)
    data[
        0
    ] = (
        syn.ENDPOINT_HEX
    )
    data[1] = n_bytes
    data[2] = n_command
    data[3] = state
    los[int(device)].write(syn.ENDPOINT_DEC, data)


def reset_rf(device,syn):
    """
    for state, e.g. '1' for command '0x02' will turn ON the RF output.
    """
    print("Resetting RF")
    n_bytes = 2  # number of bytes remaining in the packet
    n_command = 0x03  # the command number, such as '0x02' for RF output control.
    data = bytearray(64)
    data[0] = syn.ENDPOINT_HEX
    data[1] = n_bytes
    data[2] = n_command
    data[3] = 0x00  # state
    device.write(syn.ENDPOINT_DEC, data)


def set_100_output(device,state, syn):
    """
    for state, e.g. '1' for command '0x02' will turn ON the RF output.
    """
    print("Setting 100MHz output to state " + str(state))
    n_bytes = 2  # number of bytes remaining in the packet
    n_command = 0x1E   # the command number, such as '0x02' for RF output control.
    data = bytearray(64)
    data[0] = syn.ENDPOINT_HEX  # chr(ENDPOINT)
    data[1] = n_bytes
    data[2] = n_command
    data[3] = state
    device.write(syn.ENDPOINT_DEC, str(data))

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
    data[0] = syn.ENDPOINT_HEX
    data[1] = n_bytes
    data[2] = n_command
    i_strt = 3

    # During testing: option to print bytes.
    # print("in set_f, bytes = :" + str(bytes))

    for index in range(5):
        data[int(index + i_strt)] = int(bytes[index + i_strt], 16)

    los[int(device)].write(syn.ENDPOINT_DEC, data)

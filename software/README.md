# Holography Software #

This README will outline, and make reference to, the following:
1. [Tutorials](#tutorials)
2. [ROACH2 FPGA](#roach2-fpga)
3. [Syntonic Synthesizers](#syntonic-synthesizers)
4. [Dependencies](#dependencies)
5. [Contributing](#contributing)

## Tutorials ##

Operational [scripts](scripts/) for how to operate the holography experiment are available on the McMahonGroupLab github page.
* [Syntonic synthesizer operations](scripts/synth.py) and [initialization](scripts/synth_init.py).
* [ROACH2 FPGA operations](scripts/poco.py), [initialization](scripts/poco_init.py) and [real-time signal readout](scripts/plot_cross.py).
* Saving to datafiles and further analysis.

## ROACH2 FPGA ##
`casperfpga` is a python library used to interact and interface with [**CASPER** Hardware](https://github.com/casper-astro/casper-hardware). This includes reading and writing registers in the experiment.  Installation instructions here: [`casperfpga`](https://pypi.org/project/casperfpga/) for full installation instructions.

Introductory [tutorials](https://github.com/casper-astro/tutorials_devel) for ROACH2 are available on the CASPER-astro github.  Read the CASPER [documentation](https://github.com/casper-astro/casperfpga) `casperfpga` for futher information on using ipython to communicate with CASPER Hardware and reconfigure it's firmware.

```python
import casperfpga
fpga = casperfpga.CasperFpga('skarab_host or roach_name')
fpga.upload_to_ram_and_program('your_file.fpg')
```

## Syntonic Synthesizers ##

The [syntonic synthesizers](https://www.mrcy.com/products/rf-and-mixed-signal/signal-sources/ds-3000-microwave-synthesizer) communicate with the computer via USB.  To connect with the synthesizers, search USB connections via:

```python
import usb.core
LOs = tuple(usb.core.find(find_all=True, idVendor=0x10c4, idProduct=0x8468))
```

## Dependencies ##

Python packages (for complete experiment):
* casperfpga
* usb
* time
* numpy
* struct
* sys
* logging
* datetime
* serial
* os
* array
* matplotlib
* getpass
* optparse

## Contributing ##

Fork [this](https://github.com/McMahonCosmologyGroup/holog-exp) repo, add your changes and issue a pull request.
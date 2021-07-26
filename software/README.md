# Software #

This README will outline, and make reference to, the following:
1. casperfpga
    1. [Introduction](#introduction)
    2. [Tutorials](#tutorials)
2. [Installation](#installation)
3. [Dependencies](#dependencies)
4. [Contributing](#contributing)


## casperfpga ##

### Introduction ###
`casperfpga` is a python library used to interact and interface with [**CASPER** Hardware](https://github.com/casper-astro/casper-hardware). This includes reading and writing registers in the experiment. 

Installation instructions here: [`casperfpga`](https://pypi.org/project/casperfpga/) for full installation instructions.

### Tutorials ###

Operational [tutorials](tutorials/) for how to operate the ROACH2 via casperfpga package are available on the McMahonGroupLab github page.

```python
import casperfpga
fpga = casperfpga.CasperFpga('skarab_host or roach_name')
fpga.upload_to_ram_and_program('your_file.fpg')
```

## FPGA Usage ##
Introductory [tutorials](https://github.com/casper-astro/tutorials_devel) for ROACH2 are available on the CASPER-astro github.

The provided [tutorials](https://github.com/casper-astro/tutorials_devel) are tailored specifically for the holography setup. 
* tutorial 1
* tutorial 2
* tutorial 3

Read the CASPER [documentation](https://github.com/casper-astro/casperfpga) `casperfpga` for futher information on using ipython to communicate with CASPER Hardware and reconfigure it's firmware.

```python
import casperfpga
fpga = casperfpga.CasperFpga('skarab_host or roach_name')
fpga.upload_to_ram_and_program('your_file.fpg')
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
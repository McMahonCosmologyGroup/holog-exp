# Software #

# casperfpga #

`casperfpga` is a python library used to interact and interface with [**CASPER** Hardware](https://github.com/casper-astro/casper-hardware). Functionality includes being able to reconfigure firmware, as well as read and write registers across the various communication interfaces.

This README will outline, and make reference to, the following:
1. Notes to Users
    1. [New Users](#new-users)
    2. [Existing Users](#existing-users)
2. [Installation](#installation)
3. [FPGA Usage](#fpga-usage)
    1. [casperfpga](https://casper.berkeley.edu/index.php/getting-started/)
    2. [tutorials](tutorials/)
4. [Contributing](#contributing)


## Notes to casperfpga users ##

### New Users ###

Not much to say to new users except welcome! It goes without saying that once you have cloned this respository you should make sure you're on the correct branch (usually **main**, unless you're a contributor) and always pull regularly. This, to make sure you have the latest version of casperfpga with the latest features. You can move on straight to [Installation](#installation).

Should you be an existing `corr` user, wondering where some of your functionality has gone when interfacing to your ROACH/2, please [look here](https://casper-toolflow.readthedocs.io/projects/casperfpga/en/latest/migrating_from_corr.html) for a detailed explanation on **how to migrate to `casperfpga`**.

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

See [`casperfpga`](https://pypi.org/project/casperfpga/) for full installation instructions.

```shell
$ git clone https://github.com/casper-astro/casperfpga
$ cd casperfpga/
$ git checkout master
$ sudo apt-get install python-pip
$ sudo pip install -r requirements.txt
$ sudo pip install casperfpga
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

## Contributing ##

Fork [this](https://github.com/McMahonCosmologyGroup/holog-exp) repo, add your changes and issue a pull request.
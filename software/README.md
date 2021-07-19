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

Not much to say to new users except welcome! It goes without saying that once you have cloned this respository you should make sure you're on the correct branch (usually **master**, unless you're a contributor) and always pull regularly. This, to make sure you have the latest version of casperfpga with the latest features. You can move on straight to [Installation](#installation).

Should you be an existing `corr` user, wondering where some of your functionality has gone when interfacing to your ROACH/2, please [look here](https://casper-toolflow.readthedocs.io/projects/casperfpga/en/latest/migrating_from_corr.html) for a detailed explanation on **how to migrate to `casperfpga`**.

## Installation ##
[`casperfpga`](https://pypi.org/project/casperfpga/) is now available on the Python Package Index (PyPI) and can be installed via [`pip`](https://pip.pypa.io/en/stable/). However, should you need to interface with a SNAP board, your installation workflow involves the extra step of installing against `casperfpga's requirements.txt`.

```shell
$ git clone https://github.com/casper-astro/casperfpga
$ cd casperfpga/
$ git checkout master
$ sudo apt-get install python-pip
$ sudo pip install -r requirements.txt
$ sudo pip install casperfpga
```

The distribution on the Python Package Index is, of course, a built-distribution; this contains an already-compiled version of the SKARAB programming utility `progska`, written in `C`. Operating Systems tested using `pip install casperfpga` include:

1. Ubuntu 14.04 LTS
2. Ubuntu 16.04 LTS
3. Ubuntu 18.04 LTS
4. Debian 8.x

Unfortunately the success of your installation using `pip` depends on the host OS of the installation, and you might need to rebuild the utility using the C-compiler native to your OS. In short, follow the more traditional method of installing custom Python packages.

```shell
# remove current casperfpga install files
$ cd /usr/local/lib/python2.7/dist-packages
$ sudo rm -rf casper*

# clone the repository to your working directory
$ cd /path/to/working/directory
$ git clone https://github.com/casper-astro/casperfpga.git
$ cd casperfpga
$ git checkout master
$ sudo pip install -r requirements.txt
$ sudo python setup.py install
```

To check that casperfpga has been installed correctly open an ipython session and import casperfpga. To avoid errors, move out of your cloned casperfpga repository directory before doing this test. `casperfpga.__version__` will output the build and githash version of your casperfpga library.

```shell
$ ipython
```
```python
In [1]: import casperfpga
In [2]: casperfpga.__version__
```

If you receive any errors after this please feel free to contact anyone on the [CASPER Mailing List](mailto:casper@lists.berkeley.edu), or check the [Mailing List Archive](http://www.mail-archive.com/casper@lists.berkeley.edu/) to see if your issue has been resolved already.

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
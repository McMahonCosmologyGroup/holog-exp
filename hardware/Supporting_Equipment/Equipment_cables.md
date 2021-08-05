# Equipment Cables

## Power Cables

### ROACH2 FPGA

The ROACH2 uses [ATX form-factor](https://en.wikipedia.org/wiki/ATX#Power_supply) power supplies and cables.

### Syntonic Synthesizers

Synthesizers are powered by 

## Serial Cables 

### ROACH2 FPGA

A standard [ethernet](https://en.wikipedia.org/wiki/Ethernet_over_twisted_pair) cable connects a computer system to the ROACH's serial port. 

### Syntonic Synthesizers

Both synthesizers are programmed by the computer via a USB, which acts as a serial port. One could use a serial connection other than USB as long as it acts as a serial port when communicating with the computer.

## SMA Connections

The BEE2 and IBOB boards use a custom 5-pin inline connector for their
RS-232 interfaces. A wiring diagram for this cable can be found
[here](http://bee2.eecs.berkeley.edu/wiki/Bee2Setup/serial_cable.pdf).
The 5-pin connector on the BEE2/IBOB end should be 1x5 0.1" (2.54mm)
spacing.

Suggested parts: Molex
[70066-series](http://www.molex.com/customer.html?supplierPN=050579005)
crimp housing +
[70058-series](http://www.molex.com/molex/products/listview.jsp?channel=Products&sType=s&query=70058)
or
[71851-series](http://www.molex.com/molex/products/listview.jsp?channel=Products&sType=s&query=71851)
crimp terminals.

Here is information on the CX4 cabling the UCB's Radio Astronomy Lab
uses at ATA and other observatories and in the
lab:

|                  |       |                             |                                                         |
| ---------------- | ----- | --------------------------- | ------------------------------------------------------- |
| iBob v1.3        | \-\>  | BEE2                        | 1.0 and 1.5m WL Gore Cu cables.                         |

Here is information on the SFP+ cabling used in the vegas system at
NRAO, Green
Bank:

|                                 |       |                          |                                                            |
| ------------------------------- | ----- | ------------------------ | ---------------------------------------------------------- |
| Roach2 Rev2 w/ SFP+ mezz. board | \-\>  | Brocade TurboIron 24X -- | 15m LC/LC duplex fiber cable, Tripp Lite PN N320-15M, with |

ATA purchased Zarlink (now Tyco) FO cables from:

  -   
    Anthony Thia
    TechBiz, Inc.
    48521 Warm Springs Blvd.,\#316
    Fremont, CA 94539
    Tel: 510 249 6800 x 101
    Fax: 510 249 6808
    anthony@techbizinc.com
    Anthony has provided very professional service. Very prompt,
    helpful, ...

Since 2010may14 these Zarlink part numbers are now Tyco products and are
still available from TechBiz.

Warnings about fiber optic units and more generally any sort of active
CX4 cable assembly.

  -   
    They are powered off of 3.3VDC supplied by the host (BEE2, iBob,
    Roach, NIC, switch) board's
    power supply via the CX4(Infiniband 4x) connector. Not all hosts
    support active (powered)
    CX4 links.
    Do not count on the BEE2 board having the necessary supply current
    to power
    a full or even partial complement of active CX4 links even though it
    has the
    auto-detect power up circuitry on every CX4 port.

<!-- end list -->

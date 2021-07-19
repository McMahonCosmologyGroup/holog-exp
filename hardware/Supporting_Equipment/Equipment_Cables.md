# Equipment Cables

## Power Cables

### ROACH

ROACH boards use standard [ATX
form-factor](http://en.wikipedia.org/wiki/ATX#Power_supply) power
supplies and cables.

For the vegas system at NRAO, Green Bank, the Roach2 rev2 boards are
powered by a [120W picoPSU power supply
unit](http://www.mini-box.com/s.nl/it.A/id.417/.f), which is powered by
a [TDK-Lambda +12VDC power
supply](http://us.tdk-lambda.com/lp/ftp/Specs/gws.pdf)

With its full-functionality PowerPC, ROACH is considered a
[DTE](http://en.wikipedia.org/wiki/Data_terminal_equipment). As such, a
[null-modem](http://en.wikipedia.org/wiki/Null_modem) RS-232 DB9 serial
cable should be used to connect another computer system to the ROACH's
serial port.

### SMA

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
| iBob v1.3        | \-\>  | BEE2                        | 10m and 15m Zarlink FO cables.                          |
| iBob v1.3        | \-\>  | BEE2                        | lab test only: 15m Tyco PARALIGHT FO cables.            |
| iBob v1.3        | \-\>  | ATA F Board                 | 1.0, 1.5, 2.0 and 3m WL Gore Cu cables.                 |
| iBob v1.3        | \-\>  | Roach1                      | 5m Zarlink FO cables and briefly 10m Zarlink FO cables. |
| BEE2             | \<-\> | BEE2                        | 1 and 1.5m WL Gore Cu cables.                           |
| BEE2             | \<-\> | BEE2                        | 0.5m WL Gore Cu cables during the self test.            |
| Roach1           | \<-\> | Fujitsu XG700               | 3m WL Gore Cu cables                                    |
| Roach1           | \<-\> | Fujitsu XG2000              | 3m WL Gore Cu cables                                    |
| Roach1           | \<-\> | Fujitsu XFPCXF4             | 3m WL Gore Cu cables                                    |
| Fujitsu switches | \<-\> | Chelsio N310E-CX 10 GbE NIC | 1m WL Gore Cu cables.                                   |
|                  |       |                             |                                                         |

Here is information on the SFP+ cabling used in the vegas system at
NRAO, Green
Bank:

|                                 |       |                          |                                                            |
| ------------------------------- | ----- | ------------------------ | ---------------------------------------------------------- |
| Roach2 Rev2 w/ SFP+ mezz. board | \-\>  | Brocade TurboIron 24X -- | 15m LC/LC duplex fiber cable, Tripp Lite PN N320-15M, with |
|                                 |       |                          | a Finisar PN FTLX8571D3BCL transceiver on each end         |
| High Performance Computer       | \<-\> | Brocade TurboIron 24X -- | 1.0m Mellanox copper cable, PN MC3309130-001               |
| High Performance Computer       | \<-\> | Brocade TurboIron 24X -- | 5.0m Molex copper cable, PN 74752-3501                     |
|                                 |       |                          |                                                            |

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

BEE2

  -   
    The BEE2's TI PT6521 8Amp @ 3.3V integrated switching
    regulator isn't able to power the usual loads on the board and more
    than 5 or so of the Zarlink
    FO transceivers. Maybe less.
    This component, P26, isn't overheating (w/ proper heatsink) rather
    it momentarily goes into over
    current shutdown; and then cycles on and off.

<!-- end list -->

  -   
    1 or 2 active FO Zarlink cables on 1 BEE2:
    (With \~12 other passive copper CX4 cables)
    BEE2 runs fine. ATA runs its \~ 16 Beamformer BEE2s this way.

<!-- end list -->

  -   
    3 active FO Zarlink cables on 1 BEE2:
    (With \~12 other passive copper CX4 cables)
    BEE2 runs fine I think but I've only run this for short tests.

<!-- end list -->

  -   
    4 active FO Xarlink cables on 1 BEE2:
    untested. Just never got around to this case.

<!-- end list -->

  -   
    5 active FO Zarlink cables on 1 BEE2:
    With \~12 other passive copper CX4 cables:
    BEE2 lock up after a few seconds.
    Totally UNusable.
    Have to power cycle to wake back up.

<!-- end list -->

  -   
    8 active FO Zarlink cables on 1 BEE2:
    With no other passive copper XC4 cables: BEE2 passed 1
    execution of the "TESTALL" command of the Test Suite.
    I didn't try anything else; never tried with any operational
    gateware.

iBob v1.3 Boards with 1 FO Zarlink cable:

  -   
    runs without trouble.
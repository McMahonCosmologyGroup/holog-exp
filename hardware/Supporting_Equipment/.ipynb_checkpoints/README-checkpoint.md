# Hardware #

This README lists all hardware used for holography measurements, and make reference to, the following:
1. [Source and Receiver](#source-and-receiver)
2. [Waveguides](#waveguides)
3. [Correlator Electronics](#correlator-electronics)


## Source and Receiver
All source and receiver electronics are listed in the table below.  The specifications column either details the waveguide side (WRx) or the product ID.

|   Item        |   Manufacturer   |   Number  |  Specifications  |
| --------------------- | ----- | -----| ----|
| WM Harmonic Mixer | Pacific Millimeter Products | 1 |  WR8  |
| DM Harmonic Mixer | Pacific Millimeter Products | 1 |  WR6.5  |
| GaAs Harmonic Mixer | Pacific Millimeter Products | 2 |  WR10  |
| Directional Coupler | Virginia Diodes Inc. | 1 |  WR8  |
| Directional Coupler | Virginia Diodes Inc. | 1 |  WR6.5  |
| Custom Transmitter | Virginia Diodes Inc. | 1 |  TX-182  |
| Variable Attenuator | Millimeter-Wave Technology & Solutions | 1 |  WR10  |
| Variable Attenuator | Custom Microwave Incorporated | 1 |  WR6  |
| Signal Synthesizer | Mercury Systems | 2 |  DS3000  |

### Signal Management

Two synthesizers from [Mercury](https://www.mrcy.com/) specify the frequency output of the source. The exact model used is the [DS-3000 MICROWAVE SYNTHESIZER](https://www.mrcy.com/products/rf-and-mixed-signal/signal-sources/ds-3000-microwave-synthesizer).  The synthesizers are controlled with USB.

The frequency from the synthesizers is sent to the source, which is a [Virginia Diodes](https://www.vadiodes.com/en/products/custom-transmitters) 75-170 GHz Modular Transmitter (S/N:Tx 182).  The source actively multiplies the signal to the desired frequency range. 

Two [harmonic mixers](http://pacificmillimeter.com/HarmonicMixers.html) mix the signals (one signal modulated, the other non-modulated), generating two interference frequencies.  These interference frequencies are then correlated by the ROACH FPGA which outputs the amplitude and phase information. 

## Waveguides
Waveguides are used to connect receiver electronics to the telescope readout, and are also used to extend the source signal closer to the telescope window.  The specifications column details the waveguide side (WRx) or the transition waveguide ID.

|   Item        |   Manufacturer   |   Number  |  Specifications  |
| --------------------- | ----- | -----| ----|
| Rectangular Horn | Custom Microwave Incorporated | 1 |  WR10  |
| Rectangular Horn | Custom Microwave Incorporated | 1 |  WR6  |
| Rectangular 6" Extension | Custom Microwave Incorporated | 2 |  WR10  |
| Rectangular 6" Extension | Custom Microwave Incorporated | 2 |  WR6  |
| Transition: Rectangular to Circular | Custom Microwave Incorporated | 2 |  CR10R-0940R  |

## Correlator Electronics
|   Item        |   Manufacturer   |   Number  |  LO chain  |
| --------------------- | ----- | -----| ----|
| 40dB Amplifier | Microwave Dynamics | 1 |  LO2  |
| 40dB Amplifier | RF-Lambda | 1 |  LO1  |
| 3dB Amplifier | RF-Lambda | 1 |  LO1  |
| Wilkinson Power Splitter | RF-Lambda | 1 |  LO1  |
| Mixer Diplexer | Pacific Millimeter Products | 2 |  1/LO chain  |
| Low-pass Filter | Pasternack | 2 |  1/LO chain  |
| 16dB Isolator | Pasternack | 10 |  5/LO chain  |
| 1N4001 Diode | Pasternack | 2 |  1/LO chain  |
| 100 uF Capacitor | Pasternack | 2 |  1/LO chain  |
| 2.4K Resistor | Pasternack | 2 |  1/LO chain  |

## Power Supplies

This table lists the power supplies required to power the holography experiment.

|   Item powered        |   V   |   I  |  Note   |
| --------------------- | ----- | -----| ----|
| Signal Synthesizer | 12VCC | 1.5A | LO1 |
| Signal Synthesizer | 12VCC | 1.5A | LO2 |
| 3dB Amplifier    | 4VCC  | 0.9A | Amplifies LO1  |
| 40dB Amplifier  | 28VCC  | 3.4A | Microwave Dynamics  |
| 40dB Amplifier  | 12VCC  | 1.0A | Microwave Dynamics  |
| 40dB Amplifier  | 12VCC  | 1.0A | RF-Lambda |
| RedHat Desktop   |  - |  - | Standard |
| Casper ROACH2 FPGA    | -  |  - | Standard |

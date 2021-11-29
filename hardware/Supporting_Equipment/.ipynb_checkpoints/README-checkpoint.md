# Hardware #

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

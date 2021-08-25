# Holography Hardware #

This README will outline, and make reference to, the following:
1. [ROACH2 FPGA](#roach2-fpga)
2. [Supporting Equipment](#supporting-equipment)

The schematic below serves as an example setup for performing holography. This is also the setup used at the University of Chicago in 2021. 


<!-- <meta name="viewport" content="width=device-width, initial-scale=1"> -->
<style>
* {
  box-sizing: border-box;
}

/* Create two equal columns that floats next to each other */
.column {
  float: left;
  width: 50%;
  padding: 10px;
  height: 300px; /* Should be removed. Only for demonstration */
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>

<body>

<h2>Two Equal Columns</h2>

<div class="row">
  <div class="column" style="background-color:#aaa;">
    <h2>Column 1</h2>
    <p>Some text..</p>
  </div>
  <div class="column" style="background-color:#bbb;">
    <h2>Column 2</h2>
    <p>Some text..</p>
  </div>
</div>
    
<div class="row">
  <div class="column" float: left; width: 50%;></div>
    <img src = 'photos/rf_holog.png' alt="RF Holography Setup" width="300"  >
  <div class="column"  float: right; width: 50%;></div>
    Some text
</div>
</body>

## ROACH2 FPGA ##

Processing the measured signals requires an FPGA. Holography at UChicago uses the Casper ROACHH2 board. ROACH stands for Reconfigurable Open Architecture Computing Hardware.  The full hardware specifications can be found at the [Casper ROACH2 public repository](https://github.com/casper-astro/casper-hardware/tree/master/FPGA_Hosts/ROACH2). 

The FPGA is powered via a standard power supply cable. The ROACH2 is programmed via Ethernet connection.  For installation instructions, see the [Casper ROACH2 repository](https://github.com/casper-astro/casper-hardware/tree/master/FPGA_Hosts/ROACH2). Once installed, see [holog-exp/software](https://github.com/McMahonCosmologyGroup/holog-exp/tree/main/software) for tutorials and software for data acquisition.

<img src = 'photos/roach.jpg' alt="centered image" >

## Supporting Equipment ##

All [datasheets](https://github.com/McMahonCosmologyGroup/holog-exp/tree/main/hardware/Supporting_Equipment/Datasheets) are provided.

- [Cables](Supporting_Equipment/Equipment_cables.md)
- [Signal Management](Supporting_Equipment/Signal_management.md)
- [Correlation Electronics](Supporting_Equipment/Correlation_electronics.md)

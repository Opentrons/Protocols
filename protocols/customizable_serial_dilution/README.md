# Customizable Serial Dilution

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, you can do a simple serial dilution in a 96-well plate using either a single-channel or multichannel pipette on the left mount of your OT-2. This can be useful for everything from creating a simple standard curve to a concentration-limiting dilution. You can use this as a standalone protocol or as part of a larger workflow. For more information (including results and other considerations), please see our [Technical Note](https://docs.google.com/document/d/1cwSAS52fSBOEI0Hb7U2paq5jS_G1LN2fB5TssJp-Au0/edit?usp=sharing).

This protocol uses the inputs you define for **dilution factor** and **dilution volume** to automatically infer the necessary volume for each individual transfer across your plate.

* ***Example:*** For a 1 in 10 dilution series, if you define a **dilution volume** of 90uL and a **dilution factor** of 10, your OT-2 will first add 90uL of diluent to each well in your plate, then transfer 10uL between each well in the plate.
![serial dilution](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/customizable-serial-dilution/Screen+Shot+2018-09-24+at+3.04.54+PM.png)

User-Defined Inputs
* Pipette Type (defined for left mount only)
* Dilution factor
* Number of dilutions (max: 11)
* Dilution volume
* Tip Reuse Strategy (default: reuse one tip throughout dilution series)

Materials Needed
* [Opentrons OT-2](http://opentrons.com/ot-2)
* [Opentrons OT-2 Run App (Version 3.1.2 or later)](http://opentrons.com/ot-app)
* 200uL or 300 uL Tiprack - [Opentrons tips suggested](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips-racks-9-600-tips)
* [12-row automation-friendly trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx))
* Clear flat-bottom 96-well polystyrene 96-well plate
* Diluent (Pre-loaded in row 1 of trough
* Samples/Standards (Pre-loaded in Column 1 of a standard flat-bottom 96-well plate)


### Time Estimate
* Varies. 2-5 minutes depending on pipette model chosen

## Process
1. Choose the pipette you want to use from the dropdown menu above.
    * ***Note:*** Your pipette should be installed on the ***left mount*** of your OT-2.
2. Set your dilution factor.
    * ***Example:*** If you want a 1:2 ratio of sample to total reaction volume, you would set your dilution factor to 2.
3. Set your number of dilutions (max = 11)
4. Set your dilution volume
5. Set your tip reuse strategy
    * ***Note:*** This defaults to no tip changes; adjust only if you want to change tips between each well.
6. Place your 12-row trough on the deck as indicated in the deckmap. **Make sure to add diluent to the first row of your 12-row trough.**
7. Place your 96-well plate on the deck as indicated in the deckmap. **Make sure to load your desired samples/standards into column 1 of your plate.**
8. Download your customized OT-2 Serial Dilution protocol using the blue "Download" button.
9. Upload into the Opentrons Run App and hit run!


### Additional Notes
Please reference our [Technical Note](https://docs.google.com/document/d/1cwSAS52fSBOEI0Hb7U2paq5jS_G1LN2fB5TssJp-Au0/edit?usp=sharing) for more information about the expected output of this protocol, in addition to expanded sample data from the Opentrons lab. You can also see a brief summary of our findings below.

* Figure 1: Raw average absorbance values for six 1.5-fold dilutions of blue food dye. Performed on an OT-2 running software version 3.1.2 fitted with a multi-channel 300uL pipette. Dilutions performed in a Corning 96-well EIA/RIA Easy Wash™ Clear Flat Bottom Polystyrene (3368) plate.
![absorbance chart](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/customizable-serial-dilution/Screen+Shot+2018-09-24+at+2.50.23+PM.png)

* Figure 2: Column-wise comparison between Opentrons OT-2 fitted with a multi-channel 300uL pipette and Agilent Bravo running multi-channel protocol. Average coefficient of variance (%CV) per column is shown in each table.
![OT-2 vs agilent bravo](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/customizable-serial-dilution/Screen+Shot+2018-09-24+at+2.59.24+PM.png)

* We understand that there are limitations to the use of this protocol, and we plan to make improvements soon. In the meantime, if you'd like to request a more complex dilution workflow, please use our [Protocol Development Request Form](https://opentrons-protocol-dev.paperform.co/). You can also download this Python file and modify it using our [API Documentation](https://docs.opentrons.com/). For additional questions about this protocol, please email support@opentrons.com.


###### Internal
Customizable Serial Dilution, v1
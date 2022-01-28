# Normalization Protocol from .CSV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Normalization

## Description
This protocol performs a custom sample normalization from a source plate to a second plate, diluting with water from a reservoir. Sample and diluent volumes are specified via .csv file in the following format, including the header line (empty lines ignored):

```
Source/destination plate well, Description, Concentration, Sample (µl)
nA01, 13377_16S_Bac, 3.28, 12.52
```

The protocol performs the following operations:
1. Transfers 40 µL of water to each well of the destination plate using the p300
2. Removes x µL of water from the well and adds x µL of DNA sample according to the line in the CSV.
3. Mixes the samples 3 times.

**Update (Jan 28, 2022)**: This protocol has been updated. The user can now select between the [Opentrons P300 GEN2 Single-Channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette) or the [Opentrons P300 GEN2 8-Channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette).

![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [An Opentrons compatible 96-well sample source plate](https://labware.opentrons.com/?category=wellPlate)
* [An Opentrons compatible 96-well target plate](https://labware.opentrons.com/?category=wellPlate)
* [NEST 12-channel reservoir 15ml](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)
* [Opentrons 20µl and 300µl filter tipracks](https://shop.opentrons.com/collections/opentrons-tips)
* [Opentrons P20 GEN2 Single-Channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P300 GEN2 Single-Channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette) or the [Opentrons P300 GEN2 8-Channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette).

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

NEST 12-channel reservoir (slot 4)
* channel 1: water for dilution

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the normalization .csv file
2. Select your source plate containing DNA samples (located on slot 7)
3. Select your destination plate where samples will be mixed with water (located on slot 1)
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
8. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

##### Internal
66e60f

# 66e60f: Normalization protocol from CSV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Normalization

## Description
This protocol performs a custom sample normalization from a source plate to a second plate, diluting with water from a reservoir. Sample and diluent volumes are specified via .csv file in the following format, including the header line (empty lines ignored):

```
Plate, Well, SampleID, Concentration, VolumeToDispense
A, A1, Sample1, 3.28, 12.52
```
The plate is either A or B

The protocol accomplishes the following
1. Transfers 40 µL of water to each well of the destination plate using the p300
2. Removes x µL of water from the well and adds x µL of DNA sample according to the line in the CSV.
3. Pools diluted DNA samples into a tube on the tube-rack.
For more details see Protocol Steps below

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

### Labware
* [NEST 12-Well Reservoirs, 15 mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* [An Opentrons compatible 96-well sample source plates](https://labware.opentrons.com/?category=wellPlate)
* [An Opentrons compatible 96-well target plates](https://labware.opentrons.com/?category=wellPlate)

### Pipettes
* [P300 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/) or
* [P300 multi-Channel (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [P20 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

**Tip racks**

* [Opentrons 200 µL filter tiprack](https://shop.opentrons.com/opentrons-200ul-filter-tips/)
* [Opentrons 20 µL filter tiprack](https://shop.opentrons.com/opentrons-20ul-filter-tips/)


### Reagents
NEST 12-channel reservoir (slot 11)
* channel 1: Water for dilution
* channel 2: Water waste for initial distribution

---

### Deck Setup
* If the deck layout of a particular protocol is more or less static, it is often helpful to attach a preview of the deck layout, most descriptively generated with Labware Creator. Example:
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

### Reagent Setup
* Water Reservoir: slot 11
![Water reservoir on 11](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/66e60f/water_res.jpg)
* Tuberack: slot 5  
![Tuberack](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/66e60/tuberack.jpg)

### Protocol Steps
1. The protocol distributes water to each column that has a well in the inout csv file using the 300 µL multi-channel pipette to the final plate (A and B). These tips blow out into the water reservoir well 2 and are then discarded.
2. A volume of water equal to the DNA volume in the csv line is removed from the well and dispensed into tube A1 or B1 on the tuberack with a blow out and touch tip.
3. The same volume of DNA is transferred from DNA plate A or B to final plate A or B using the same tip. An air gap is added to prevent contamination of other samples.
4. The tip touches the sides of the destination well.
5. The tip blows out into tube C1 or D1.
6. The tip is parked for reuse.
7. Step 2 to 6 are repeated for each well.
8. Reusing each parked tip in turn 5 µL of diluted DNA sample is transferred, with an air gap, to the DNA pooling tube in position in position A2. Finally the tip is discarded

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

# Plate Filling Heat Inactivated Covid Samples for PCR

### Author
[Opentrons](https://opentrons.com/)

## Categories
* PCR
	* PCR Prep

## Description
This protocol preps a 96 well plate with heat inactivated Covid samples and mastermix, along with a positive and negative control for further processing on a Quant-5. The protocol can be considered in 3 main sections:

* Controls added to 96 well plate
* Mastermix added to 96 well plate
* Samples added to 96 well plate

Explanation of complex parameters below:
* `Number of Samples`: Specify the number of samples (1-94) to run on this protocol. Note: samples will be picked by row in the tube racks, in order of slots 7, 8, 10, and 11.
* `Plate`: Specify whether loading the microamp (I48HO) 96 well plate, or another 96 well plate.
* `P20 Mount`: Specify which side to mount your P20 Multi Channel Pipette.

---

### Labware
* [Opentrons 20ul tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* Microamp 200ul well plate
* Opentrons 4-in-1 tuberack with 4x6 tube insert (1.5mL tubes)


### Pipettes
* [P20 Multi Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette)


---

### Deck Setup
* This is the deck setup for a run with 94 samples (bottom two rows of slot 11 are not populated).
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/2df9f8/Screen+Shot+2021-08-04+at+10.09.08+AM.png)

### Reagent Setup
* Note: Mastermix and positive/negative control tubes should be the same tube.
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/2df9f8/Screen+Shot+2021-08-04+at+10.09.25+AM.png)


---

### Protocol Steps
1. Negative control added to A1 of plate
2. Positive control added to A2 of plate
3. Mastermix added to 96 well plate for all wells containing sample.
3. Samples added to 96 well plate starting from well A3 across the row

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
2df9f8

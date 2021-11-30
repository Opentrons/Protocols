# Serial Dilution of Analyte Stock

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Serial Dilution

## Description
This protocol serially dilutes stock from the stock tube rack (slot 4) to up to 15 tubes in the dilution rack (see diagram below). Volume, tube source, tube destination, and slot source/destination are all read by the robot to perform all transfer steps. 2 mix steps are also included at half tube depth to avoid pipette submersion.

Explanation of complex parameters below:
* `csv`: Import a csv file with the following format (you do not need to specify mix steps):
![csv layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/469c70/Screen+Shot+2021-11-30+at+10.36.56+AM.png)

* `P1000 Single-Channel Mount`: Specify which mount (left or right) to host the P1000 single-channel pipette.




---

### Labware
* [Opentrons 4-in-1 tube rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Opentrons 1000ul Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [Nest 1-well Reservoir 195mL](https://shop.opentrons.com/collections/reservoirs/products/nest-1-well-reservoir-195-ml)



### Pipettes
* [P1000 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/469c70/Screen+Shot+2021-11-30+at+7.51.44+AM.png)

---

### Protocol Steps
1. Stock is transferred from tube 1 of the stock rack to the first dilution rack.
2. The stock is stepped down according to the csv.
3. Steps 1 and 2 are repeated for all stock tubes.


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
469c70

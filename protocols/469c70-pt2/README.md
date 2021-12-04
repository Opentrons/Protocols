# Fresh Spiking with CSV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Serial Dilution

## Description
This protocol transfers one-to-one analyte from the analyte tube rack on slot 2 to the final tube rack on slot 3. It then transfers plasma to all tubes up to the number specified by the user in the final tube rack. The solution in each tube is mixed upon dispensing the plasma.

Explanation of complex parameters below:
* `csv`: Import a csv file with the following format (you do not need to specify mix steps). Note that volumes should be in microliters:
![csv layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/469c70/Screen+Shot+2021-12-03+at+9.32.11+AM.png)

* `P20 Single-Channel Mount`: Specify which mount (left or right) to host the P20 single-channel pipette.
* `P1000 Single-Channel Mount`: Specify which mount (left or right) to host the P1000 single-channel pipette.


---

### Labware
* [Opentrons 4-in-1 tube rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Opentrons 1000ul Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [Opentrons 20ul Tips](https://shop.opentrons.com/collections/opentrons-tips)



### Pipettes
* [P1000 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P20 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/469c70/Screen+Shot+2021-11-30+at+7.50.04+AM.png)

---

### Protocol Steps
1. Matrix is added to the final racks on slot 2 and 4 via multi dispense (1 tip) according to the csv.
2. Analyte is added to final racks according to csv. Mix after with 2 repetitions.
3. Resulting solutions in final racks are transferred according to the csv. Mix after with two repetitions.


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
469c70-pt2

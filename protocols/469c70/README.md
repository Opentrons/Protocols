# Serial Dilution of Analyte Stock

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Serial Dilution

## Description
This protocol serially dilutes stock from the stock tube rack (slot 4) to up to 15 tubes in the dilution rack (see diagram below). Volume, tube source, tube destination, and slot source/destination are all read by the robot to perform all transfer steps. 2 mix steps are also included at half tube depth to avoid pipette submersion. The user can specify any number of tube racks (15 or 24) in the csv, and the protocol will accommodate.

Explanation of complex parameters below:
* `csv`: Import a csv file with the following format (you do not need to specify mix steps). Note that volumes should be in mL. Also note that unless calling the reservoir, an initial tube volume should be placed for all tubes.
![csv layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/469c70/Screen+Shot+2021-12-27+at+11.52.01+AM.png)
* `Number of tipracks`: Specify how many tipracks of each type below. For 1000ul tipracks, tipracks should be placed in order of slots 6, 9, and 11. For 20ul tipracks, tipracks should be placed in order of slots 8 then 10. For volumes less than 100ul, the P20 pipette will be used. For all volumes greater than 100ul, the P1000 pipette will be used.
* `Aspirate/dispense/blowout rate`: A value of 1 returns a defualt rate for both pipettes. A value of 1.5 is 50% faster than the default for both pipette, 0.33 is 1/3 of the default rate, etc.
* `P1000/P20 Single-Channel Mount`: Specify which mount (left or right) to host the P1000 and P20 single-channel pipettes.




---

### Labware
* [Opentrons 4-in-1 tube rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Opentrons 1000ul Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [Nest 1-well Reservoir 195mL](https://shop.opentrons.com/collections/reservoirs/products/nest-1-well-reservoir-195-ml)



### Pipettes
* [P1000 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P20 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)

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

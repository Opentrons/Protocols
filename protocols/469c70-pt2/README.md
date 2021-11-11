# Sample Prep MALDI spotting - Fresh Spiking

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Serial Dilution

## Description
This protocol transfers one-to-one analyte from the analyte tube rack on slot 2 to the final tube rack on slot 3. It then transfers plasma to all tubes up to the number specified by the user in the final tube rack. The solution in each tube is mixed upon dispensing the plasma.

Explanation of complex parameters below:
* `Number of analyte tubes`: Specify the number of analyte tubes for this run.
* `Volume of plasma (ul)`: Specify the volume of plasma to distribute to each tube in the final tube rack.
* `Volume of analyte`: Specify the volume of analyte to distribute to each tube in the final tube rack.
* `P20 Single-Channel Mount`: Specify which mount (left or right) to host the P20 Single-Channel Pipette.
* `P1000 Single-Channel Mount`: Specify which mount (left or right) to host the P1000 Single-Channel Pipette.


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
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/469c70/Screen+Shot+2021-11-11+at+2.26.41+PM.png)

---

### Protocol Steps
1. Add 5µl analyte from 2 mL Eppendorf tube in analyte tube rack to 2 mL Eppendorf tube in final tube rack.
2. Transfer 195 µL of Plasma from plasma tube rack to 2 mL Eppendorf tubes in final tube rack.  
3. Mix 5 times


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

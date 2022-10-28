# CGE Buffer Load


### Author
[Opentrons](https://opentrons.com/)


## Categories
* Sample Prep
	* Plate Filling


## Description
This protocol preps tubes from a custom csv with liquid handling parameters also present in the csv. The csv header has the following parameters in the first row: Liquid Name, Change Tip, Transfer Volume, Source Container Type, SourceSlot, SourceWell, Destination Container Type, DestinationSlot,DestinationWell, Aspirate Flow Rate, Aspirate Position From Bottom, Aspirate Delay (Y/N), Aspirate Delay (s), Aspirate Delay (mm), Aspirate Touchtip (Y/N), Aspirate Touchtip (mm), Aspirate Airgap, Dispense Flow Rate, Dispense Position From Bottom, Dispense Delay (Y/N), Dispense Delay (s), Dispense Delay (mm), Dispense Touchtip (Y/N), Dispense Touchtip (mm),Dispense Blowout, Dispense Airgap, Volume in A1, Volume in B1, Volume in B2, Volume in A2, Volume in A3, Vome MAX. It is crucial that the header of the csv is exactly in that order. The user can specify up to 3 slots for the for the source racks (Falcon racks, slots 1, 2, and 3), and up to 3 slots for the destination racks (CGE racks, slots 4, 5, 6). The user must specify how many racks of each are on the deck at the start of the run, and put the racks in order of numerical lowest to highest (i.e. slots 4, and 5 for only two destination racks on the deck).


### Labware
* CGE v2 36 Tube Rack with clear 2 mL
* [Opentrons 6 Tube Rack with Falcon 50 mL Conical](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Opentrons 96 Tip Rack 1000 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)


### Pipettes
* [Opentrons P1000 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0cbd26/Screen+Shot+2022-10-28+at+3.31.57+PM.png)



### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit "Run".


### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).


###### Internal
0cbd26

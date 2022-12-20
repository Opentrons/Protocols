# Cell Culture


### Author
[Opentrons](https://opentrons.com/)


## Categories
* Sterile Workflows
	* Cell Culture


## Description
This protocol performs a custom 12-factor cell culture assay in a 96-deepwell plate. Please use [this example .csv template](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0909e6/ex4.csv) to format your worklist! When uploading your file below, please ensure it is saved in the format `.csv`.


### Labware
* [Opentrons 6 Tube Rack with Falcon 50 mL Conical](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [USA Scientific 96 Deep Well Plate 2.4 mL #1896-2000](https://www.usascientific.com/2ml-deep96-well-plateone-bulk.aspx)
* Opentrons 96 Filter Tip Rack 200 µL
* Opentrons 96 Filter Tip Rack 1000 µL


### Pipettes
* [Opentrons P1000 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Opentrons P300 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0909e6/deck3.png)


### Reagent Setup
![reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0909e6/reagents2.png)  
Note that factors 16-30 are arranged in the same format as factors 1-15.


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
0909e6

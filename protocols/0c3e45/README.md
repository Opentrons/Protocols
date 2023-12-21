# Liquid Transfer


### Author
[Opentrons](https://opentrons.com/)



# Opentrons has launched a new Protocol Library. This page won’t be available after January 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* Sample Prep
	* Plate Filling


## Description
This protocol performs a basic plate filling protocol for 9 plates from one source reservoir. The same set of tips is used for the entire protocol, and tips are tracked across protocols.

The protocol is adapted to Python from [this Protocol Designer protocol](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0c3e45/pd.json).


### Labware
* [NEST 96 Well Plate 200 µL Flat #701011](http://www.cell-nest.com/page94?_l=en&product_id=85)
* [NEST 1 Well Reservoir 195 mL #360103](http://www.cell-nest.com/page94?_l=en&product_id=102)
* [Opentrons 96 Filter Tip Rack 200 µL](https://shop.opentrons.com/opentrons-200ul-filter-tips/)


### Pipettes
* [Opentrons P300 8 Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0c3e45/deck.png)


### Reagent Setup
![reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0c3e45/reagents.png)


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
0c3e45

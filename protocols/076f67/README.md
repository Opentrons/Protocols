# SARS-COV2 (VSV) Neutralization Assay


### Author
[Opentrons](https://opentrons.com/)



# Opentrons has launched a new Protocol Library. This page won’t be available after March 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* Sample Prep
	* Plate Filling


## Description
This protocol performs the SARS-COV2 (VSV) Neutralization Assay on the OT-2. The user may select how many source-destination plate pairs (1-3) for this protocol, as well as select labware. The protocol will pause if the tips are depleted, prompting the user to refill tips. 


### Labware
* Falcon 96 Well Plate 200 µL
* [Corning 96 Well Plate 360 µL Flat #3650](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Corning%C2%AE-96-well-Solid-Black-and-White-Polystyrene-Microplates/p/corning96WellSolidBlackAndWhitePolystyreneMicroplates)
* [Agilent 1 Well Reservoir 290 mL #201252-100](https://www.agilent.com/store/en_US/Prod-201252-100/201252-100)
* [NEST 12 Well Reservoir 15 mL #360102](http://www.cell-nest.com/page94?_l=en&product_id=102)
* [Opentrons 96 Tip Rack 300 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)


### Pipettes
* [Opentrons P300 8 Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/076f67/deck.png)



### Protocol Steps
1. Serum added
2. Individual serum added
3. Serially dilute down source plates
4. Add virus to plates
5. Incubate plates
6. Discard media
7. Transfer media from source plate to destination plate
8. Incubate plates
9. Dispense overlay in plates

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
076f67

# Normalization Using .csv File


### Author
[Opentrons](https://opentrons.com/)



# Opentrons has launched a new Protocol Library. This page won’t be available after January 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* Normalization
	* Normalization and Pooling


## Description
This is a normalization protocol that transfers diluent buffer from a 50 mL tube into an empty 96-well PCR plate, then transfers sample from a 96-well PCR plate on the temperature module into the plate with the diluent.


### Modules
* [Opentrons Temperature Module (GEN2)](https://shop.opentrons.com/temperature-module-gen2/)


### Labware
* Eppendorf Twin.tec 96 Well Plate 150 µL  #0030129512
* Eppendorf Twin.Tec 96 on Aluminum Block 150 µL
* Starlab 96-Well PCR Plate, Skirted 200 µL #E1403-5200
* Starlab 96-Well PCR Plate on Aluminum Block 200 µL
* [Opentrons 96 Filter Tip Rack 20 µL](https://shop.opentrons.com/opentrons-20ul-filter-tips/)
* [Opentrons 96 Filter Tip Rack 200 µL](https://shop.opentrons.com/opentrons-200ul-filter-tips/)
* [Opentrons 10 Tube Rack with Falcon 4x50 mL, 6x15 mL Conical](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)


### Pipettes
* [Opentrons P20 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Opentrons P300 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/08207f/deck.png)



### Protocol Steps
1. Transfer X uL (from .csv file) of buffer from tube rack A3 to X number of wells in 96 well plate (same tips), slot6 (the number of samples will be specified in .csv file); use p300/or p20 single channel.
2. Use single channel p20 to add X uL of sample (data in the .csv file) from A1 (slot3) to A1 well in end-point-plate (slot6) (well A1 to well A1, well B1 to well B1 …). Use 10ul air gap and blow out, new tip each time.
3. Repeat steps 2 across plate


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
08207f

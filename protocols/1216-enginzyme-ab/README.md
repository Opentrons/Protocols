#  DoE with Variable Number of Factors and Special Fields

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Distribution

## Description
Using this protocol, your robot will be able to distribute a number of reagents into a 96-well plate. User can define the locations of the stocks by uploading a location CSV in the field below. The reagents that make up each well in the 96-well plate are specified in a separate reagent CSV. See Additional Notes for the required CSV layouts.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your location CSV.
2. Upload your reagent CSV.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".

### Additional Notes
* Slot **2** and **6** are occupied by the 96-well plate and tiprack. You can put your reagent containers in any other slot on the robot.
* Here are list of container type you can use in your location csv:
    * opentrons-tuberack-15_50ml
    * opentrons-tuberack-15ml
    * opentrons-tuberack-2ml-eppendorf
    * opentrons-tuberack-2ml-screwcap
    * opentrons-tuberack-50ml
    * trough-12row
    * 96-deep-well
    * if you would like to use other containers, please email support@opentrons.com.

* Location CSV Layout:
    * Each row represents a reagent

    ![location csv](	https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1216-enginzyme-ab/location_csv.png)


* Reagent CSV Layout:
    * Each row represents a well, starting from A1, B1... to H12.

    ![reagent csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1216-enginzyme-ab/reagent_csv.png)

###### Internal
dRzOlXKI
1216

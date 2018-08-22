# 96-Well Plate Consolidation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Consolidation

## Description
With this protocol, your robot can consolidate the contents of an entire 96-well plate into a single 2 mL tube using a p50 single channel pipette, with tip change every time. A CSV file containing volumes to be transferred from each well is required to be upload in the field below. Please see CSV format in Additional Information.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your volume CSV file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Transfer appropriate volume from wells of the 96-well plate to a single 2 mL tube in well A1 of tube rack.

### Additional Notes
* New tip is used for each liquid transfer. If you want to use one tip throughout the entire run, or change your labware, see our [API documentation](https://docs.opentrons.com/index.html) for tips on how to modify your Python script.
* CSV file format (8 X 12)
    * no headers
    * each cell represents a well in the 96-well plate
    * volumes must be in integers

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|----|----|----|
| 2 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| 3 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| 4 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|   |   |   |   |   |   |   |   |   |    |    |    |
|   |   |   |   |   |   |   |   |   |    |    |    |
|   |   |   |   |   |   |   |   |   |    |    |    |
|   |   |   |   |   |   |   |   |   |    |    |    |

###### Internal
HiS8CHvE
1135

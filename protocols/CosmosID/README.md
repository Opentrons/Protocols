# DNA Library Quantification using qPCR

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, you robot can perform DNA library Quantification via qPCR. The robot first prepare 5 serial dilutions of E. coli DH10B Control Library. Then the robot prepare 3 serial dilutions of each DNA sample library. MasterMix solution is then prepared. The robot distributes the MasterMix solution, and appropriate reagents in the PCR plate. Each time, user can use up to 4 DNA sample libraries.


### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".

### Additional Information
* The final layout of the plate is as follow:  

| Standard 1 | Standard 1 | Standard 1 | NTC | Sample 1.1 | Sample 1.1 | Sample 2.1 | Sample 2.1 |   |   |   |   |
|------------|------------|------------|-----|------------|------------|------------|------------|---|---|---|---|
| Standard 2 | Standard 2 | Standard 2 | NTC | Sample 1.2 | Sample 1.2 | Sample 2.2 | Sample 2.2 |   |   |   |   |
| Standard 3 | Standard 3 | Standard 3 | NTC | Sample 1.3 | Sample 1.3 | Sample 2.3 | Sample 2.3 |   |   |   |   |
| Standard 4 | Standard 4 | Standard 4 |     |            |            |            |            |   |   |   |   |
| Standard 5 | Standard 5 | Standard 5 |     |            |            |            |            |   |   |   |   |
|            |            |            |     |            |            |            |            |   |   |   |   |
|            |            |            |     |            |            |            |            |   |   |   |   |
|            |            |            |     |            |            |            |            |   |   |   |   |


###### Internal
N8wmZsYk
1114
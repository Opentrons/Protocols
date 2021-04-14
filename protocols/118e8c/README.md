# FluoGene HLA NX 96-Well Setup

### Author
[Opentrons](https://opentrons.com/)

## Categories
* qPCR Setup
     * FluoGene HLA

## Description
FluoGene HLA NX 96-Well Setup. This protocol performs the setup of two Fluogene 96-well trays to perform a multiplexed TaqMan-based assay.

Links:
* [json protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-04-02/dc23h0c/FluoGene%20HLA%20NX%20Match-96%20ver.%2057%20with%207.5.json)

This protocol is a translation of the attached json protocol to python with a couple additional features for faster completion time and tracking of reservoir columns and tips between protocol runs: A multi-channel p20 pipette is used to dispense 4 ul of water and 4 ul pcr mix to well H1 of each tray by using only the rear-most channel of the pipette. Then the p300 single is used to mix the DNA dilution with the pcr mix and transfer it to the reagent reservoir. The p20 multi is then used to distribute 8 ul of this mixture to each of the remaining wells of the two 96-well trays.
The deck layout can be displayed by uploading the attached json protocol to the [Opentrons Protocol Designer web page](https://opentrons.com/protocols/designer/).
### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* FluoGene HLA Reagents

## Process
1. Input your liquid handling parameters below.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map below.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

###### Internal
118e8c

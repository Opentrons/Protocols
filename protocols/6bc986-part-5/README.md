# Distribution of Elution Buffer

### Author
[Opentrons](https://opentrons.com/)


# Opentrons has launched a new Protocol Library. This page won’t be available after January 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* PCR
     * PCR Prep

## Description
Part 5 of 6: Distribution of Elution Buffer

Links:
* [Distribution of Sample Lysis Buffer](https://protocols.opentrons.com/protocol/6bc986)
* [Distribution of Prot K (Apostle)](https://protocols.opentrons.com/protocol/6bc986-part-2)
* [Transfer of DNA Template](https://protocols.opentrons.com/protocol/6bc986-part-3)
* [Distribution of Master Mix](https://protocols.opentrons.com/protocol/6bc986-part-4)
* [Distribution of Elution Buffer](https://protocols.opentrons.com/protocol/6bc986-part-5)
* [Distribution of Prot K (Qiagen)](https://protocols.opentrons.com/protocol/6bc986-part-6)

This protocol is a translation of the attached json protocol [json protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-04-19/eg83ite/2.%20Elution%20Buffer-edit.json) to python with a couple additional features for control of the blow out location in order to place it near the bottom of the source reservoir well: 20 ul elution buffer is distributed from a reservoir to the columns of a 96-well plate with a blow out of the disposal volume occuring in a location close to the bottom of the source well.
The deck layout can be displayed by uploading the attached json protocol to the [Opentrons Protocol Designer web page](https://opentrons.com/protocols/designer/).

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input your number of samples (1-96) and well bottom clearances (in mm) for aspiration and dispense using the parameters on this page.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".

###### Internal
6bc986-part-5

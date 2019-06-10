# CSV Cherrypicking

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol performs cherrypicking from 4 4x6 tube racks to a 96-well PCR plate from an input CSV file. See 'Additional Information' below for proper file formatting, reagent and deck setup, and transfer scheme.

---

You will need:
* [VWR 96-well PCR plate #82006-636](https://us.vwr.com/store/product/4679497/vwr-96-well-pcr-and-real-time-pcr-plates)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 1.5ml Eppendorf Tubes
* [12-Row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [Opentrons 10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV file (according to the format shown in 'Additional Notes' below).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol parses the CSV file for each source well and its associated volume from each of 4 tube racks.
8. The input volume is transferred from each source well to each of its destination wells. Tips are changed between each group of source and destination wells.

### Additional Notes
![CSV Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1578/CSV_format.png)  
Ensure tube racks are in listed in order. Include empty rows and rack names.

![Deck Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1578/deck_setup_2.png)

![Trough Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1578/trough_setup.png)

![Transfer Scheme](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1578/transfer_scheme.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
izZ90Ed6  
1578

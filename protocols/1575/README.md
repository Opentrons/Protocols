# Cherry Picking to Multiple Plates

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol performs cherrypicking from a 96-deep well source plate to up to 9 destination plates. The protocol allows for the user to select transfer volume, the number of destination plates, and the type of destination plate (96- or 384-well). The source and destination wells are specified and uploaded on a single CSV file. See 'Additional Information' below for proper file formatting.

---

You will need:
* [96-Deep well source plate](https://www.usascientific.com/2ml-deep96-well-plateone-sterile.aspx)
* 96-Well standard destination plates
* 384-Well standard destination plates
* [P50 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the distribution volume (in µl), the number of destination plates, and the type of destination plate (96- or 384-well), and upload your CSV file (according to the format shown in 'Additional Notes' below).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol parses the CSV file for each source well and its associated destination wells on all specified plates.
8. The input volume is transferred from each source well to each of its destination wells. Tips are changed between each group of source and destination wells.

### Additional Notes
![CSV Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1575/CSV_setup.png)
Ensure plates are in listed in order. Destination plates can continue right for up to 9 plates. Source wells can continue down for up to 96 wells.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
5PqCcOj4  
1575

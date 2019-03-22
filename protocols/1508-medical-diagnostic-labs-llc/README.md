# Barcode Transfer

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
    * Well-to-well Transfer

## Description
This protocol performs performs barcode plate mapping from a 96-well deep well elution plate to a 96-well half-skirt Axygen plate, one well at a time. Source and destination wells as well as transfer volumes are input via CSV. [See 'Additional Notes' below for proper CSV formatting.]

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Labware
* [p10 Single-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [96-well deep Axygen Plate](https://www.fishersci.com/shop/products/axygen-96-round-deep-well-plate/14223345#?keyword=96-well+deep)
* [96-well half-skirt Axygen plate](https://www.fishersci.com/shop/products/axygen-96-well-half-skirt-pcr-microplates-8/p-4371201)

## Process
1. Choose your CSV file that specifies transfer information.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol parses through the input CSV, reading each row as a transfer. From the row, a specified source well, transfer volume, and destination well is determined.
8. The volume for the transfer is transferred from the source well of the deep-well plate to the corresponding destination well of the tall PCR plate.
9. The process is repeated for each row in the CSV, using a fresh tip each time.
10. The protocol exits and the user manually seals the source barcode plate and the destination plate.

### Additional Notes
![CSV Format](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1508-medical-diagnostic-labs-llc/CSV_setup.png)

###### Internal
QQ86fp3w  
1508

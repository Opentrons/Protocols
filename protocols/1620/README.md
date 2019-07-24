# CSV Sample Recombination

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol allows your robot to cherrypick from a custom 6x8 tuberack into a single 2 mL tube through an input CSV file specifying transfer volumes. See 'Additional Notes' below for the required CSV layout.

---

You will need:
* Custom 6x8 1.5ml tube rack
* [Opentrons 2ml tube rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Opentrons P10 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [Greiner Sapphire 10ul pipette tips # 771261](https://shop.gbo.com/en/usa/products/bioscience/liquid-handling/sapphire-tips/bs-sapphire-filter-tips/)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV file, select the mount for your P10 pipette, and select your destination tube type
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The specified volume of each sample will be transferred to the destination pooling tube. For small volumes (<10µl), a touch tip is performed at the source tube. Only non-zero entries are transferred to conserve tips and time.

### Additional Notes
CSV file layout:
![CSV layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1620/csv_layout.png)

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
FYFhRI0K  
1620

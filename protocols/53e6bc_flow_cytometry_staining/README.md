# Flow Cytometry Staining

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* Assay

## Description
This protocol performs custom flow cytometry staining from a previously created custom mastermix from antibodies. Two temperature modules are used in the case of more than 8 samples. Please follow these instructions for using 2 temperature modules simultaneously:

1. [Setup SSH](https://support.opentrons.com/en/articles/3203681-setting-up-ssh-access-to-your-ot-2) if necessary and [SSH into to your robot](https://support.opentrons.com/en/articles/3287453-connecting-to-your-ot-2-with-ssh).
2. run `$ls /dev/tty*`  
you are looking for two values with the format `/dev/ttyACM*`  
you will use those values in lines 81 and 82 of the code.

If you need to know which tempdeck is hooked up to which port:
1. unplug one of the modules
2. run $ls /dev/tty* : the results correlates to the module that is plugged in
3. plug the other module in and run ls /dev/tty* again, you will be able to
   know the value of the second module

Links:
* [Antibody Mastermix Creation](./53e6bc_mastermix_creation)

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [VWR 96-deepwell plate 2.2ml #10755-250](https://us.vwr.com/store/product/4693284/vwr-96-well-deep-well-plates)
* [VWR conical self-standing tubes 5ml #89497-740](https://us.vwr.com/store/product/11707931/self-standing-sample-tubes-5-and-10-ml-globe-scientific) (or equivalent) seated in [Opentrons 4-in-1 tuberack](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1) with 3x5 insert
* [Opentrons temperature module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) with [aluminum plate](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Opentrons P300 GEN1 single-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [Opentrons P300 GEN1 multi-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 300ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

3x5 tuberack for 5ml screwcap tubes (slot 2)
* tube A1: mastermix (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P300 and P10 single-channel pipettes, the number of samples, and the antibody .csv file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
53e6bc

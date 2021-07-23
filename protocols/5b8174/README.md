# Custom Multi-CSV Transfer for PCR Prep

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
This protocol performs transfers of positive controls and patient samples to a 384 well plate loaded onto a temperature module. All labware and transfers can be controlled through the CSV files that are used as input for this protocol.

Explanation of complex parameters below:
* `P20 Single Channel Pipette Mount Position`: Choose the mount position of your pipette.
* `Control CSV File`: Upload the CSV file for controls here. You can download an [example CSV file here](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5b8174/Control.csv) OR follow the format directly below.
```
Rack,Sr.Barcode, ,Dest.Barcode,Dest.List Name,
1,,PCRCTR15000004,,,
2,,,,,
3,,,,,
4,,,,,
,,,,,
Source Labware,Source Slot,Source Well,Dest Labware,Dest Slot,Dest Well
eppendorf_24_tuberack_generic_2.0ml_screwcap,1,C1,appliedbiosystems_384_wellplate_20ul,6,B1
eppendorf_24_tuberack_generic_2.0ml_screwcap,1,A1,appliedbiosystems_384_wellplate_20ul,6,A4
eppendorf_24_tuberack_generic_2.0ml_screwcap,1,A1,appliedbiosystems_384_wellplate_20ul,6,D2
```
* `Assembly CSV File`: Upload the CSV file for assembly/patient samples here. You can download an [example CSV file here](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5b8174/Assembly.csv) OR follow the format directly below.
```
Rack,Sr.Barcode, ,Dest.Barcode,Dest.List Name,
1,,,,,
2,,,,,
3,,,,,
4,,,,,
,,,,,
Source Labware,Source Slot,Source Well,Dest Labware,Dest Slot,Dest Well
appliedbiosystems_96_wellplate_200ul_on_eppendorf_cooling_block,2,C11,appliedbiosystems_384_wellplate_20ul,6,B1
appliedbiosystems_96_wellplate_200ul_on_eppendorf_cooling_block,2,E11,appliedbiosystems_384_wellplate_20ul,6,A4
appliedbiosystems_96_wellplate_200ul_on_eppendorf_cooling_block,2,E11,appliedbiosystems_384_wellplate_20ul,6,D2
appliedbiosystems_96_wellplate_200ul_on_eppendorf_cooling_block,2,E11,appliedbiosystems_384_wellplate_20ul,6,E2
```

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Labware
* [Opentrons 20 uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

### Pipettes
* [Opentrons P20 Single Channel GEN2 Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)

---

### Deck Setup
* If the deck layout of a particular protocol is more or less static, it is often helpful to attach a preview of the deck layout, most descriptively generated with Labware Creator. Example:
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5b8174/5b8174_layout.png)

---

### Protocol Steps
1. Using information from Control CSV file, transfer 1.5uL of positive control from the (Source Labware, Source Slot, Source Well) to the (Dest Labware, Dest Slot, Dest Well), as indicated in the CSV. Change tip between each transfer.
2. Using information from Assembly CSV file, transfer 1.5uL of patient DNA from the (Source Labware, Source Slot, Source Well) to the (Dest Labware, Dest Slot, Dest Well), as indicated in the CSV. Change tip between each transfer.


### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5b8174
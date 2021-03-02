# swiftbiosci.com accel-amplicon-plus-egfr-pathway-panel

## Categories
* NGS Library Prep
	* accel-amplicon-plus-egfr-pathway-panel


## Description

With this protocol, your [OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2) can prepare up to 24 libraries [Swift accel-amplicon-plus-egfr-pathway-panel](https://swiftbiosci.com/accel-amplicon-plus-egfr-pathway-panel/).



---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase consumables, labware, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)


* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.15.0 or later)](https://opentrons.com/ot-app/)
* [Swift accel-amplicon-plus-egfr-pathway-panel](Swift accel-amplicon-plus-egfr-pathway-panel)
* [Opentrons Thermocycler Module](https://shop.opentrons.com/collections/hardware-modules/products/thermocycler-module)
* [Opentrons Temperature Module with Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons P20 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette) or Opentrons P50 Single-Channel Pipette*
* [Opentrons P300 Single-Channel Pipette](https://shop.opentrons.com/products/single-channel-electronic-pipette)
* [Opentrons Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [NEST 96-Well PCR Plate](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt)
* [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/reservoirs/products/nest-12-well-reservoir-15-ml)
* DNA samples resuspended in 10 uL Low EDTA TE.

---




__Using the customizations fields, below set up your protocol.__
* **Number of Samples**: Specify the number of samples (choose from 1 up to 24) you'd like to run.
* **Hold PCR plate on ice until block reaches 98 degrees?**: Select yes if you would like to manually place the PCR plate on the cycler only after it reaches 98 degrees (as described in the Swift protocol), select no if you choose to leave the plate on the cycler while it pre-heats.



**Note**: The initial DNA samples are placed on the Thermocycler Module plate in column order using B2-G2, B3-G3, B4-B4, B5-G5 ordering. The PCR plate can be optionally removed from the deck and held on ice while the thermocycler block pre-heats to 98 degrees (per reagent manufacturer instructions). The OT-2 deck lights will go off to signal pauses occurring when reagents are needed on the OT-2 deck. The final 20µL elution will be transferred to Columns 9, 10 and 11 of the PCR plate on the Thermocycler unless otherwise specified in the parameters below.

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters (specify the number of initial DNA samples (1-24) and indicate if you want to manually place the PCR plate on the 98 degree pre-heated thermocycler).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app). Be sure to use OT App settings in advance of the protocol run to pre-cool the temperature and thermocycler modules to 4 degrees.
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".
7. Deck lights will momentarily go off to indicate a pause when reagents should be added to the OT-2 deck:
   a.  Multiplex Mastermix and PCR plate containing the initial DNA samples (both at 4 degrees).
   b.  Optional: PCR plate held on ice while thermocycler block pre-heats to 98 degrees.
   c.  Beads and 80% ethanol (both at room temp).
   d.  Index plate and cold indexing reaction mix (4 degrees).
   e.  PEG NaCl and post PCR TE (both at room temp).

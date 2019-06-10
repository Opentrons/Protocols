# Bead Purification 1 & 2

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
This protocol performs an identical Bead Purification assay consecutively in the same run. The protocol allows for the user to input the number of samples (up to 96) to process. For reagent setup, see 'Additional Notes' below.

---

You will need:
* P50 Sinlge-channel Pipette
* P300 Multi-channel Pipette
* [FrameStar® Break-A-Way PCR Plates, Low Profile](https://www.brookslifesciences.com/products/framestar-break-way-pcr-plate-low-profile)
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)
* [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 12-well Trough
* Opentrons 300 ul Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the number of samples you would like process (MAX = 96).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 15 uL SPRI beads are distributed to each sample, which is pre-loaded in a 96-well PCR plate on the Magnetic Module.
8. After an incubation of 5 minutes, the Magnetic Module will engage for 5 minutes to allow the beads to settle.
9. While the Magnetic Module is being engaged, 34 uL of the supernatant (34 of 40 total) is discarded.
11. Samples are washed with 80% Ethanol twice, then allowed to air-dry for 5 minutes.
12. Samples are resuspended with 30 uL elution buffer.
13. After an incubation of 3 minutes, the Magnetic Module will engage for 1 minutes to allow the beads to settle.
14. 25 uL of the supernatant is transferred and mixed into a clean PCR plate in slot 1.
15. Robot pauses and allows user to perform PCR2 on a thermocycler. Once it is completed, user can resume the protocol and allow the samples to go through a second round of bead purification (repeats steps 7-14).


### Additional Notes
Trough 12-row Setup:
* A1: 80% Ethanol
* A2: 80% Ethanol
* A3: Elution Buffer for Bead Purification 1
* A4: Elution Buffer for Bead Purification 2

---

4x6 1.5-mL Eppendorf Tube Rack Setup:
* A1: SPRI Beads

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
W886Z34b
1580

# Ion AmpliSeq Library Prep 3/4: Ligate Adapters

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* NGS Library Prep
    * Ion AmpliSeq Library Prep

## Description
Links:
* [Part 1: DNA Target Amplification](./1557-part1)
* [Part 2: Partially Digest Amplicons](./1557-part2)
* [Part 3: Ligate Adapters](./1557-part3)
* [Part 4: Library Purification](./1557-part4)

---
You will need:
* [P10 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5978988707869)
* [Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Twin.tec skirted PCR Plates](https://www.fishersci.com/shop/products/eppendorf-96-well-twin-tec-pcr-plates-yellow-skirted-150-l/e951020427)
* Neptune 10 uL Filter Tips

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the number of samples you are processing. (MAX=24)
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. If number of samples is less than 3, robot will create PCR mix in the appropriate wells in the PCR plate. If greater than 3, robot will create a master mix in an Eppendorf tube before distributing its content to the PCR wells.
8. Robot will transfer Switch Solution from the 2 mL tube rack to PCR plate.
9. Robot will transfer IonCode Adapters from the PCR tube rack to PCR plate.
10. Robot will transfer DNA ligase from the 2 mL tube rack to PCR plate.


### Additional Notes
Twin.tec skirted PCR Plate (Reagent Plate in slot 1):
* Switch Solution: column 1
* DNA Ligase: column 2

---
 Aluminum 96-well PCR Block:
 * IonCode Adapters Plate

---

4-in-1 2-mL Tube Rack (Sample Rack):
* Sample order: A1, B1, C1, D1, A2, B2...

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
D2AAz1dg
1557

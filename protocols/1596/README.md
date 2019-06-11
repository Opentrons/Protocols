# PCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs PCR preparation on a custom MicroAmp 96-well PCR plate. **Ensure the reaction plate is mounted on the Opentrons 96-well aluminum block, which is in turn mounted on the Opentrons temperature module.** For reagent setup, see 'Additional Notes' below.

---

You will need:
* [Opentrons P50 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [Opentrons P50 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [TipOne 200ul Tips](https://www.usascientific.com/tiponefiltertips.aspx)
* [Axygen Boil-Proof 1.5ml microcentrifuge tubes, VWR # 10011-702](https://us.vwr.com/store/product/4674517/boil-proof-microcentrifuge-tubes-axygen-scientific)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons temperature module with aluminum block set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents
* 10mM dNTP mix, Fisher Scientific # PR-U1511
* RNAse H (120 U), Thermo # 18021-071
* SuperScript III Reverse Transcriptase, Thermo # 18080044
* RNAseOUT Recombinant Ribonuclease Inhibitor, Thermo # 10777019

## Process
1. Input the number of sample columns to be processed.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol waits for the tempdeck to cool to 4˚C before continuing.
8. The first master mix is created in volumes according to the number of samples that will be processed. The mix is mixed after all contents are transferred.
9. 5ul of master mix * the number of sample columns to be processed is transferred to each well in column 1 of the tempdeck plate.
10. 5ul of sample is distributed from column 1 of the tempdeck plate to all other columns to be processed.
11. The protocol pauses and prompts the user to place the deepwell plate containing RNA samples in slot 2 before resuming.
12. 25ul of RNA is transferred from the deepwell plate to the corresponding well of the tempdeck plate. A new tip is used for each transfer, and the contents of the destination well are mixed after each transfer.
13. The protocol pauses and prompts the user to replace the master mix tube with a fresh tube.
14. The second master mix is created in volumes according to the number of samples that will be processed. The mix is mixed after all contents are transferred.
15. The protocol pauses and promps the user to place the tempdeck plate back on the tempdeck before resuming.
16. 20ul of the new master mix is transferred to each sample well on the tempdeck plate being processed.

### Additional Notes
Reagent setup in Opentrons 4x6 aluminum block for 1.5ml Eppendorf tubes:
* primer 1: tube A1
* primer 2: tube B1
* dNTP: tube C1
* H2O: tube D1
* 5x buffer: tube A2
* DTT: tube B2
* RNAseOut: tube C2
* SuperScript III: tube D2
* Master Mix: tube A3 (loaded empty)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
EBfh59dT  
1596

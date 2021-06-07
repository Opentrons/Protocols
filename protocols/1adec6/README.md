# Small Molecule Library Prep

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* Assay

## Description
This protocol is the first protocol of several that are involved in this protein quantification protocol.

This protocol begins by adding 44µL of DMSO columns 6-10 of a 96-well plate (neglecting rows F-H in column 10).

After the addition of DMSO to columns 6-10, 33µL of sample is transferred between columns on the plate.

At this point, the user is prompted to manually add reagents before the protocol resumes and completes.

Finally, the OT-2 will transfer user specified aliquots to destination plates.

**Update (06/07/2021)**: This protocol has been updated and will no longer transfer the aliquots at the end from columns 11 and 12.

Explanation of complex parameters below:
* **P300-Multi Mount**: Select which mount the P300-Multi Pipette is attached to.
* **Number of Destination Plates**: Select the number of destination plates.
* **DMSO Volume (µL)**: Specify the volume of DMSO that will be transferred in the first step.
* **Aliquot Volume (µL)**: Specify the volume of the aliquots that will be transferred from the source plate to the destination plate(s).

---

### Labware
* [Opentrons 300µL Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)
* SPL 96-Well Cell Culture Plates

### Pipettes
* [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)

### Reagents
* DMSO (Column 1 of 12-Well Reservoir)

---

### Deck Setup
**Slot 1**: Sample Plate (SPL 96-Well Cell Culture Plates)</br>
</br>
**Slot 2**: Aliquot Destination Plate 1 (SPL 96-Well Cell Culture Plates)</br>
</br>
**Slot 3**: Aliquot Destination Plate 2 (SPL 96-Well Cell Culture Plates)</br>
</br>
**Slot 7**: [Opentrons 300µL Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)</br>
</br>
**Slot 8**: [Opentrons 300µL Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)</br>
</br>
**Slot 9**: [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)</br>
</br>

### Reagent Setup
1. Load DMSO in `Column 1` of the [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)

---

### Protocol Steps
1. The [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) will pick up the first column of [Opentrons 300µL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips) in Slot 7.
2. The [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) will transfer user-defined amount of DMSO (from `Column 1` of [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)) to columns 6-9 of the Sample Plate.
3.  The [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) will return the tips and pick up 5 tips from column 1.
4. The [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) will transfer user-defined amount of DMSO (from `Column 1` of [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)) to column 10, skipping rows F-H.
5. The [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) will return the tips to column 1.
6. For `Columns 1-4` of the Sample Plate, the [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) will pick up a column of tips, transfer 33µL of sample from the corresponding column to the column 5 columns over (ex. Column 1 --> Column 6), then return the tips.
7. The above step will be replicated again, but only three tips will be picked up so the sample transfer only occurs between rows A-C as samples are transferred from `Column 5` to `Column 10`.
8. The protocol will pause and the user will be prompted to manually add reagents. When ready, the user will click RESUME and the protocol will complete.
9. For each column of the Sample Plate, the [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) will pick up tips, transfer the specified aliquot volume from the column to the corresponding column in the destination plate(s), then return the tips.
10. End of the protocol.

### Process
1. Input your protocol parameters above.
2. Download your protocol bundle.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions), if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
1adec6

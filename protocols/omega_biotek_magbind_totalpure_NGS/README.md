# Nucleic Acid Purification with Omega Bio-tek Mag-Bind® TotalPure NGS

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
With this protocol, you can perform high-quality nucleic acid purifications using [Omega Bio-tek Mag-Bind® TotalPure NGS](https://shop.opentrons.com/products/mag-bind-total-pure-ngs?_ga=2.87650270.758603424.1545063195-403439593.1535387376&_gac=1.3933956.1543039580.EAIaIQobChMI0bPCrK7s3gIVhx6BCh0oPA25EAEYASAAEgJxEfD_BwE) magnetic beads and the [Opentrons Magnetic Module](https://shop.opentrons.com/products/magdeck?_ga=2.120183432.1039841802.1542049668-403439593.1535387376). This setup yields high quality PCR product and other nucleic acids without the use of centrifugation or vacuum separation.

This kit is widely used in NGS cleanup for its affordability and simplicity. It is also well-adapted for nucleic acid size selection by varying bead ratios for  the  isolation  of  a  wide  array  of  fragment  sizes. For more detailed information on how to use this protocol, please see our [Technical Note]().

---

---


![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/Nucleic+Acid+Purification/Setup.png)

Using the customization fields below, set up your protocol as follows:

   * **Pipette:** Specify your pipette. We recommend using a p50 or p300 multi- or single-channel.
   * **Pipette Mount:** Specify which mount (left or right) your pipette is on.
   * **Sample number:** Customize the number of samples to run per protocol. A multiple of 8 is recommended when you are using a multichannel pipette.
   * **Sample volume:** Specify the starting volume (in uL) of the input sample.
   * **Bead Ratio:** Customize the ratio of beads for left or right side size-selection of fragments. *The default bead ratio is 1.8x the input sample volume.*
   * **Elution Volume:** Specify the final volume (in uL) to elute the purified nucleic acid. *The Opentrons MagDeck supports elution volumes above 10 µL.*

---

---


![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/customizable-serial-dilution/materials.png)

-- [Omega Bio-tek Mag-Bind® TotalPure NGS Kit](https://shop.opentrons.com/products/mag-bind-total-pure-ngs?_ga=2.87650270.758603424.1545063195-403439593.1535387376&_gac=1.3933956.1543039580.EAIaIQobChMI0bPCrK7s3gIVhx6BCh0oPA25EAEYASAAEgJxEfD_BwE)

-- [Opentrons OT-2](http://opentrons.com/ot-2)

-- [Opentrons Magnetic Module](https://shop.opentrons.com/products/magdeck?_ga=2.171718441.823190023.1542396855-403439593.1535387376)

-- [Opentrons OT-2 Run App (Version 3.1.2 or later)](http://opentrons.com/ot-app)

-- 200uL or 300 uL Tiprack ([Opentrons tips suggested](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips-racks-9-600-tips))

-- [12-row automation-friendly trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

-- [BioRad HardShell 96-Well PCR Plates](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)

-- Ethanol 

-- Elution Buffer (Typically  10 mM Tris pH 8.0, TE Buffer, or nuclease-free water)

---

---

### Time Estimate
* Varies.

## Process
1. Select all desired settings according to the "Setup" section above to create your cusotmized protocol.
2. Download your customized OT-2 protocol using the blue "Download" button.
3. Upload your protocol file into the Opentrons Run App and follow the instructions there to set up your deck and proceed to run!
4. Make sure to add reagents to your labware before placing it on the deck! You can see where to place your reagents below.

![Labware setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/Nucleic+Acid+Purification/Nucleic+Acid+Purification+with+Magnetic+Beads+-+Reagent+Starting+Position+Image+(2).png)

###### Internal
Nucleic Acid Purification, v1

### Additional Notes
Please reference our [Technical Note]() for more information about the expected output of this protocol, in addition to expanded sample data from the Opentrons and Omega Bio-tek labs. 

We understand that there are limitations to the use of this protocol and we plan to make improvements soon! In the meantime, if you'd like to request a more complex purification workflow, please use our [Protocol Development Request Form](https://opentrons-protocol-dev.paperform.co/). You can also download the Python file from this page and modify it using our [API Documentation](https://docs.opentrons.com/). For additional questions about this protocol, please email protocols@opentrons.com.

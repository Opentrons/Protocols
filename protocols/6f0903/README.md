# MethylPatch Protocol for Opentrons OT-2

### Author
[Opentrons](https://opentrons.com/)

### Partner
[University of Utah Huntsman Cancer Institute](https://healthcare.utah.edu/huntsmancancerinstitute/)

## Categories
* NGS Prep
	*  MethylPatch Protocol

## Description
This is an NGS prep protocol...
TODO: Fill out this section

Explanation of parameters below:
* `p20 mount`: Choose whether the P20 single channel pipette should be mounted in the right or left pipette mount. The P300 8-channel pipette will then automatically be assigned to the other mount.

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Thermocycler Module](https://shop.opentrons.com/collections/hardware-modules/products/thermocycler-module)

### Labware
* [Nest 96 well plate 100 µL flat](https://labware.opentrons.com/nest_96_wellplate_200ul_flat?category=wellPlate)
* [NEST 12-Well Reservoirs, 15 mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)

### Pipettes
* [P20 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P300 multi-Channel (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)

---

### Deck Setup
* If the deck layout of a particular protocol is more or less static, it is often helpful to attach a preview of the deck layout, most descriptively generated with Labware Creator. Example:
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

### Reagent Setup
* This section can contain finer detail and images describing reagent volumes and positioning in their respective labware. Examples:
* Reservoir 1: slot 5
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res1_v2.png)
* Reservoir 2: slot 2  
![reservoir 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res2.png)

---

### Protocol Steps
Step 1: Restriction enzyme digestion of DNA (uses 8 P20 tips)

1. Use P20 to mix Temperature Tube 1 (Digest Master Mix).
2. Transfer 10 uL of Temperature Tube 1 to Thermocycler Tube 1A.
3. Mix Thermocycler Tube 1A.
4. Discard Tip.
5. Repeat steps 1.1 -1.4 for transfers from Temperature Tube 1 to Thermocycler Tubes 1B,1C,1D,1E,1F,1G, 1H.
6. Close lid.
7. Incubate at 37C for 60 minutes.
8. Incubate at 4C for 3 minutes.
9. Open lid.

Step 2: Patch ligation (uses 8 P20 tips)

10. Use P20 to mix Temperature Tube 2 (Patch Master Mix).
11. Transfer 15 uL of Temperature Tube 2 to Thermocycler Tube 1A.
12. Mix Thermocycler Tube 1A.
13. Discard Tip.
14. Repeat steps 2.1 -2.4 for transfers from Temperature Tube 2 to Thermocycler Tubes 1B,1C,1D,1E,1F,1G, 1H.
15. Close lid.
16. Cycle temperature: 94C for 30 seconds and 65 degrees for 4 minutes for 25 cycles.
17. Incubate at 4C for 3 minutes.
18. Open lid.

Step 3: Exonuclease degradation (uses 8 P20 tips)

19. Use P20 to mix Temperature Tube 3 (Exo Master Mix).
20.	Transfer 2 uL of Temperature Tube 3 to Thermocycler Tube 1A.
21.	Mix Thermocycler Tube 1A.
22.	Discard Tip.
23.	Repeat steps 3.1 -3.4 for transfers from Temperature Tube 3 to Thermocycler Tubes 1B,1C,1D,1E,1F,1G, 1H.
24.	Close lid.
25. Incubate at 37C for 60 minutes.
26.	Incubate at 4C for 3 minutes.
27.	Open lid.

Step 4: AMPure cleanup \#1 (uses 32 P300 tips)

28.	Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High Viscosity).
29.	Transfer 74 uL of Reservoir Well 1 to Magnet Wells Column 1 A-H.
30.	Transfer 37 uL of Thermocycler Column 1 A-H to Magnet Wells Column 1 A-H.
31.	Mix Magnet Wells Column 1 A-H at 1 minute intervals for 10 minutes.
32. Engage magnet.
33. Hold for 5 minutes (magnet still engaged).
34.	Remove 111 uL from Magnet Wells Column 1 A-H.
35. Discard tips.
36.	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
37.	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 1 A-H.
38. Slowly mix Magnet Wells Column 1 A-H 10 times. (Magnet still engaged, washing bead pellet).
39. Remove 200 uL from Magnet Wells Column 1 A-H.
40. Discard tips.
41.	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
42. Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 1 A-H.
43. Slowly mix Magnet Wells Column 1 A-H 10 times. (Magnet still engaged, washing bead pellet).
44. Remove 200 uL from Magnet Wells Column 1 A-H.
45. Discard tips.
46. Hold for 10 minutes (magnet still engaged) to let residual ethanol evaporate.
47.	Close thermocycler lid.
48. Heat thermocycler to 37C for 2 minutes.
49. Open thermocycler lid.
50. Disengage magnet.
51. Use 8-channel P300 to transfer 30 uL of water from Thermocycler Column 9 Rows A-H to Magnet Wells Column 1 A-H. Dispense liquid over the side of the tube with the magnetic contact.
52. Mix Magnet Wells Column 1 A-H at 1 minute intervals for 10 minutes (eluting DNA from beads).
53. Engage magnet.
54. Hold for 3 minutes (magnet still engaged).
55. Transfer 28uL from Magnet Wells Column 1 A-H to Thermocycler Column 3 Rows A-H.
56. Discard tips.
57. Disengage magnet.

Step 5: TET2 Oxidation (uses 24 P20 tips)

58.	Use P20 to mix Temperature Tube 4 (TET2 Master Mix).
59. Transfer 17 uL of Temperature Tube 4 to Thermocycler Tube 3A.
60. Mix Thermocycler Tube 3A.
61. Discard Tip.
62. Repeat steps 5.1 -5.4 for transfers from Temperature Tube 4 to Thermocycler Tubes 3B,3C,3D,3E,3F,3G, 3H.
63.	Use P20 to mix Temperature Tube 5 (Fe solution).
64. Transfer 5 uL of Temperature Tube 5 to Thermocycler Tube 3A.
65. Mix Thermocycler Tube 3A.
66. Discard Tip.
67. Repeat steps 5.6 -5.9 for transfers from Temperature Tube 5 to Thermocycler Tubes 3B,3C,3D,3E,3F,3G, 3H.
68. Close lid.
69. Incubate at 37C for 60 minutes.
70. Incubate at 25C for 3 minutes.
71. Open lid.
72. Use P20 to mix Temperature Tube 6 (Stop Reagent).
73. Transfer 1 uL of Temperature Tube 6 to Thermocycler Tube 3A.
74. Mix Thermocycler Tube 3A.
75. Discard Tip.
76. Repeat steps 5.15 -5.18 for transfers from Temperature Tube 6 to Thermocycler Tubes 3B,3C,3D,3E,3F,3G, 3H.
77. Close lid.
78. Incubate at 37C for 30 minutes.
79. Incubate at 4C for 3 minutes.
80. Open lid.

Step 6: AMPure cleanup \#2 (uses 32 P300 tips)

1	Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High Viscosity).
2 	Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 3 A-H.
3 	Transfer 51 uL of Thermocycler Column 3 A-H to Magnet Wells Column 3 A-H.
4 	Mix Magnet Wells Column 3 A-H at 1 minute intervals for 10 minutes.
5	Engage magnet.
6	Hold for 5 minutes (magnet still engaged).
7 	Remove 151 uL from Magnet Wells Column 3 A-H.
8	Discard tips.
9 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
10 	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 3 A-H.
11	Slowly mix Magnet Wells Column 3 A-H 10 times. (Magnet still engaged, washing bead pellet).
12	Remove 200 uL from Magnet Wells Column 3 A-H.
13	Discard tips.
14 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
15	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 3 A-H.
16	Slowly mix Magnet Wells Column 3 A-H 10 times. (Magnet still engaged, washing bead pellet).
17	Remove 200 uL from Magnet Wells Column 3 A-H.
18	Discard tips.
19	Hold for 10 minutes (magnet still engaged) to let residual ethanol evaporate.
20 	Close thermocycler lid.
21	Heat thermocycler to 37C for 2 minutes.
22	Open thermocycler lid.
23	Disengage magnet.
24	Use 8-channel P300 to transfer 17 uL of water from Thermocycler Column 10 Rows A-H to Magnet Wells Column 3 A-H. Dispense liquid over the side of the tube with the magnetic contact.
25	Mix Magnet Wells Column 3 A-H at 1 minute intervals for 10 minutes (eluting DNA from beads).
26	Engage magnet.
27	Hold for 3 minutes (magnet still engaged).
28	Transfer 16uL from Magnet Wells Column 3 A-H to Thermocycler Column 5 Rows A-H.
29	Discard tips.
30	Disengage magnet.

Step 7: APOBEC Deamination (uses 24 P20 tips)

7.1	Close thermocycler.
7.2 	Incubate thermocycler at 50C for 3 minutes.
7.3	Use P20 to mix Temperature Tube 7 (NaOH).
7.4	Open thermocycler.
7.5 	Transfer 4 uL of Temperature Tube 7 to Thermocycler Tube 5A.
7.6 	Mix Thermocycler Tube 5A.
7.7 	Discard Tip.
7.8 	Repeat steps 7.5 -7.7 for transfers from Temperature Tube 7 to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
7.9	Close thermocycler.
7.10	Incubate at 50C for 10 minutes.
7.11	Incubate at 4C for 5 minutes.
7.12	Open thermocycler.
7.13 	Use P20 to transfer 10 uL of Temperature Tube 8 (water) to Thermocycler Tube 5A.
7.14 	Mix Thermocycler Tube 5A.
7.15	Discard Tip.
7.16 	Repeat steps 7.13 -7.15 for transfers from Temperature Tube 8 to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
7.17 	Use P20 to mix Temperature Tube 9 (APOBEC Master Mix).
7.18	Use P20 to transfer 20 uL of Temperature Tube 9 to Thermocycler Tube 5A.
7.19 	Mix Thermocycler Tube 5A.
7.20	Discard Tip.
7.21 	Repeat steps 7.17 -7.20 for transfers from Temperature Tube 9 to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
7.22 	Close lid.
7.23	Incubate at 37C for 3 hours.
7.24	Incubate at 4C for 3 minutes.
7.25	Open lid.


Step 8: AMPure cleanup #3 (uses 32 P300 tips)

8.1	Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High Viscosity).
8.2 	Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 5 A-H.
8.3 	Transfer 50 uL of Thermocycler Column 5 A-H to Magnet Wells Column 5 A-H.
8.4 	Mix Magnet Wells Column 5 A-H at 1 minute intervals for 10 minutes.
8.5	Engage magnet.
8.6	Hold for 5 minutes (magnet still engaged).
8.7 	Remove 150 uL from Magnet Wells Column 5 A-H.
8.8	Discard tips.
8.9 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
8.10 	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 5 A-H.
8.11	Slowly mix Magnet Wells Column 5 A-H 10 times. (Magnet still engaged, washing bead pellet).
8.12	Remove 200 uL from Magnet Wells Column 5 A-H.
8.13	Discard tips.
8.14 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
8.15	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 5 A-H.
8.16	Slowly mix Magnet Wells Column 5 A-H 10 times. (Magnet still engaged, washing bead pellet).
8.17	Remove 200 uL from Magnet Wells Column 5 A-H.
8.18	Discard tips.
8.19	Hold for 10 minutes (magnet still engaged) to let residual ethanol evaporate.
8.20 	Close thermocycler lid.
8.21	Heat thermocycler to 37C for 2 minutes.
8.22	Open thermocycler lid.
8.23	Disengage magnet.
8.24	Use 8-channel P300 to transfer 30 uL of water from Thermocycler Column 11 Rows A-H to Magnet Wells Column 5 A-H. Dispense liquid over the side of the tube with the magnetic contact.
8.25	Mix Magnet Wells Column 5 A-H at 1 minute intervals for 10 minutes (eluting DNA from beads).
8.26	Engage magnet.
8.27	Hold for 3 minutes (magnet still engaged).
8.28	Transfer 29 uL from Magnet Wells Column 5 A-H to Thermocycler Column 7 Rows A-H.
8.29	Discard tips.
8.30	Disengage magnet.

Step 9: PCR Master Mix Prep (uses 16 P20 tips)

9.1 	Use P20 to mix Temperature Tube 10 (PCR Master Mix).
9.2 	Transfer 20 uL of Temperature Tube 10 to Thermocycler Tube 7A.
9.3 	Mix Thermocycler Tube 7A.
9.4 	Discard Tip.
9.5 	Repeat steps 9.1 -9.4 for transfers from Temperature Tube 10 to Thermocycler Tubes 7B,7C,7D,7E,7F,7G, 7H.
9.6 	Use P20 to mix Temperature Tube 11 (Barcode Primer 1).
9.7	Transfer 1 uL of Temperature Tube 11 to Thermocycler Tube 7A.
9.8 	Mix Thermocycler Tube 7A.
9.9	Discard Tip.
9.10 	Use P20 to mix Temperature Tube 12 (Barcode Primer 2).
9.11	Transfer 1 uL of Temperature Tube 12 to Thermocycler Tube 7B.
9.12 	Mix Thermocycler Tube 7B.
9.13	Discard Tip.
9.14 	Use P20 to mix Temperature Tube 13 (Barcode Primer 3).
9.15	Transfer 1 uL of Temperature Tube 13 to Thermocycler Tube 7C.
9.16 	Mix Thermocycler Tube 7C.
9.17	Discard Tip.
9.18 	Use P20 to mix Temperature Tube 14 (Barcode Primer 4).
9.19	Transfer 1 uL of Temperature Tube 14 to Thermocycler Tube 7D.
9.20 	Mix Thermocycler Tube 7D.
9.21 	Use P20 to mix Temperature Tube 15 (Barcode Primer 5).
9.22	Transfer 1 uL of Temperature Tube 15 to Thermocycler Tube 7E.
9.23 	Mix Thermocycler Tube 7E.
9.24	Discard Tip.
9.25 	Use P20 to mix Temperature Tube 16 (Barcode Primer 6).
9.26	Transfer 1 uL of Temperature Tube 16 to Thermocycler Tube 7F.
9.27 	Mix Thermocycler Tube 7F.
9.28 	Use P20 to mix Temperature Tube 17 (Barcode Primer 7).
9.29	Transfer 1 uL of Temperature Tube 17 to Thermocycler Tube 7G.
9.30 	Mix Thermocycler Tube 7G.
9.31	Discard Tip.
9.32 	Use P20 to mix Temperature Tube 18 (Barcode Primer 8).
9.33	Transfer 1 uL of Temperature Tube 18 to Thermocycler Tube 7H.
9.34 	Mix Thermocycler Tube 7H.
9.35	Discard Tip.
9.36 	Close lid.
9.37	Incubate at 95C for 30 sec.
9.38	Cycle temperature: 94C for 30 seconds and 60 degrees for 3 minutes for 25 cycles.
9.39 	Incubate at 4C for 3 minutes.
9.40 	Open lid.


Step 10: AMPure cleanup #4 (uses 32 P300 tips)

10.1	Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High Viscosity).
10.2 	Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 7 A-H.
10.3 	Transfer 50 uL of Thermocycler Column 7 A-H to Magnet Wells Column 7 A-H.
10.4 	Mix Magnet Wells Column 7 A-H at 1 minute intervals for 10 minutes.
10.5	Engage magnet.
10.6	Hold for 5 minutes (magnet still engaged).
10.7 	Remove 150 uL from Magnet Wells Column 7 A-H.
10.8	Discard tips.
10.9 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
10.10 	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 7 A-H.
10.11	Slowly mix Magnet Wells Column 7 A-H 10 times. (Magnet still engaged, washing bead pellet).
10.12	Remove 200 uL from Magnet Wells Column 7 A-H.
10.13	Discard tips.
10.14 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
10.15	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 7 A-H.
10.16	Slowly mix Magnet Wells Column 7 A-H 10 times. (Magnet still engaged, washing bead pellet).
10.17	Remove 200 uL from Magnet Wells Column 7 A-H.
10.18	Discard tips.
10.19	Hold for 10 minutes (magnet still engaged) to let residual ethanol evaporate.
10.20 	Close thermocycler lid.
10.21	Heat thermocycler to 37C for 2 minutes.
10.22	Open thermocycler lid.
10.23	Disengage magnet.
10.24	Use 8-channel P300 to transfer 42 uL of water from Thermocycler Column 12 Rows A-H to Magnet Wells Column 7 A-H. Dispense liquid over the side of the tube with the magnetic contact.
10.25	Mix Magnet Wells Column 7 A-H at 1 minute intervals for 10 minutes (eluting DNA from beads).
10.26	Engage magnet.
10.27	Hold for 3 minutes (magnet still engaged).
10.28	Transfer 40 uL from Magnet Wells Column 7 A-H to Thermocycler Column 9 Rows A-H.
10.29	Discard tips.
10.30	Disengage magnet.
10.31	Close thermocycler lid.
10.32  Hold thermocycler at 4C.
10.33	Alert user that the protocol has finished.

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
6f0903

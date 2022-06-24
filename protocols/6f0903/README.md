# MethylPatch Protocol for Opentrons OT-2

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Varley Lab, University of Utah Huntsman Cancer Institute](https://uofuhealth.utah.edu/huntsman/labs/varley/)

## Categories
* NGS Library Prep
	*  MethylPatch Protocol

## Description
This is an NGS prep protocol...
TODO: Fill out this section

Explanation of parameters below:
* `p20 mount`: Choose whether the P20 single channel pipette should be mounted in the right or left pipette mount. The P300 8-channel pipette will then automatically be assigned to the other mount.
* `Barcode tubes initial volume (µL)`: The initial volume of the tubes containing barcodes, the volumes are presumed to be the same for all of the barcode tubes, and is used to determine the volume for mixing the barcodes prior to transferring them to the sample tubes.
* `Magnet engagement height (mm)`: The distance from the base of the plate to raise the magnets on the magnetic module when engaging the magnets.
* `Number of mixing repetitions`: How many mixing repetitions to perform for every mixing step.
* `Flash the OT-2 lights when the protocol finishes?`: If this parameter is set to `Yes` the OT-2 will flash its lights five times when the protocol finishes to alert the user.

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

81.	Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High Viscosity).
82. 	Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 3 A-H.
83. 	Transfer 51 uL of Thermocycler Column 3 A-H to Magnet Wells Column 3 A-H.
84. 	Mix Magnet Wells Column 3 A-H at 1 minute intervals for 10 minutes.
85.	Engage magnet.
86.	Hold for 5 minutes (magnet still engaged).
87. 	Remove 151 uL from Magnet Wells Column 3 A-H.
88.	Discard tips.
89. 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
90. 	Transfer 200 uL of Reservoir Well 5 to Magnet.. Wells Column 3 A-H.
91.	Slowly mix Magnet Wells Column 3 A-H 10 times. (Magnet still engaged, washing bead pellet).
92.	Remove 200 uL from Magnet Wells Column 3 A-H.
93.	Discard tips.
94. 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
95.	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 3 A-H.
96.	Slowly mix Magnet Wells Column 3 A-H 10 times. (Magnet still engaged, washing bead pellet).
97.	Remove 200 uL from Magnet Wells Column 3 A-H.
98.	Discard tips.
99.	Hold for 10 minutes (magnet still engaged) to let residual ethanol evaporate.
100. 	Close thermocycler lid.
101.	Heat thermocycler to 37C for 2 minutes.
102.	Open thermocycler lid.
103.	Disengage magnet.
104.	Use 8-channel P300 to transfer 17 uL of water from Thermocycler Column 10 Rows A-H to Magnet Wells Column 3 A-H. Dispense liquid over the side of the tube with the magnetic contact.
105.	Mix Magnet Wells Column 3 A-H at 1 minute intervals for 10 minutes (eluting DNA from beads).
106.	Engage magnet.
107.	Hold for 3 minutes (magnet still engaged).
108.	Transfer 16uL from Magnet Wells Column 3 A-H to Thermocycler Column 5 Rows A-H.
109.	Discard tips.
110.	Disengage magnet.

Step 7: APOBEC Deamination (uses 24 P20 tips)

111.	Close thermocycler.
122. 	Incubate thermocycler at 50C for 3 minutes.
123.	Use P20 to mix Temperature Tube 7 (NaOH).
124.	Open thermocycler.
125. 	Transfer 4 uL of Temperature Tube 7 to Thermocycler Tube 5A.
126. 	Mix Thermocycler Tube 5A.
127. 	Discard Tip.
128. 	Repeat steps 7.5 -7.7 for transfers from Temperature Tube 7 to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
129.	Close thermocycler.
130.	Incubate at 50C for 10 minutes.
131.	Incubate at 4C for 5 minutes.
132.	Open thermocycler.
133. 	Use P20 to transfer 10 uL of Temperature Tube 8 (water) to Thermocycler Tube 5A.
134. 	Mix Thermocycler Tube 5A.
135.	Discard Tip.
136. 	Repeat steps 7.13 -7.15 for transfers from Temperature Tube 8 to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
137. 	Use P20 to mix Temperature Tube 9 (APOBEC Master Mix).
138.	Use P20 to transfer 20 uL of Temperature Tube 9 to Thermocycler Tube 5A.
139. 	Mix Thermocycler Tube 5A.
140.	Discard Tip.
141. 	Repeat steps 7.17 -7.20 for transfers from Temperature Tube 9 to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
142. 	Close lid.
143.	Incubate at 37C for 3 hours.
144.	Incubate at 4C for 3 minutes.
145.	Open lid.

Step 8: AMPure cleanup \#3 (uses 32 P300 tips)

146.	Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High Viscosity).
147. 	Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 5 A-H.
148. 	Transfer 50 uL of Thermocycler Column 5 A-H to Magnet Wells Column 5 A-H.
149. 	Mix Magnet Wells Column 5 A-H at 1 minute intervals for 10 minutes.
150.	Engage magnet.
151.	Hold for 5 minutes (magnet still engaged).
152. 	Remove 150 uL from Magnet Wells Column 5 A-H.
153.	Discard tips.
154. 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
155. 	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 5 A-H.
156.	Slowly mix Magnet Wells Column 5 A-H 10 times. (Magnet still engaged, washing bead pellet).
157.	Remove 200 uL from Magnet Wells Column 5 A-H.
158.	Discard tips.
159. 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
160.	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 5 A-H.
161.	Slowly mix Magnet Wells Column 5 A-H 10 times. (Magnet still engaged, washing bead pellet).
162.	Remove 200 uL from Magnet Wells Column 5 A-H.
163.	Discard tips.
164.	Hold for 10 minutes (magnet still engaged) to let residual ethanol evaporate.
165. 	Close thermocycler lid.
166.	Heat thermocycler to 37C for 2 minutes.
167.	Open thermocycler lid.
168.	Disengage magnet.
169.	Use 8-channel P300 to transfer 30 uL of water from Thermocycler Column 11 Rows A-H to Magnet Wells Column 5 A-H. Dispense liquid over the side of the tube with the magnetic contact.
170.	Mix Magnet Wells Column 5 A-H at 1 minute intervals for 10 minutes (eluting DNA from beads).
171.	Engage magnet.
172.	Hold for 3 minutes (magnet still engaged).
173.	Transfer 29 uL from Magnet Wells Column 5 A-H to Thermocycler Column 7 Rows A-H.
174.	Discard tips.
175.	Disengage magnet.

Step 9: PCR Master Mix Prep (uses 16 P20 tips)

176. 	Use P20 to mix Temperature Tube 10 (PCR Master Mix).
177. 	Transfer 20 uL of Temperature Tube 10 to Thermocycler Tube 7A.
178. 	Mix Thermocycler Tube 7A.
179. 	Discard Tip.
180. 	Repeat steps 9.1 -9.4 for transfers from Temperature Tube 10 to Thermocycler Tubes 7B,7C,7D,7E,7F,7G, 7H.
181. 	Use P20 to mix Temperature Tube 11 (Barcode Primer 1).
182.	Transfer 1 uL of Temperature Tube 11 to Thermocycler Tube 7A.
183. 	Mix Thermocycler Tube 7A.
184.	Discard Tip.
185. 	Use P20 to mix Temperature Tube 12 (Barcode Primer 2).
186.	Transfer 1 uL of Temperature Tube 12 to Thermocycler Tube 7B.
187. 	Mix Thermocycler Tube 7B.
188.	Discard Tip.
189. 	Use P20 to mix Temperature Tube 13 (Barcode Primer 3).
190.	Transfer 1 uL of Temperature Tube 13 to Thermocycler Tube 7C.
191. 	Mix Thermocycler Tube 7C.
192.	Discard Tip.
193. 	Use P20 to mix Temperature Tube 14 (Barcode Primer 4).
194.	Transfer 1 uL of Temperature Tube 14 to Thermocycler Tube 7D.
195. 	Mix Thermocycler Tube 7D.
196. 	Use P20 to mix Temperature Tube 15 (Barcode Primer 5).
197.	Transfer 1 uL of Temperature Tube 15 to Thermocycler Tube 7E.
198. 	Mix Thermocycler Tube 7E.
199.	Discard Tip.
200. 	Use P20 to mix Temperature Tube 16 (Barcode Primer 6).
201.	Transfer 1 uL of Temperature Tube 16 to Thermocycler Tube 7F.
202. 	Mix Thermocycler Tube 7F.
203. 	Use P20 to mix Temperature Tube 17 (Barcode Primer 7).
204.	Transfer 1 uL of Temperature Tube 17 to Thermocycler Tube 7G.
205. 	Mix Thermocycler Tube 7G.
206.	Discard Tip.
207. 	Use P20 to mix Temperature Tube 18 (Barcode Primer 8).
208.	Transfer 1 uL of Temperature Tube 18 to Thermocycler Tube 7H.
209. 	Mix Thermocycler Tube 7H.
210.	Discard Tip.
211. 	Close lid.
212.	Incubate at 95C for 30 sec.
213.	Cycle temperature: 94C for 30 seconds and 60 degrees for 3 minutes for 25 cycles.
214. 	Incubate at 4C for 3 minutes.
215. 	Open lid.

Step 10: AMPure cleanup \#4 (uses 32 P300 tips)

216.	Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High Viscosity).
217. 	Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 7 A-H.
218. 	Transfer 50 uL of Thermocycler Column 7 A-H to Magnet Wells Column 7 A-H.
219. 	Mix Magnet Wells Column 7 A-H at 1 minute intervals for 10 minutes.
220.	Engage magnet.
221.	Hold for 5 minutes (magnet still engaged).
222. 	Remove 150 uL from Magnet Wells Column 7 A-H.
223.	Discard tips.
224. 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
225. 	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 7 A-H.
226.	Slowly mix Magnet Wells Column 7 A-H 10 times. (Magnet still engaged, washing bead pellet).
227.	Remove 200 uL from Magnet Wells Column 7 A-H.
228.	Discard tips.
229. 	Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
230.	Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 7 A-H.
231.	Slowly mix Magnet Wells Column 7 A-H 10 times. (Magnet still engaged, washing bead pellet).
232.	Remove 200 uL from Magnet Wells Column 7 A-H.
233.	Discard tips.
234.	Hold for 10 minutes (magnet still engaged) to let residual ethanol evaporate.
235. 	Close thermocycler lid.
236.	Heat thermocycler to 37C for 2 minutes.
237.	Open thermocycler lid.
238.	Disengage magnet.
239.	Use 8-channel P300 to transfer 42 uL of water from Thermocycler Column 12 Rows A-H to Magnet Wells Column 7 A-H. Dispense liquid over the side of the tube with the magnetic contact.
240.	Mix Magnet Wells Column 7 A-H at 1 minute intervals for 10 minutes (eluting DNA from beads).
241.	Engage magnet.
242.	Hold for 3 minutes (magnet still engaged).
243.	Transfer 40 uL from Magnet Wells Column 7 A-H to Thermocycler Column 9 Rows A-H.
244.	Discard tips.
245.	Disengage magnet.
246.	Close thermocycler lid.
247.  Hold thermocycler at 4C.
248.	Alert user that the protocol has finished.

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

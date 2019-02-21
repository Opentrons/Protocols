from opentrons import labware, instruments

metadata = {
    'protocolName': 'PCR/qPCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}

reservoir_name = 'E&K-undivided-deep-well-reservoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=85,
        depth=39.2)

# labware setup
dna_stock = labware.load('PCR-strip-tall', '1')
dna_dilution = labware.load('PCR-strip-tall', '2')
reagent = labware.load(reservoir_name, '5').wells('A1')
tipracks = [labware.load('tiprack-10ul', slot)
            for slot in ['3', '6']]

# instruments setup
p10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks)

# transfer DNA
for source, dest in zip(dna_stock.cols(), dna_dilution.cols()):
    p10.transfer(5, source, dest, blow_out=True)

# transfer reagent
for col in dna_dilution.cols():
    p10.pick_up_tip()
    p10.transfer(5, reagent, col, new_tip='never')
    p10.mix(3, 5, col)
    p10.blow_out(col[0].top())
    p10.drop_tip()

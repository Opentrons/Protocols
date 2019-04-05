from opentrons import labware, instruments
from otcustomizers import FileInput
import math

metadata = {
    'protocolName': 'ELISA: Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

deep_plate_name = 'usa-scientific-tuberack-1.2ml'
if deep_plate_name not in labware.list():
    labware.create(
        deep_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=44)


example_csv = """
50,500,5000
10,10000,100000
100,,
5,,
"""


def run_custom_protocol(
        starting_buffer_volume: float=50,
        number_of_standards: int=6,
        concentration_csv: FileInput=example_csv):

    # labware setup
    tuberack_1 = labware.load('opentrons-tuberack-15_50ml', '1')
    tuberack_4 = labware.load('opentrons-tuberack-2ml-eppendorf', '4')
    deep_plates = [labware.load(deep_plate_name, slot)
                   for slot in ['5', '6']]

    tiprack_1000 = labware.load('tiprack-1000ul', '2')
    tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['3', '7']]

    # instrument setup
    p1000 = instruments.P1000_Single(
        mount='left',
        tip_racks=[tiprack_1000])
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    tubes = [well for row in tuberack_4.rows() for well in row]
    samples = tubes[2 + number_of_standards:]
    dilution_buffer = tuberack_1.wells('A3')

    dil_dests = [row for deep_plate in deep_plates
                 for row in deep_plate.rows()]

    conc_lists = [[int(cell) for cell in line.split(',') if cell]
                  for line in concentration_csv.splitlines() if line]

    concs = [5, 10, 25, 50, 100, 500, 1000, 5000, 10000, 25000, 50000, 100000]
    diluent_vols = [320, 450, 180, 320, 450, 320, 450, 320, 450, 180, 320, 450]
    sample_vols = [80, 50, 120, 80, 50, 80, 50, 80, 50, 120, 80, 50]
    concs_init = [1, 1, 10, 10, 10, 100, 100, 1000, 1000, 10000, 10000, 10000]
    dil_formulae = {
        conc: {'diluent_vol': diluent_vol,
               'sample_vol': sample_vol,
               'conc_init': conc_init,
               'col_index': index}
        for conc, diluent_vol, sample_vol, conc_init, index in zip(
            concs, diluent_vols, sample_vols, concs_init, range(12))
        }

    buffer_height = 20 + \
        (50 - starting_buffer_volume) * 1000 / (math.pi * (13.5 ** 2))

    dilution_concs = []
    for sample_index, concentrations in enumerate(conc_lists):
        new_concs = []
        factors = [10, 100, 1000, 10000, 100000]
        conc_inspect = max(concentrations)

        for factor_index, factor in enumerate(factors):
            if (conc_inspect // factor) > 0 and (conc_inspect // factor) < 10:
                [new_concs.append(factors[:factor_index+1])]
                [concentrations.pop(concentrations.index(num))
                 for num in factors[:factor_index+1] if num in concentrations]
                [new_concs.append([conc_inspect])
                 if conc_inspect not in new_concs[0] else '']
                [concentrations.pop(concentrations.index(conc_inspect))
                 if conc_inspect in concentrations else '']
        [new_concs.append([conc]) for conc in concentrations if concentrations]
        dilution_concs.append(new_concs)

    # transfer dilution buffer
    p1000.pick_up_tip()
    for sample_index, (row, concs) in enumerate(
            zip(dil_dests, dilution_concs)):
        volumes = [dil_formulae[conc]['diluent_vol']
                   for c_list in concs for conc in c_list]
        dests = [row.wells(dil_formulae[conc]['col_index'])
                 for c_list in concs for conc in c_list]
        for volume, dest in zip(volumes, dests):
            buffer_height += volume / (math.pi * (13.5 ** 2))
            if buffer_height > 75:
                source = dilution_buffer.bottom(3)
            else:
                source = dilution_buffer.top(-buffer_height)
            p1000.transfer(
                volume,
                source,
                dest.top(-10),
                new_tip='never')
            p1000.blow_out(dest.top())
    p1000.drop_tip()

    # transfer samples
    for sample_index, (row, concs) in enumerate(
            zip(dil_dests, dilution_concs)):
        for c_list in concs:
            volumes = [dil_formulae[conc]['sample_vol'] for conc in c_list]
            sources = []
            for conc in c_list:
                if dil_formulae[conc]['conc_init'] == 1:
                    sources.append(samples[sample_index])
                else:
                    source_conc = dil_formulae[conc]['conc_init']
                    sources.append(
                        row.wells(dil_formulae[source_conc]['col_index']))
            dests = [row.wells(dil_formulae[conc]['col_index'])
                     for conc in c_list]
            p300.pick_up_tip()
            for volume, source, dest in zip(volumes, sources, dests):
                p300.transfer(volume, source, dest, new_tip='never')
                p300.mix(3, 200, dest)
            p300.drop_tip()

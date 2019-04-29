from opentrons import labware, instruments
from otcustomizers import FileInput
import math

metadata = {
    'protocolName': 'ELISA',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


example_csv = """
250,2.5,5
10,25,50
100,5,
5,250,
"""

deep_plate_name = "plateone-96-deep-well-plate-2ml"
if deep_plate_name not in labware.list():
    labware.create(
        deep_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=41.3,
        volume=2000)


def run_custom_protocol(
        starting_buffer_volume: float=50,
        number_of_standards: int=6,
        concentration_csv: FileInput=example_csv):

    # labware setup
    tuberack_15_50ml = labware.load('opentrons-tuberack-15_50ml', '1')
    tiprack_1000 = labware.load('tiprack-1000ul', '2')
    tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['3', '7', '10']]
    tuberack_2ml = labware.load('opentrons-tuberack-2ml-eppendorf', '4')
    deep_plate = labware.load(deep_plate_name, '5')
    stp_plate = labware.load('96-well-plate-20mm', '6')

    # instruments setup
    p1000 = instruments.P1000_Single(
        mount='left',
        tip_racks=[tiprack_1000])
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    tuberack_wells = [well for row in tuberack_2ml.rows() for well in row]
    blank = tuberack_wells[0]
    control = tuberack_wells[1]
    standards = tuberack_wells[2:2 + number_of_standards]
    samples = tuberack_wells[2 + number_of_standards:]
    dilution_buffer = tuberack_15_50ml.wells('A3')

    conc_lists = [[float(cell) for cell in line.split(',') if cell]
                  for line in concentration_csv.splitlines() if line]

    dil_dests = deep_plate.cols()

    concs = [1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 100.0, 250.0]
    diluent_vols = [0, 180, 320, 450, 180, 320, 450, 180]
    sample_vols = [500, 120, 80, 50, 120, 80, 50, 120]
    concs_init = [1, 1, 1, 1, 10, 10, 10, 100]
    dil_formulae = {
        conc: {'diluent_vol': diluent_vol,
               'sample_vol': sample_vol,
               'conc_init': conc_init,
               'col_index': index}
        for conc, diluent_vol, sample_vol, conc_init, index in zip(
            concs, diluent_vols, sample_vols, concs_init, range(8))
        }

    buffer_height = 20 + \
        (50 - starting_buffer_volume) * 1000 / (math.pi * (13.5 ** 2))

    dilution_concs = []
    for sample_index, concentrations in enumerate(conc_lists):
        new_concs = []
        factors = [1.0, 10.0, 100.0]
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

    """Sample Serial Dilution
    """

    # transfer dilution buffer
    p1000.pick_up_tip()
    for sample_index, (row, concs) in enumerate(
            zip(dil_dests, dilution_concs)):
        volumes = [dil_formulae[conc]['diluent_vol']
                   for c_list in concs for conc in c_list]
        dests = [row.wells(dil_formulae[conc]['col_index'])
                 for c_list in concs for conc in c_list]
        for volume, dest in zip(volumes, dests):
            if volume:
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
                if not dest.get_name()[0] == 'A':
                    p300.mix(3, 200, dest)
            p300.drop_tip()

    """Transfer Samples
    """

    conc_lists = [[float(cell) for cell in line.split(',') if cell]
                  for line in concentration_csv.splitlines() if line]
    concs = [1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 100.0, 250.0]
    samples = [
        row.wells(concs.index(conc))
        for concentrations, row in zip(conc_lists, dil_dests)
        for conc in concentrations
        ]

    dests = [
        [stp_plate.rows(index)[num], stp_plate.rows(index+1)[num]]
        for num in range(12) for index in range(0, 8, 2)
        ]

    # transfer blank
    p300.distribute(100, blank, dests[-5])
    dests.pop(-5)

    # transfer control
    p300.distribute(100, control, dests[-1])
    dests.pop(-1)

    # transfer standards
    for standard in standards:
        p300.distribute(100, standard, dests[0])
        dests.pop(0)

    # transfer samples
    for sample in samples:
        p300.pick_up_tip()
        p300.aspirate(200, sample)
        for dest in dests[0]:
            p300.dispense(100, dest)
        p300.drop_tip()
        dests.pop(0)

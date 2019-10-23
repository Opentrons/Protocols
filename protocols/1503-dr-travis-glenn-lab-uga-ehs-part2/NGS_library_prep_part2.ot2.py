from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        number_of_columns: int=12,
        p10_tiprack_type: StringSelection(
            'opentrons_96_tiprack_10ul',
            'fisherbrand-filter-tiprack-10ul',
            'phenix-filter-tiprack-10ul')='opentrons_96_tiprack_10ul'):

    if p10_tiprack_type not in labware.list():
        labware.create(
            p10_tiprack_type,
            grid=(12, 8),
            spacing=(9, 9),
            diameter=5,
            depth=60)

    # labware setup
    plate = labware.load('biorad-hardshell-96-PCR', '1')
    reagent_tubes = labware.load('96-PCR-tall', '5')

    tipracks_m10 = labware.load(p10_tiprack_type, '10')
    tipracks_p10 = labware.load(p10_tiprack_type, '11')

    # instruments setup
    m10 = instruments.P10_Multi(
        mount='right',
        tip_racks=[tipracks_m10])
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=[tipracks_p10])

    # reagent setup
    i5_primers = reagent_tubes.cols('1')
    i7_primers = reagent_tubes.wells('A2', length=number_of_columns)

    for index, primer in enumerate(i7_primers):
        p10.pick_up_tip()
        for well in plate.cols(index):
            p10.set_flow_rate(aspirate=2, dispense=2)
            p10.transfer(1.25, primer, well.top(), new_tip='never')
            p10.set_flow_rate(dispense=20)
            p10.blow_out(well.top())
        p10.drop_tip()

    m10.pick_up_tip()
    for col in plate.cols('1', length=number_of_columns):
        m10.set_flow_rate(aspirate=2, dispense=2)
        m10.transfer(1.25, i5_primers, col[0].top(), new_tip='never')
        m10.set_flow_rate(dispense=20)
        m10.blow_out(col[0].top())
    m10.drop_tip()

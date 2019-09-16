from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'Axygen-96-well'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        depth=15.1,
        diameter=5.22,
        volume=200
        )

plate_name_2 = 'Axygen-96-well_Cold'
if plate_name_2 not in labware.list():
    labware.create(
        plate_name_2,
        grid=(12, 8),
        spacing=(9, 9),
        depth=14.75,
        diameter=5.22,
        volume=200
        )

# labware and modules
tempdeck = modules.load('tempdeck', '1')
plate1 = labware.load(plate_name_2, '1', share=True)
barcode_plate = labware.load(plate_name, '2')
dna_plate = labware.load(plate_name, '3')
tubes = labware.load('opentrons-aluminum-block-2ml-eppendorf', '4')
single_tips = [labware.load('tiprack-10ul', slot)
               for slot in ['5', '6']]
multi_tips = [labware.load('tiprack-10ul', slot)
              for slot in ['7', '8']]

# tube setup
mm = tubes.wells('A1')
edta = tubes.wells('A2')

# set temperature
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()


def run_custom_protocol(
        p10_multi_mount: StringSelection('right', 'left') = 'right',
        p10_single_mount: StringSelection('left', 'right') = 'left',
        aspirate_ratio: float = 0.5,
        dispense_ratio: float = 2,
        number_of_sample_columns: int = 12,
        volume_of_mastermix_in_ul: float = 7,
        volume_of_DNA_to_pool_in_ul: float = 9
):

    # check
    if p10_multi_mount == p10_single_mount:
        raise Exception('Pipette mounts must be distinct.')
    if number_of_sample_columns > 12 or number_of_sample_columns < 1:
        raise Exception('Number of sample columns must be between 1-12 \
(inclusive).')

    # pipettes
    p10 = instruments.P10_Single(mount=p10_single_mount, tip_racks=single_tips)
    m10 = instruments.P10_Multi(mount=p10_multi_mount, tip_racks=multi_tips)

    # slow flow rates
    p10.set_flow_rate(aspirate=5*aspirate_ratio, dispense=10*dispense_ratio)
    m10.set_flow_rate(aspirate=5*aspirate_ratio, dispense=10*dispense_ratio)

    # transfer barcode to corresponding well
    for s, d in zip(
            barcode_plate.rows('A')[:number_of_sample_columns],
            plate1.rows('A')[:number_of_sample_columns]
    ):
        m10.pick_up_tip()
        m10.transfer(
            2,
            s,
            d,
            new_tip='never'
        )
        m10.blow_out()
        m10.drop_tip()

    # transfer mm with air gap
    num_dests = number_of_sample_columns*8
    dests = [well.bottom(0.5) for well in plate1.wells('A1', length=num_dests)]
    for d in dests:
        p10.pick_up_tip()
        p10.aspirate(10-volume_of_mastermix_in_ul, mm.top())
        p10.aspirate(volume_of_mastermix_in_ul, mm)
        p10.dispense(10, d)
        p10.blow_out()
        p10.drop_tip()

    # transfer dna to corresponding well and mix
    sources = dna_plate.rows('A')[0:number_of_sample_columns]
    dests = plate1.rows('A')[0:number_of_sample_columns]
    for source, dest in zip(sources, dests):
        m10.pick_up_tip()
        m10.transfer(
            2,
            source,
            dest,
            new_tip='never'
        )
        m10.mix(10, 9, dest)
        m10.blow_out(dest.top())
        m10.drop_tip()

    robot.pause('Perform reaction. Resume when finished...')

    # consolidate dna in tube 2
    p10.pick_up_tip()
    sources = dna_plate.wells('A1', len=num_dests)
    for s in sources:
        p10.aspirate(10-volume_of_DNA_to_pool_in_ul, s.top())
        p10.aspirate(volume_of_DNA_to_pool_in_ul, s)
        p10.dispense(10, edta)
        p10.blow_out()
    p10.mix(10, 9, edta)
    p10.blow_out(edta.top())
    p10.drop_tip()

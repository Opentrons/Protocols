from opentrons import labware, instruments, modules, robot

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

# labware and modules
tempdeck = modules.load('tempdeck', '1')
plate1 = labware.load(plate_name, '1', share=True)
barcode_plate = labware.load(plate_name, '2')
dna_plate = labware.load(plate_name, '3')
tubes = labware.load('opentrons-aluminum-block-2ml-eppendorf', '4')
single_tips = [labware.load('tiprack-10ul', slot)
               for slot in ['5', '6']]
multi_tips = [labware.load('tiprack-10ul', slot)
              for slot in ['7', '8']]

# pipettes
p10 = instruments.P10_Single(mount='right', tip_racks=single_tips)
m10 = instruments.P10_Multi(mount='left', tip_racks=multi_tips)

# slow flow rates
p10.set_flow_rate(aspirate=2.5, dispense=5)
m10.set_flow_rate(aspirate=2.5, dispense=5)

# tube setup
mm = tubes.wells('A1')
edta = tubes.wells('A2')

# set temperature
if not robot.is_simulating():
    tempdeck.set_temperature(4)
    tempdeck.wait_for_temp()


def run_custom_protocol(number_of_sample_columns: int = 12,
                        volume_of_DNA_to_pool: float = 10):
    # transfer barcode to corresponding well
    m10.transfer(
        2,
        barcode_plate.rows('A')[0:number_of_sample_columns],
        plate1.rows('A')[0:number_of_sample_columns],
        new_tip='always',
        blow_out=True
        )

    # transfer mm with air gap
    num_dests = number_of_sample_columns*8
    dests = plate1.wells('A1', len=num_dests)
    for d in dests:
        p10.pick_up_tip()
        p10.aspirate(3, mm.top())
        p10.aspirate(7, mm)
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
            new_tip='never',
            blow_out=True
            )
        m10.mix(10, 10, dest)
        m10.blow_out(dest.top())
        m10.drop_tip()

    robot.pause('Perform reaction. Resume when finished...')

    # consolidate dna in tube 2
    p10.pick_up_tip()
    sources = dna_plate.wells('A1', len=num_dests)
    for s in sources:
        p10.aspirate(10-volume_of_DNA_to_pool, s.top())
        p10.aspirate(volume_of_DNA_to_pool, s)
        p10.dispense(10, edta)
        p10.blow_out()
    p10.mix(10, 9, edta)
    p10.blow_out(edta.top())
    p10.drop_tip()

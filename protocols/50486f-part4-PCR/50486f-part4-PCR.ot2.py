from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep 4/4: PCR',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

pcrcool = 'labcon_96_wellplate_pcr_on_cooler'
if pcrcool not in labware.list():
    labware.create(
        pcrcool,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=20,
        volume=200
    )
tempplate = labware.load(pcrcool, '1', 'Labcon Plate on PCR Cooler')

pcr_well = labware.load(pcrcool, '2', 'PCR Strip on PCR Cooler')

primer_plate = labware.load(
            'biorad_96_wellplate_200ul_pcr', '3', 'primer plate (BioRad)')
dna_plate = labware.load(
            'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '4',
            'DNA plate on Aluminum Block')
tipracks = [
    labware.load('tiprack-10ul', slot) for slot in range(5, 12)
]


def run_custom_protocol(
        p10_mount: StringSelection('left', 'right') = 'left',
        number_of_plates: int = 1
):

    # Check number of plates
    if number_of_plates > 6 or number_of_plates < 1:
        raise Exception('The number of plates should be between 1 and 6.')

    # create pipette

    pip10 = instruments.P10_Multi(mount=p10_mount, tip_racks=tipracks)

    tip10_max = len(tipracks)*12
    tip10_count = 0

    def pick_up(pip):
        nonlocal tip10_count

        if tip10_count == tip10_max:
            robot.pause(
                'Replace 10ul tipracks in slots 7, 8, and 9 before resuming.')
            pip10.reset()
            tip10_count = 0
        pip10.pick_up_tip()
        tip10_count += 1

    dest = tempplate.rows('A')
    primers = primer_plate.rows('A')
    samps = dna_plate.rows('A')

    for i in range(number_of_plates):
        # step 1

        pick_up(pip10)

        for d in dest:
            pip10.transfer(8.7, pcr_well.wells('A1'), d, new_tip='never')
            pip10.blow_out(d.top())

        pip10.drop_tip()

        # step 2

        for p, d in zip(primers, dest):
            pick_up(pip10)
            pip10.transfer(1.3, p, d, new_tip='never')
            pip10.blow_out(d.top())
            pip10.drop_tip()

        # step 3

        for s, d in zip(samps, dest):
            pick_up(pip10)
            pip10.transfer(5, s, d, new_tip='never')
            pip10.blow_out(d.top())
            pip10.drop_tip()

        if i == number_of_plates-1:
            robot.comment("Congratulations, you have completed step 4/4 of this \
            protocol. Please remove samples from OT-2 and properly store.")
        else:
            robot.pause("Congratulations, you have completed step 4/4 of this \
            protocol for plate "+str(i+1)+". Please remove samples from OT-2 \
            and properly store. When you're ready to fill the next plate, \
            please load proper materials and click RESUME.")

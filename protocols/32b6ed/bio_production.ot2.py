from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Production of Biological Products',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
disc_plate_name = 'bioquell_48_discplate_56ul'
if disc_plate_name not in labware.list():
    labware.create(
        disc_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=9,
        depth=2,
        volume=56
    )

tiprack_name = 'eppendorf_96_tiprack_300ul'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3,
        depth=60
    )

# load labware
disc_plate = labware.load(disc_plate_name, '1', 'carrier disc plate')
sol_a = labware.load(
    'agilent_1_reservoir_290ml', '2', 'solution A').wells(0)
tiprack300 = labware.load(tiprack_name, '4')


def run_custom_protocol(
        p300_single_mount: StringSelection('right', 'left') = 'right',
        number_of_discs_to_receive_solution: int = 48,
        volume_of_solution_to_transfer_in_ul: float = 50,
        transfer_plan: StringSelection(
            'distribution', 'single transfers') = 'distribution',
        circle_destination_well: StringSelection('yes', 'no') = 'yes',
        tip_well: str = 'A1'
):
    # check
    if (
            number_of_discs_to_receive_solution < 1
            or number_of_discs_to_receive_solution > 48
    ):
        raise Exception('Invalid number of discs to receive solution \
(must be 1-48).')
    if volume_of_solution_to_transfer_in_ul > 50:
        robot.pause('WARNING: Discs may overflow with selected volume. Resume \
to continue.')
    if tip_well.upper() not in [
            t.get_name() for t in tiprack300.get_all_children()]:
        raise Exception('Invalid tip well (must be A1-H12).')

    # pipette
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=[tiprack300])

    # setup discs
    dests = [
        well for row in [row[::2] if i % 2 == 0 else row[1::2]
                         for i, row in enumerate(disc_plate.rows())]
        for well in row
    ][:number_of_discs_to_receive_solution]

    # distribute solution
    p300.pick_up_tip(tiprack300.wells(tip_well))
    if transfer_plan == 'distribution':
        p300.distribute(
            volume_of_solution_to_transfer_in_ul,
            sol_a,
            [d.top(1) for d in dests],
            new_tip='never',
            disposal_vol=10,
            blow_out=True
        )
    else:
        for d in dests:
            p300.transfer(
                volume_of_solution_to_transfer_in_ul,
                sol_a,
                d.top(0.5),
                new_tip='never')
            if circle_destination_well == 'yes':
                # move around well
                [p300.move_to((d, d.from_center(r=0.9, h=0, theta=angle/10)))
                    for angle in range(0, 63, 6)]
            else:
                # standard touch tip
                p300.touch_tip(d, 0.9, 0.5, 20)
            p300.blow_out(d.top(5))
    p300.drop_tip()

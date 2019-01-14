from opentrons import labware, instruments, robot

microplate_name = 'greiner-384-square-1'
if microplate_name not in labware.list():
    labware.create(
        microplate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.7,
        depth=11.5)

# labware setup
destination = labware.load(microplate_name, '2', 'Destination')
destination.properties['height'] = 14.5

master = labware.load(microplate_name, '1', 'Master')
master.properties['height'] = 14.5

control_1 = labware.load(microplate_name, '3', 'Control 1')
control_1.properties['height'] = 14.5

control_2 = labware.load(microplate_name, '5', 'Control 2')
control_2.properties['height'] = 14.5

tipracks = [labware.load('tiprack-10ul', str(slot))
            for slot in ['4', '6', '7', '8']]

# instruments setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks)


def run_custom_protocol(
        sample_volume: float=5,
        control_volume: float=5,
        control_column: str=1,
        number_of_destination_plates: int=4):

    if number_of_destination_plates > 4:
        raise Exception("Number of plates cannot exceed 4.")

    for plate_num in range(number_of_destination_plates):

        # transfer samples
        sample_cols = [col for col in master.cols(plate_num*6, length=6)]
        for well_index in range(2):
            for index, sample in enumerate(sample_cols, 1):
                source = sample[well_index]
                dests = [col[well_index].top(-6)
                         for col in destination.cols(index*3, length=3)]
                for dest in dests:
                    m10.pick_up_tip()
                    m10.transfer(sample_volume, source, dest, new_tip='never')
                    m10.blow_out(dest)
                    m10.drop_tip()

        # transfer controls
        ctrl_1 = [well for well in control_1.cols(control_column)[:2]]
        ctrl_2 = [well for well in control_2.cols(control_column)[:2]]
        ctrl_1_dest = [[destination.cols(col_num)[index]
                       for col_num in ['2', '22']]
                       for index in range(2)]
        ctrl_2_dest = [[destination.cols(col_num)[index]
                       for col_num in ['3', '23']]
                       for index in range(2)]

        for source, dests in zip(ctrl_1, ctrl_1_dest):
            for dest in dests:
                m10.transfer(control_volume, source, dest.top(-6))

        for source, dests in zip(ctrl_2, ctrl_2_dest):
            for dest in dests:
                m10.transfer(control_volume, source, dest.top(-6))

        if not plate_num == (number_of_destination_plates-1):
            robot.pause("Put a new plate in slot 2 and refill all of the \
tipracks.")
            m10.reset_tip_tracking()

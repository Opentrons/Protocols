from opentrons import labware, instruments, robot
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': '',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

example_csv = """
Destination,Sample_ID,Diluent,Sample
Plate2-A1,Plate1-A1,0,22.3
Plate2-A2,Plate1-A2,27.9,32.1
Plate2-A3,Plate1-A3,66,14
Plate2-A4,Plate1-A4,62.6,17.4
Plate5-B1,Plate4-B1,67.8,12.2
Plate5-B2,Plate4-B2,61.5,18.5
Plate5-B3,Plate4-B3,66.6,13.4
Plate5-B4,Plate4-B4,61,19
Plate8-C1,Plate7-C1,56,24
Plate8-C2,Plate7-C2,53.5,26.5
Plate8-C3,Plate7-C3,63.9,16.1
Plate8-C4,Plate7-C4,52.8,27.2
"""

output_plate_name = 'ssibio-96-PCR-semi-skirted'
if output_plate_name not in labware.list():
    labware.create(
        output_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=19.85,
        volume=350
        )


def run_custom_protocol(
    volume_csv: FileInput=example_csv,
    pause_to_spin_plate: StringSelection('True', 'False')='True'
        ):

    # labware setup
    plates = {slot: labware.load(plate_type, slot)
              for slots, plate_type in zip(
                [['1', '4', '7'], ['2', '5', '8']],
                ['biorad-hardshell-96-PCR', output_plate_name])
              for slot in slots}

    diluent = labware.load('trough-1row', '3').wells('A1')
    tipracks = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['6', '9', '10', '11']]

    # instruments setup
    p50 = instruments.P50_Single(
        mount='left',
        tip_racks=tipracks)
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=tipracks)

    def volume_csv_to_lists(csv_string):
        info_list = [cell for line in csv_string.splitlines() if line
                     for cell in [line.split(',')]]
        sample_vols = []
        diluent_vols = []
        dests = []
        samples = []
        for line in info_list[1:]:
            dest_info = line[0].split('-')
            dest = plates[dest_info[0][-1]].wells(dest_info[1])
            sample_info = line[1].split('-')
            sample = plates[sample_info[0][-1]].wells(sample_info[1])
            diluent_vol = float(line[2])
            sample_vol = float(line[3])
            dests.append(dest)
            samples.append(sample)
            diluent_vols.append(diluent_vol)
            sample_vols.append(sample_vol)
        return sample_vols, diluent_vols, dests, samples

    tips = [well for rack in tipracks for well in rack]

    volume_csv = example_csv
    sample_vols, diluent_vols, dests, samples = volume_csv_to_lists(volume_csv)

    # transfer diluent
    for vol, dest in zip(diluent_vols, dests):
        if not vol > 0:
            pass
        else:
            if vol <= 50:
                pipette = p50
            else:
                pipette = p300
            if not pipette.tip_attached:
                pipette.pick_up_tip(tips[0])
                tips.pop(0)
                pipette.mix(2, diluent)
            pipette.transfer(vol, diluent, dest, new_tip='never')
            pipette.blow_out(dest)
            pipette.touch_tip(dest)
    if p50.tip_attached:
        p50.drop_tip()
    if p300.tip_attached:
        p300.drop_tip()

    if pause_to_spin_plate == 'True':
        robot.pause("Seal and spin plates down. Place the plates back to the \
slots before resuming.")

    # transfer samples
    for vol, sample, dest in zip(sample_vols, samples, dests):
        if vol <= 50:
            pipette = p50
        else:
            pipette = p300
        pipette.pick_up_tip(tips[0])
        tips.pop(0)
        pipette.mix(2, sample)
        pipette.transfer(vol, sample, dest, new_tip='never')
        pipette.mix(5, dest)
        pipette.blow_out(dest)
        pipette.touch_tip(dest)
        pipette.drop_tip()

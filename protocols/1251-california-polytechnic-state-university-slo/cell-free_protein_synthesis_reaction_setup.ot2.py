from opentrons import labware, instruments, modules
from otcustomizers import FileInput

# labware setup
aluminum_tuberack = labware.load('opentrons-aluminum-block-2ml-screwcap', '5')
temp_module = modules.load('tempdeck', '4')
pcr_plate = labware.load('opentrons-aluminum-block-96-PCR-plate', '4',
                         share=True)
tiprack10 = labware.load('tiprack-10ul', '1')
tiprack50 = labware.load('tiprack-200ul', '2')

# reagent setup
water = aluminum_tuberack.wells('A1')
extract = aluminum_tuberack.wells('B1')
dna = aluminum_tuberack.wells('C1')
buffer_1 = aluminum_tuberack.wells('D1', length=5)
buffer_2 = aluminum_tuberack.wells('A3', length=5)
buffer_3 = aluminum_tuberack.wells('B4', length=5)
solution_a = aluminum_tuberack.wells('C5')
solution_b = aluminum_tuberack.wells('D5')

# pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack10])

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack50])

example_csv = """
Destination,Water,Solution A,Solution B,DNA,Buffer 1,Buffer 2,Buffer 3,Extract
H1-E1,11.4,4.4,4.2,0,0,0,0,10
D1-A1,9.4,4.4,4.2,2,0,0,0,10
H2-E2,7.4,4.4,4.2,2,A:2,0,0,10
D2-A2,5.4,4.4,4.2,2,B:2,A:2,0,10
H3-E3,5.4,4.4,4.2,2,C:2,B:2,0,10
D3-A3,5.4,4.4,4.2,2,D:2,C:2,0,10

"""


def csv_to_dict(csv_string):
    new_list = [line.split(',') for line in csv_string.splitlines() if line]
    headers = ['wells', water, solution_a, solution_b, dna, buffer_1, buffer_2,
               buffer_3, extract]
    new_dict = {header: [] for header in headers}
    for line in new_list[1:]:
        for header, info in zip(headers, line):
            if header == 'wells':
                wells = info.split('-')
                info = pcr_plate.wells(wells[0], to=wells[1])
            new_dict[header].append(info)
    return new_dict


def get_destinations(locations, reagent_vol_list):
    dest = []
    volume = []
    for group_loc, vol in zip(locations, reagent_vol_list):
        for loc in group_loc:
            if float(vol) > 0:
                dest.append(loc.top())
                volume.append(float(vol))
    return dest, volume


def run_custom_protocol(
        volume_csv: FileInput=example_csv):

    info = csv_to_dict(volume_csv)

    # transfer water to each well
    dest, volume = get_destinations(info['wells'], info[water])
    if dest and volume:
        p10.distribute(volume, water, dest, disposal_vol=0)

    # transfer extract to each well
    dest, volume = get_destinations(info['wells'], info[extract])
    if dest and volume:
        p50.pick_up_tip()
        p50.mix(3, 50, extract)
        p50.distribute(volume, extract, dest, disposal_vol=0,
                       mix_before=(2, 50), new_tip='never')
        p50.drop_tip()

    # transfer dna to each well
    dest, volume = get_destinations(info['wells'], info[dna])
    if dest and volume:
        p10.pick_up_tip()
        p10.mix(3, 10, dna)
        p10.distribute(volume, dna, dest, disposal_vol=0, mix_before=(2, 10),
                       new_tip='always')

    alphabets = ['a', 'b', 'c', 'd', 'e']

    # transfer buffer 1A-E to each well
    for alpha, buffer_loc in zip(alphabets, buffer_1):
        new_vol = []
        for vol in info[buffer_1]:
            if vol.split(':')[0].lower() == alpha:
                new_vol.append(vol.split(':')[1])
            else:
                new_vol.append('0')
        dest, volume = get_destinations(info['wells'], new_vol)
        if dest and volume:
            p10.pick_up_tip()
            p10.mix(5, 10, buffer_loc)
            p10.distribute(volume, buffer_loc, dest, disposal_vol=0)

    # transfer buffer 2A-E to each well
    for alpha, buffer_loc in zip(alphabets, buffer_2):
        new_vol = []
        for vol in info[buffer_2]:
            if vol.split(':')[0].lower() == alpha:
                new_vol.append(vol.split(':')[1])
            else:
                new_vol.append('0')
        dest, volume = get_destinations(info['wells'], new_vol)
        if dest and volume:
            p10.pick_up_tip()
            p10.mix(5, 10, buffer_loc)
            p10.distribute(volume, buffer_loc, dest, disposal_vol=0)

    # transfer buffer 3A-E to each well
    for alpha, buffer_loc in zip(alphabets, buffer_3):
        new_vol = []
        for vol in info[buffer_3]:
            if vol.split(':')[0].lower() == alpha:
                new_vol.append(vol.split(':')[1])
            else:
                new_vol.append('0')
        dest, volume = get_destinations(info['wells'], new_vol)
        if dest and volume:
            p10.pick_up_tip()
            p10.mix(5, 10, buffer_loc)
            p10.distribute(volume, buffer_loc, dest, disposal_vol=0)

    # transfer solution A to each well
    dest, volume = get_destinations(info['wells'], info[solution_a])
    if dest and volume:
        p50.pick_up_tip()
        p50.mix(5, 50, solution_a)
        for index in range(0, len(dest), 8):
            p50.distribute(
                volume[index:index + 8],
                solution_a,
                dest[index:index + 8],
                disposal_vol=0,
                mix_before=(5, 50),
                new_tip='always')

    # transfer solution B to each well
    dest, volume = get_destinations(info['wells'], info[solution_b])
    if dest and volume:
        p50.pick_up_tip()
        p50.mix(10, 50, solution_b)
        for index in range(0, len(dest), 8):
            p50.distribute(
                volume[index:index + 8],
                solution_b,
                dest[index:index + 8],
                disposal_vol=0,
                mix_before=(10, 50),
                new_tip='always')

    # mix each PCR tube 2x, change tips every 4 tubes
    for group in info['wells']:
        p50.pick_up_tip()
        for loc in group:
            p50.mix(2, 50, loc)
        p50.drop_tip()

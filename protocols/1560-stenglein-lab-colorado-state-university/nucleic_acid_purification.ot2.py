from opentrons import labware, instruments, modules, robot
from otcustomizers import FileInput

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'Biorad-96-high-unskirted'
if plate_name not in labware.list():
    labware.create(plate_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   depth=19.85,
                   diameter=5.5,
                   volume=300)

# labware
start_plate = labware.load(plate_name, '2')
new_plate = labware.load(plate_name, '3')
trough = labware.load('trough-12row', '4')
tips = [labware.load('opentrons-tiprack-300ul', str(slot))
        for slot in range(5, 12)]

# modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(plate_name, '1', share=True)

# pipette
m300 = instruments.P300_Multi(mount='left', tip_racks=tips)

# reagent setup
isopropanol = trough.wells('A1')
beads = trough.wells('A2')
wash_buffer_1 = trough.wells('A3')
DNase = trough.wells('A4')
binding_buffer = trough.wells('A5')
wash_buffer_2 = trough.wells('A6')
autoclave_ddH2O = trough.wells('A7')
waste = trough.wells('A12')

example = """1,2,3,4,5,6,7,8,9,10,11,12"""


def get_cols_from_csv(file_string):
    whole_file = file_string.splitlines()
    cols = whole_file[0]
    els = cols.split(',')
    return(els)


def run_custom_protocol(volume_autoclave_ddH2O: float = 50,
                        file: FileInput = example):

    # wash function
    def wash(wash_buffer):
        magdeck.disengage()
        m300.set_flow_rate(aspirate=150)
        m300.distribute(150,
                        wash_buffer,
                        [well.top() for well in mag_samples])

        for s in mag_samples:
            m300.pick_up_tip()
            m300.mix(10, 150, s)
            m300.drop_tip()

        m300.delay(minutes=2)
        robot._driver.run_flag.wait()
        magdeck.engage(height=18)
        m300.delay(minutes=3)
        m300.set_flow_rate(aspirate=25)

        m300.transfer(150, mag_samples, waste, new_tip='always')

    # setup samples and tips
    cols = get_cols_from_csv(file)
    start_samples = [start_plate.rows['A'][col] for col in cols]
    mag_samples = [mag_plate.rows['A'][col] for col in cols]
    new_samples = [new_plate.rows['A'][col] for col in cols]

    for s in start_samples:
        m300.pick_up_tip()
        m300.transfer(60,
                      isopropanol,
                      s,
                      new_tip='never')
        m300.mix(10, 60, s)
        m300.drop_tip()

    m300.delay(minutes=1)

    m300.pick_up_tip()
    m300.mix(10, 300, beads),
    m300.distribute(100,
                    beads,
                    [s.top() for s in mag_samples],
                    new_tip='never')
    m300.drop_tip()

    for source, dest in zip(start_samples, mag_samples):
        m300.pick_up_tip()
        m300.transfer(160,
                      source,
                      dest,
                      new_tip='never')
        m300.mix(15, 160, dest)
        m300.drop_tip()

    m300.delay(minutes=10)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)
    m300.set_flow_rate(aspirate=25)

    m300.transfer(160, mag_samples, waste, new_tip='always')

    robot.pause('Please reload tipracks if necessary before resuming.')
    m300.reset()

    # 2x buffer wash
    for _ in range(2):
        wash(wash_buffer_1)

    magdeck.disengage()

    # distribute DNase, mix, and incubate
    m300.distribute(30, DNase, [s.top() for s in mag_samples])
    for s in mag_samples:
        m300.pick_up_tip()
        m300.mix(10, 30, s)
        m300.drop_tip()
    m300.delay(minutes=30)

    # distribute binding buffer, mix, and incubate
    m300.distribute(100, binding_buffer, [s.top() for s in mag_samples])
    for s in mag_samples:
        m300.pick_up_tip()
        m300.mix(10, 130, s)
        m300.drop_tip()
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)

    robot.pause('Please reload tipracks if necessary before resuming.')
    m300.reset()

    m300.transfer(130, mag_samples, waste, new_tip='always')

    # 2x buffer wash
    for _ in range(2):
        wash(wash_buffer_2)

    # dry beads
    m300.delay(minutes=3)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    # distribute autoclave ddH2O, mix, and incubate
    m300.distribute(volume_autoclave_ddH2O,
                    autoclave_ddH2O,
                    [s.top() for s in mag_samples])
    for s in mag_samples:
        m300.pick_up_tip()
        m300.mix(10, volume_autoclave_ddH2O, s)
        m300.drop_tip()
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)

    robot.pause('Please reload a tiprack in slot 5 if necessary before '
                'resuming.')
    m300.reset()

    m300.transfer(volume_autoclave_ddH2O-2,
                  mag_samples,
                  new_samples,
                  new_tip='always')

    magdeck.disengage()
